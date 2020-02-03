import logging
from nlu import SemanticNLU
from question import QuestionAnswer
from models import *
from goals import *
from error import *
from helpers import *

example_procedure = Procedure(name="example", actions=[
    CreateVariableAction("foo", 4),
    SayAction("I want to get your input."),
    GetUserInputAction("input"),
    CreateListAction("groceries"),
    SetVariableAction("foo", 6),
    AddToVariableAction("foo", 5),
    SayAction("hello world!"),
    ConditionalAction(
        ComparisonCondition("foo", "greater than", 10),
        actions=[
            [SayAction("foo is not greater than 10"), CreateVariableAction("bar", 10)],
            [SayAction("foo is greater than 10"), CreateVariableAction("bar", 4), SayAction("random")]
        ]
    ),
    LoopAction(
        loop="until",
        condition=ComparisonCondition("bar", "less than", 15),
        actions=[
            SayAction("bar is less than 15"),
            AddToVariableAction("bar", 1)
        ]
    ),
    AddToListAction("groceries", "\"apples\"")
])

sounds_procedure = Procedure(name="dog or cat", actions=[
    SayAction("Do you want to hear a dog or a cat?"),
    GetUserInputAction("input"),
    ConditionalAction(
        EqualityCondition("input", "dog"),
        actions=[
            [ConditionalAction(
                EqualityCondition("input", "cat"),
                actions=[
                    [SayAction("You did not say a dog or a cat.")],
                    [PlaySoundAction("meow")]
                ]
            )],
            [PlaySoundAction("bark")]
        ]
    )
])

empty_procedure = Procedure(name="empty", actions=[])

infinite_loop_procedure = Procedure(name="infinite loop", actions=[
    CreateVariableAction("bad var", 0),
    LoopAction(
        loop="while",
        condition=EqualityCondition("bad var", 0),
        actions=[SayAction("in the loop")]
    )
])

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

    def reset(self, context=None):
        if context is not None:
            self.context = context
            self.qa = QuestionAnswer(context)
            self.nlu = SemanticNLU(context)
        else:
            self.context.reset()
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
            return response

        response = self.handle_help(message)
        if response is not None:
            return response

        if self.context.state == "executing":
            return self.handle_execution(message)

        response = self.handle_cancel(message)
        if response is not None:
            return response

        response = self.handle_question(message)
        if response is not None:
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
            logging.error(e.message)
            response = "I cannot do this right now"
            if isinstance(e.goal, ActionGoal):
                response += " because I am currently not creating or editing a procedure"
            elif isinstance(e.goal, StepGoal):
                if e.state == "editing_action":
                    response += " because I am currently adding or editing an action"
                else:
                    response += " because I am currently not editing a procedure"
            elif isinstance(e.goal, HomeGoal):
                if e.state == "creating":
                    response += " because I am currently creating a procedure. You can stop by saying \"done\""
                elif e.state == "editing":
                    response += " because I am currently editing a procedure. You can stop by saying \"done\""
                elif e.state == "editing_action":
                    response += " because I am currently adding or editing an action. Finish editing then you can stop by saying \"done\""
            return f"{response}."

    def handle_goal(self):
        if self.current_goal() is None:
            goal = self.context.parsed
            if goal is None or not isinstance(goal, BaseGoal):
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
        example = Class("example")
        example.add_property(Property(example, "count", "number"))
        self.sid = sid
        self.classes = { "example": example }
        self.procedures = { "example": example_procedure, "dog or cat": sounds_procedure, "empty": empty_procedure, "infinite loop": infinite_loop_procedure }
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
