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

transitions = {
    "home": {
        "edit_class": "class",
        "create_class": "class",
        "create_procedure": "actions",
        "create_class_procedure": "class_actions",
        "run": "execution",
        "edit": "editing"
    },
    "class_actions": {
        "complete": "home"
    },
    "edit_actions": {
        "complete": "editing"
    },
    "actions": {
        "complete": "home"
    },
    "class": {
        "complete": "home"
    },
    "execution": {
        "complete": "home"
    },
    "editing": {
        "complete": "home",
        "add_step": "edit_actions"
    }
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
            if isinstance(self.context.parsed, BaseGoal):
                self.context.validate_goal(self.context.parsed)
        except InvalidStateError as e:
            logging.warning(e.message)
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
        self.procedures = { "example": example_procedure }
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
        if self.state == "home":
            if isinstance(goal, CreateClassGoal):
                self.transition("create_class")
            elif isinstance(goal, AddClassProcedureGoal):
                self.transition("create_class_procedure")
            elif isinstance(goal, AddProcedureGoal):
                self.transition("create_procedure")
            elif isinstance(goal, AddPropertyGoal):
                self.transition("edit_class")
            elif isinstance(goal, RunGoal):
                self.transition("run")
            elif isinstance(goal, EditGoal):
                self.transition("edit")
            else:
                raise InvalidStateError(self.state, str(goal))
        elif self.state in ["actions", "class_actions"]:
            if isinstance(goal, CreateClassGoal) \
                or isinstance(goal, AddClassProcedureGoal) \
                or isinstance(goal, AddProcedureGoal) \
                or isinstance(goal, AddPropertyGoal):
                raise InvalidStateError(self.state, str(goal))
        elif self.state == "edit_actions":
            if isinstance(goal, AddStepGoal) \
                or isinstance(goal, DeleteStepGoal) \
                or isinstance(goal, GoToStepGoal):
                raise InvalidStateError(self.state, str(goal))
        elif self.state in ["editing"]:
            if isinstance(goal, AddStepGoal):
                self.transition("add_step")
        elif self.state == "class":
            raise InvalidStateError(self.state, str(goal))

    def transition(self, action):
        actions = transitions[self.state]
        if action not in actions:
            raise InvalidStateError(self.state, str(action))

        self.state = actions[action]
