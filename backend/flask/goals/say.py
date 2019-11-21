from models import *
from goals import *

class SayActionGoal(BaseGoal):
    def __init__(self, context, phrase=None):
        super().__init__(context)
        self.setattr("phrase", phrase)

    def complete(self):
        assert hasattr(self, "actions")
        self.actions.append(SayAction(self.phrase))
        return super().complete()

    def setattr(self, attr, value):
        if attr == "phrase" and value is None:
            self.todos.append(GetInputGoal(self.context, self, attr, f"What do you want me to say?"))
        setattr(self, attr, value)
