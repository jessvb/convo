from goals import *
from models import *
from word2number import w2n

class LoopActionGoal(ActionGoal):
    def __init__(self, context, loop=None, condition=None, action=None):
        super().__init__(context)
        self.loop_actions = []
        self.todos = [GetLoopActionsGoal(self.context, self.loop_actions)]
        self.setattr("action", action)
        self.setattr("condition", condition)
        self.setattr("loop", loop)

    def complete(self):
        hasattr(self, "actions")
        self.actions.append(LoopAction(self.loop, self.condition, self.loop_actions))
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
        if attr == "action" and value:
            setattr(value, "actions", self.loop_actions)
            if value.error:
                self.error = value.error
            elif value.is_complete:
                value.complete()
            else:
                self.todos[0].actions.append(value)
            return
        elif attr == "condition":
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
        elif attr == "loop":
            assert value is not None
            self.loop = value
            return
        setattr(self, attr, value)
