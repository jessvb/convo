from nlu import SemanticNLU
from rasa_nlu import RasaNLU
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
        "edit": "editing",
        "connect_intent": "editing"
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
    """Represents a dialog manager for a client"""
    def __init__(self, sid, rasa_port="5005", procedures={}):
        self.sid = sid
        self.rasa_port = rasa_port
        self.context = DialogContext(sid, rasa_port, procedures)
        self.qa = QuestionAnswer(self.context)
        self.nlu = SemanticNLU(self.context)
        self.rasa = RasaNLU(self.context)

    def reset(self, context=None):
        """Resets the context either entirely or to a snapshot of another context"""
        if context is not None:
            # If a context is provided, set the context to the provided context
            self.context = context
            self.qa = QuestionAnswer(context)
            self.nlu = SemanticNLU(context)
            self.rasa = RasaNLU(context)
        else:
            self.context.reset()
        logger.debug(f"[{self.sid}] Resetting the entire conversation.")
        return "Conversation has been reset. What do you want to do first?"

    @property
    def immediate_goal(self):
        """Returns the immediate, lowest-level current goal"""
        current = self.context.current_goal
        while current and current.todos:
            current = current.todos[-1]
        return current

    def current_goal(self):
        """Returns the current high-level goal, may contain other goals in its todos"""
        return self.context.current_goal

    def handle_message(self, message, isUnconstrained):
        """Handle messages by the client"""
        self.context.add_message(message)

        # Handle message indicating a reset
        response = self.handle_reset(message)
        if response is not None:
            logger.debug(f"[{self.sid}] User resetted.")
            return response

        # If message indicates client needed help, return appropriate response
        response = self.handle_help(message)
        if response is not None:
            logger.debug(f"[{self.sid}] User needed help.")
            return response

        # Handle messages received by server during program execution
        if self.context.state == "executing":
            logger.debug(f"[{self.sid}] Program is currently executing.")
            return self.handle_execution(message)

        # Handle message indicating a canceling of the immediate goal
        response = self.handle_cancel(message)
        if response is not None:
            logger.debug(f"[{self.sid}] User canceled.")
            return response

        # Handle message that may be question and answer it
        response = self.handle_question(message)
        if response is not None:
            logger.debug(f"[{self.sid}] User asked a question.")
            return response

        # If none of the above, parse the message for either a goal or slot-filling value
        response = self.handle_parse(message, isUnconstrained)
        if response is not None:
            return response

        return self.handle_goal()

    def handle_reset(self, message):
        """Check for reset"""
        if message.lower() == "reset":
            return self.reset()

    def handle_help(self, message):
        """Check for help"""
        if message.lower() in ["help", "i need help"]:
            return "Raise your hand and help will be on the way!"

    def handle_execution(self, message):
        """Check if DM in stage of execution"""
        execution = self.context.execution
        if message.lower() in ["stop", "cancel"]:
            # Stop execution if user commands it
            execution.finish("Procedure has been stopped.")
        elif execution.input_needed:
            # If execution was paused to ask for user input, continue the execution with provided input
            execution.run(message)
        else:
            # Do not allow any other action besides the two cases above
            return "Procedure is still executing."
        return

    def handle_cancel(self, message):
        """
        Check for cancellation

        If cancel, cancels the lowest-level goal that is not a "Get Input" or "Get Condition" goal
        For example, if the goal chain is "Add Step" -> "Create Variable" -> "Get Input", it will cancel "Create Variable"
        """
        if message.lower() == "cancel":
            previous = None
            current = self.context.current_goal
            while current and current.todos:
                if isinstance(current.todos[-1], GetInputGoal) or isinstance(current.todos[-1], GetConditionGoal):
                    break
                previous, current = current, current.todos[-1]

            logger.debug(f"[{self.context.sid}] Canceling the current goal: {current}")
            current.cancel()
            if current is None:
                return "You are not doing anything right now. What do you want to do?"
            elif previous is None:
                assert self.context.state == "home"
                self.context.goals.pop()
                return "Canceled! What do you want to do now?"
            else:
                previous.todos.pop()
                return f"Canceled! {previous.message}"

    def handle_question(self, message):
        """Check if message is a question and answer if it is"""
        if QuestionAnswer.is_question(message):
            logger.debug(f"Answering a potential question: {message}")
            answer = self.qa.answer(message)
            if answer is not None:
                logger.debug(f"Question can be answered with: {answer}")
                return answer

    def handle_parse(self, message, isUnconstrained):
        """Parses the message"""
        try:
            if isUnconstrained:
                goal = self.rasa.parse_message(message)
                if goal is None:
                    goal = self.nlu.parse_message(message)
            else:
                goal = self.nlu.parse_message(message)
            self.context.parsed = goal
        except InvalidStateError as e:
            response = "I can't do this right now"
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
        """
        Advances and updates the context based on the current received message
        """
        if self.current_goal() is None:
            # If a current goal does not exist at the moment current message is received
            goal = self.context.parsed
            if goal is None or not isinstance(goal, BaseGoal):
                logger.debug(f"[{self.sid}] Did not understand utterance: {self.context.current_message}")
                response = "I didn't understand what you were saying. Please try again."
            elif goal.error is not None:
                # If parsed goal has an error, respond to client
                response = goal.error
            elif goal.is_complete:
                # If parsed goal can already be completed, complete the goal and respond to client
                response = goal.complete()
            else:
                # Add parsed goal to the current context and respond to client about the goal
                response = goal.message
                self.context.add_goal(goal)
        else:
            # If there is a current goal, advance the current goal
            goal = self.current_goal()
            goal.advance()
            if goal.error is not None:
                # If current goal has an error, remove the goal and respond to client
                response = goal.error
                self.context.goals.pop()
            elif goal.is_complete:
                # If current goal can be completed, complete the goal and respond to client
                response = goal.complete()
                self.context.goals.pop()
            else:
                response = goal.message

        return response

    def handle_train(self, intents):
        """
        Prompts the user to connect or create procedures for each intent that was trained.
        """
        logger.debug(f"[{self.sid}] Finished training the following intents: {intents}.")
        return f"You've finished training the intents: {intents}! Please connect it to the procedure you want to execute when the intent is recognized by saying \"connect the intent [intent name] to the procedure [procedure name]\"."

