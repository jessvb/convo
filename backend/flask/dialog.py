import logging
from nlu import SemanticNLU
from models import *
from goals import *
from error import *

example_procedure = Procedure(name="example", actions=[
    CreateVariableAction("foo", 4),
    SayAction("I want to get your input."),
    GetUserInputAction("input"),
    CreateListAction("groceries"),
    SetVariableAction("foo", 6),
    IncrementVariableAction("foo", 5),
    SayAction("hello world!"),
    ConditionalAction(
        ComparisonCondition("foo", "greater than", 10),
        actions=[
            [SayAction("foo is not greater than 10"), CreateVariableAction("bar", 10)],
            [SayAction("foo is greater than 10"), CreateVariableAction("bar", 4), SayAction("random")]
        ]
    ),
    UntilLoopAction(
        ComparisonCondition("bar", "less than", 15),
        actions=[
            SayAction("bar is less than 15"),
            IncrementVariableAction("bar", 1)
        ]
    ),
    AddToListAction("groceries", "\"apples\"")
])

sounds_procedure = Procedure(name="dog or cat", actions=[
    SayAction("Do you want to hear a dog or a cat?"),
    GetUserInputAction("input"),
    ConditionalAction(
        ComparisonCondition("input", "equal to", "dog"),
        actions=[
            [ConditionalAction(
                ComparisonCondition("input", "equal to", "cat"),
                actions=[
                    [SayAction("You did not say a dog or a cat.")],
                    [PlaySoundAction("meow")]
                ]
            )],
            [PlaySoundAction("bark")]
        ]
    )
])

state_machine = {
    "home": {
        "add_procedure": "creating",
        "run": "executing",
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
        "complete": "home"
    },
    "editing_action": {
        "complete": "editing"
    }
}

allowed_goals = {
    "home": [HomeGoal, EditGoal, RunGoal],
    "creating": [ActionGoal, GetActionsGoal, GetConditionGoal, GetInputGoal],
    "editing": [StepGoal, GetInputGoal],
    "editing_action": [ActionGoal, GetActionsGoal, GetConditionGoal, GetInputGoal],
    "executing": [GetUserInputGoal, GetInputGoal]
}

class DialogManager(object):
    def __init__(self, sid):
        self.sid = sid
        self.context = DialogContext(sid)
        self.nlu = SemanticNLU(self.context)

    def reset(self):
        self.context.reset()
        return "Conversation has been reset. What do you want to do first?"

    def current_goal(self):
        return self.context.current_goal

    def handle_message(self, message):
        self.context.add_message(message)

        # Check for interrupts
        if (message == "reset"):
            return self.reset()
        elif (message == "cancel"):
            if self.context.goals:
                self.context.goals.pop()
            self.context.state = "home"
            return "Canceled! What do you want to do?"

        try:
            self.context.parsed = self.nlu.parse_message(message)
        except InvalidStateError as e:
            logging.error(e.message)
            base = "I cannot do this right now."
            if (self.context.state == "home"):
                return base + " Try 'create a procedure' or 'create a class'."
            response = base + (f" {self.current_goal().message}" if self.current_goal() else "")
            if response:
                self.context.add_message(response)
            return response

        if self.current_goal() is None:
            goal = self.context.parsed
            if goal is None or not isinstance(goal, BaseGoal):
                response = "I didn't understand what you were saying. Please try again."
            elif goal.error:
                response = goal.error
            else:
                if goal.is_complete:
                    response = goal.complete()
                else:
                    response = goal.message
                    self.context.add_goal(goal)
        else:
            goal = self.current_goal()
            goal.advance()
            if goal.is_complete:
                response = goal.complete()
                self.context.goals.pop()
            elif goal.error:
                response = goal.error
                self.context.goals.pop()
            else:
                response = goal.message

        if response:
            self.context.add_message(response)
        return response

class DialogContext(object):
    def __init__(self, sid):
        example = Class("example")
        example.add_property(Property(example, "count", "number"))
        self.sid = sid
        self.classes = { "example": example }
        self.procedures = { "example": example_procedure, "dog or cat": sounds_procedure }
        self.reset()

    @property
    def current_message(self):
        return self.conversation[-1] if self.conversation else None

    @property
    def current_goal(self):
        return self.goals[-1] if self.goals else None

    def reset(self):
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
            raise InvalidStateError(f"Cannot create goal {str(goal)} in state {self.state}")

    def transition(self, action):
        self.state = state_machine[self.state][str(action)]
