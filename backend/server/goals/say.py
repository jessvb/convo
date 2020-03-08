from models import *
from goals import *

class SayActionGoal(ActionGoal):
    """Goal for adding a say action"""
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
                    self.error = f"Variable, {value.variable}, hasn't been created. Try using an existing variable if you want to try again."
                    return
                self.phrase = value
            else:
                self.phrase = value
            return
        setattr(self, attr, value)
