from nlu import SemanticNLU
from question import QuestionAnswer
from models import *
from goals import *
from error import *
from helpers import *
from app import logger

state_machine = {
    "home": {
        "create_procedure": "creating",
        "execute": "executing",
        "edit": "editing"
    },
    "creating": {
        "complete": "home"
    },
    "editing": {
        "add_step": "editing_action",
        "change_step": "editing_action",
        "complete": "home"
    },
    "executing": {
        "finish": "home"
    },
    "editing_action": {
        "complete": "editing"
    }
}

allowed_goals = {
    "home": [HomeGoal, GetInputGoal],
    "creating": [ActionGoal, GetActionsGoal, GetConditionGoal, GetInputGoal],
    "editing": [StepGoal, GetInputGoal, ActionGoal, GetActionsGoal, GetConditionGoal],
    "editing_action": [ActionGoal, GetActionsGoal, GetConditionGoal, GetInputGoal],
    "executing": [GetUserInputGoal, GetInputGoal]
}

class DialogManager(object):
    def __init__(self, sid):
        self.sid = sid
        self.context = DialogContext(sid)
        self.qa = QuestionAnswer(self.context)
        self.nlu = SemanticNLU(self.context)
        logger.debug(f"[{self.sid}] Created dialog manager.")

    def reset(self, context=None):
        if context is not None:
            self.context = context
            self.qa = QuestionAnswer(context)
            self.nlu = SemanticNLU(context)
        else:
            self.context.reset()
        logger.debug(f"[{self.sid}] Resetting the entire conversation.")
        return "Conversation has been reset. What do you want to do first?"

    @property
    def immediate_goal(self):
        current = self.context.current_goal
        while current and current.todos:
            current = current.todos[-1]
        return current

    def current_goal(self):
        return self.context.current_goal

    def handle_message(self, message):
        self.context.add_message(message)

        response = self.handle_reset(message)
        if response is not None:
            logger.debug(f"[{self.sid}] User resetted.")
            return response

        response = self.handle_help(message)
        if response is not None:
            logger.debug(f"[{self.sid}] User needed help.")
            return response

        if self.context.state == "executing":
            logger.debug(f"[{self.sid}] Program is currently executing.")
            return self.handle_execution(message)

        response = self.handle_cancel(message)
        if response is not None:
            logger.debug(f"[{self.sid}] User canceled.")
            return response

        response = self.handle_question(message)
        if response is not None:
            logger.debug(f"[{self.sid}] User asked a question.")
            return response

        response = self.handle_parse(message)
        if response is not None:
            return response

        return self.handle_goal()

    def handle_reset(self, message):
        # Check for reset
        if message.lower() == "reset":
            return self.reset()

    def handle_help(self, message):
        # Check for help
        if message.lower() in ["help", "i need help"]:
            return "Raise your hand and help will be on the way!"

    def handle_execution(self, message):
        # Check if running program
        execution = self.context.execution
        if message.lower() in ["stop", "cancel"]:
            execution.finish("Procedure has been stopped.")
        elif execution.input_needed:
            execution.run(message)
        else:
            return "Procedure is still executing."
        return

    def handle_cancel(self, message):
        # Check if desire to cancel goal
        if message.lower() == "cancel":
            if self.context.goals:
                self.context.goals.pop()
            self.context.state = "home"
            return "Canceled! What do you want to do?"

    def handle_question(self, message):
        # Check if message is a question
        if QuestionAnswer.is_question(message):
            answer = self.qa.answer(message)
            if answer is not None:
                return answer

    def handle_parse(self, message):
        try:
            self.context.parsed = self.nlu.parse_message(message)
        except InvalidStateError as e:
            response = "I cannot do this right now"
            if isinstance(e.goal, ActionGoal):
                logger.debug(f"[{self.sid}] Invalid state to do action because currently not creating or editing a procedure.")
                response += " because I am currently not creating or editing a procedure"
            elif isinstance(e.goal, StepGoal):
                if e.state == "editing_action":
                    logger.debug(f"[{self.sid}] Invalid state to do action because currently adding or editing an action.")
                    response += " because I am currently adding or editing an action"
                else:
                    logger.debug(f"[{self.sid}] Invalid state to do action because currently not editing a procedure.")
                    response += " because I am currently not editing a procedure"
            elif isinstance(e.goal, HomeGoal):
                if e.state == "creating":
                    logger.debug(f"[{self.sid}] Invalid state to do action because currently creating a procedure.")
                    response += " because I am currently creating a procedure. You can stop by saying \"done\""
                elif e.state == "editing":
                    logger.debug(f"[{self.sid}] Invalid state to do action because currently editing a procedure.")
                    response += " because I am currently editing a procedure. You can stop by saying \"done\""
                elif e.state == "editing_action":
                    logger.debug(f"[{self.sid}] Invalid state to do action because adding or editing an action.")
                    response += " because I am currently adding or editing an action. Finish editing then you can stop by saying \"done\""
            else:
                logger.debug(f"[{self.sid}] Invalid state to do action.")
            return f"{response}."

    def handle_goal(self):
        if self.current_goal() is None:
            goal = self.context.parsed
            if goal is None or not isinstance(goal, BaseGoal):
                logger.debug(f"[{self.sid}] Did not understand utterance: {self.context.current_message}")
                response = "I didn't understand what you were saying. Please try again."
            elif goal.error is not None:
                response = goal.error
            elif goal.is_complete:
                response = goal.complete()
            else:
                response = goal.message
                self.context.add_goal(goal)
        else:
            goal = self.current_goal()
            goal.advance()
            if goal.error is not None:
                response = goal.error
                self.context.goals.pop()
            elif goal.is_complete:
                response = goal.complete()
                self.context.goals.pop()
            else:
                response = goal.message

        return response

class DialogContext(object):
    def __init__(self, sid):
        self.sid = sid
        self.classes = { }
        self.procedures = { }
        self.execution = None
        self.reset()

    @property
    def current_message(self):
        return self.conversation[-1].lower() if self.conversation else None

    @property
    def current_goal(self):
        return self.goals[-1] if self.goals else None

    def reset(self):
        if self.execution is not None:
            self.execution.finish()
        self.state = "home"
        self.conversation = []
        self.goals = []
        self.current = None
        self.execution = None
        self.edit = None

    def add_message(self, message):
        self.conversation.append(message)

    def add_goal(self, goal):
        self.goals.append(goal)

    def add_class(self, klass):
        self.classes[klass.name] = klass

    def add_procedure(self, procedure):
        self.procedures[procedure.name] = procedure

    def get_class(self, name):
        return self.classes.get(name)

    def validate_goal(self, goal):
        allowed = any([type(goal) == goaltype or isinstance(goal, goaltype) for goaltype in allowed_goals[self.state]])
        if not allowed:
            raise InvalidStateError(goal, self.state)

    def transition(self, action):
        self.state = state_machine[self.state][str(action)]
