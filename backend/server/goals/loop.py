from app import logger
from goals import *
from models import *

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
        logger.debug(f"Advancing {self.__class__.__name__}...")
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
                self.todos[0].todos.append(value)
            return
        elif attr == "condition":
            if value is None:
                self.todos.append(GetConditionGoal(self.context, self))
            elif value.variable.variable not in self.variables:
                self.error = f"Variable {value.variable.variable} used in the condition hasn't been created yet. Please try again or create the variable first."
            elif isinstance(value.value, ValueOf) and value.value.variable not in self.variables:
                self.error = f"Variable {value.value.variable} used in the condition hasn't been created yet. Please try again or create the variable first."
            elif isinstance(value, ComparisonCondition) and isinstance(value.value, str):
                self.error = f"The value {value} is not a number, so I cannot compare. Please try again."
            else:
                self.condition = value
            return
        elif attr == "loop":
            assert value is not None
            self.loop = value
            return
        setattr(self, attr, value)
