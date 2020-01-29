import logging
from goals import *
from models import *
from word2number import w2n

class ConditionalActionGoal(ActionGoal):
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
        self._message = "Added the sets of conditional actions. Do you want to do anything else?"
        return super().complete()

    def advance(self):
        logging.debug(f"Advancing {self.__class__.__name__}...")
        self._message = None
        if self.todos:
            todo = self.todos.pop()
            todo.advance()
            if todo.error:
                if isinstance(todo, GetConditionGoal):
                    self.error = todo.error
                else:
                    self._message = todo.error
                return

            if todo.is_complete:
                todo.complete()
            else:
                self.todos.append(todo)

    def setattr(self, attr, value):
        if (attr == "action") and value:
            setattr(value, "actions", self.conditional_actions[1])
            if value.error:
                self.error = value.error
            elif value.is_complete:
                value.complete()
            else:
                self.todos[1].todos.append(value)
            return
        elif (attr == "condition"):
            if value is None:
                self.todos.append(GetConditionGoal(self.context, self))
            elif value.variable not in self.variables:
                self.error = f"Variable {value.variable} used in the condition does not exist. Please try again or create the variable first."
            elif value.value.isnumeric():
                num = float(value.value)
                value.value = int(num) if num.is_integer() else num
                self.condition = value
            else:
                try:
                    value.value = w2n.word_to_num(value.value)
                    self.condition = value
                except ValueError as e:
                    if isinstance(value, EqualityCondition):
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
        if self.error:
            return self.error

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
            self.error = "This is not a valid condition, so the action is canceled. Try again or add another action."

    def complete(self):
        self.obj.setattr("condition", self.condition)
        return super().complete()
