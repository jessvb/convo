from models import *
from goals import *

class GreetActionGoal(ActionGoal):
    """Goal for adding a greet action"""
    def __init__(self, context):
        super().__init__(context)
        # self.setattr("phrase", phrase) <- don't need to set attribute, because
        # there are no attributes (see say.py for an example with a greet attr)

    def complete(self):
        assert hasattr(self, "actions")
        self.actions.append(GreetAction())
        return super().complete()

    # def setattr(self, attr, value):
        # don't need to set any attr, so leave this blank in this case
