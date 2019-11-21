from nlu import SemanticNLU
from models import *

class DialogManager(object):
    def __init__(self):
        self.context = DialogContext()
        self.nlu = SemanticNLU(self.context)

    def reset(self):
        self.context.reset()
        return "Reset"

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

        parsed = self.nlu.parse_message(message)
        self.context.parsed = parsed
        if self.current_goal() is None:
            if parsed is None:
                response = "I didn't understand what you were saying. Please try again."
            else:
                self.context.add_goal(parsed)
                response = self.current_goal().try_complete() if parsed.is_complete else self.current_goal().message
        else:
            response = self.current_goal().try_complete()

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
        self.cached = None
        example = Class("example")
        example.add_property(Property(example, "count", "number"))
        self.classes = { "example": example }
        self.parsed = None

    def add_message(self, message):
        self.conversation.append(message)

    def add_goal(self, goal):
        self.goals.append(goal)

    def add_class(self, klass):
        self.classes[klass.name] = klass
        self.cached = klass

    def get_class(self, name):
        return self.classes.get(name)
