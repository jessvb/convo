import logging
from goals import *
from models import *
from word2number import w2n

class ConditionalActionGoal(BaseGoal):
    def __init__(self, context, condition=None, action=None):
        super().__init__(context)
        self.conditional_actions = [[], []]
        self.todos = [GetConditionalActionsGoal(self.context, self.conditional_actions[0], False),
                      GetConditionalActionsGoal(self.context, self.conditional_actions[1], True)]
        self.setattr("action", action)
        self.setattr("condition", condition)

    def complete(self):
        hasattr(self, "actions")
        self.actions.append(ConditionalAction(self.condition, self.conditional_actions))
        return super().complete()

    def setattr(self, attr, value):
        if (attr == "action") and value:
            setattr(value, "actions", self.conditional_actions[1])
            if value.is_complete:
                value.complete()
            else:
                self.todos[1].append(value)
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
                    if value.op == "equal to":
                        self.condition = value
                    else:
                        self.todos.append(GetConditionGoal(self.context, self, f"The value {value} is not a number. Try another condition."))
            return
        setattr(self, attr, value)

class GetConditionGoal(BaseGoal):
    def __init__(self, context, obj, message=None):
        super().__init__(context)
        self.obj = obj
        self.condition = None
        self._message = message

    @property
    def is_complete(self):
        return self.condition is not None

    @property
    def message(self):
        if self._message:
            return self._message

        return "GetConditionGoal completed!" if self.is_complete else "What's the condition?"

    def advance(self):
        logging.debug(f"Advancing {self.__class__.__name__}...")
        parsed = self.context.parsed
        if parsed and isinstance(parsed, Condition):
            self.condition = parsed
            self._message = None
        else:
            self._message = "Not a condition. Try again."

    def complete(self):
        self.obj.setattr("condition", self.condition)
        return super().complete()