class DialogContext(object):
    """
    Contains context and information needed to process messages and maintain conversations

    More specifically, contains the classes, procedures, intents (and entities), state, conversation, goals
    and execution/editing subcontexts for the client
    """
    def __init__(self, sid, rasa_port, procedures={}):
        self.sid = sid
        self.rasa_port = rasa_port
        self.classes = {}
        self.procedures = procedures
        self.execution = None
        self.intents = {} # maps intent name to a list of required entities
        self.intent_to_procedure = {} # maps intent name to a procedure that it is linked to
        self.entities = {} # maps entities to their respective values, if given
        self.reset()

    @property
    def current_message(self):
        """Retrieves the latest message of the conversation"""
        return self.conversation[-1].lower() if self.conversation else None

    @property
    def current_goal(self):
        """Retrives the current top-level goal"""
        return self.goals[-1] if self.goals else None

    def reset(self):
        """Resets the context"""
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

    def add_intent(self, intent, entities):
        self.intents[intent] = entities
        for entity in entities:
            self.entities[entity] = None

    def add_entity(self, entity, value):
        self.entities[entity] = value

    def get_class(self, name):
        return self.classes.get(name)

    def validate_goal(self, goal):
        """Check if goal is allowed in the current state of the context"""
        allowed = any([type(goal) == goaltype or isinstance(goal, goaltype) for goaltype in allowed_goals[self.state]])
        if not allowed:
            raise InvalidStateError(goal, self.state)

    def transition(self, action):
        """Transition state given the action"""
        self.state = state_machine[self.state][str(action)]
