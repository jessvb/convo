from models import *
from goals import *

class SayActionGoal(ActionGoal):
    def __init__(self, context, phrase=None):
        super().__init__(context)
        self.setattr("phrase", phrase)

    def complete(self):
        assert hasattr(self, "actions")
        self.actions.append(SayAction(self.phrase))
        return super().complete()

    def setattr(self, attr, value):
        if attr == "phrase":
            if value is None:
                self.todos.append(GetInputGoal(self.context, self, attr, f"What do you want me to say?"))
            elif isinstance(value, ValueOf):
                if value.variable not in self.variables:
                    self.todos.append(GetInputGoal(self.context, self, attr, f"Variable {value.variable} does not exist. Try another variable or phrase."))
        setattr(self, attr, value)
