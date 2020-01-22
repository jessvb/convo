from goals import *
from models import *
from word2number import w2n

class LoopActionGoal(BaseGoal):
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
            elif value.value.isnumeric():
                num = float(value.value)
                value.value = int(num) if num.is_integer() else num
                self.condition = value
            else:
                try:
                    value.value = w2n.word_to_num(value.value)
                    self.condition = value
                except ValueError as e:
                    self.todos.append(GetConditionGoal(self.context, self, "The value is not a number. Try again."))
            return
        setattr(self, attr, value)

class UntilLoopActionGoal(LoopActionGoal):
    def __init__(self, context, condition=None, action=None):
        super().__init__(context, condition, action)

class WhileLoopActionGoal(LoopActionGoal):
    def __init__(self, context, condition=None, action=None):
        super().__init__(context, condition, action)
