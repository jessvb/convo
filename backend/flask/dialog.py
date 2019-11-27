from nlu import SemanticNLU
from models import *

class DialogManager(object):
    def __init__(self):
        self.context = DialogContext()
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
            return "Canceled!"

        self.context.parsed = self.nlu.parse_message(message)
        if self.current_goal() is None:
            goal = self.context.parsed
            if goal is None:
                response = "I didn't understand what you were saying. Please try again."
            else:
                if goal.is_complete:
                    response = goal.complete()
                else:
                    response = goal.message
                    self.context.add_goal(goal)
        else:
            self.current_goal().advance()
            if self.current_goal().is_complete:
                response = self.current_goal().complete()
                self.context.goals.pop()
            else:
                response = self.current_goal().message

        self.context.add_message(response)
        return response

class DialogContext(object):
    def __init__(self):
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
        example = Class("example")
        example.add_property(Property(example, "count", "number"))
        self.classes = { "example": example }
        self.procedures = {}
        self.current = None

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
