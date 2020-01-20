from goals import *
from models import *

class UntilLoopActionGoal(BaseGoal):
    def __init__(self, context, condition=None, action=None):
        super().__init__(context)
        self.loop_actions = []
        self.todos = [GetLoopActionsGoal(self.context, self.loop_actions)]
        self.setattr("action", action)
        self.setattr("condition", condition)

    def complete(self):
        hasattr(self, "actions")
        self.actions.append(UntilLoopAction(self.condition, self.loop_actions))
        return super().complete()

    def setattr(self, attr, value):
        if (attr == "action") and value:
            setattr(value, "actions", self.loop_actions)
            if value.is_complete:
                value.complete()
            else:
                self.todos[0].append(value)
            return
        elif (attr == "condition"):
            if value is None:
                self.todos.append(GetConditionGoal(self.context, self))
            elif not value.value.isnumeric():
                self.todos.append(GetConditionGoal(self.context, self, "The value is not a number. Try again."))
            else:
                num = float(value.value)
                value.value = int(num) if num.is_integer() else num
                self.condition = value
            return
        setattr(self, attr, value)
