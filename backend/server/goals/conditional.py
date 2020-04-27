from app import logger
from goals import *
from models import *

class ConditionalActionGoal(ActionGoal):
    """Goal for adding a conditional action"""
    def __init__(self, context, condition=None, action=None):
        super().__init__(context)
        self.conditional_actions = [[], []]

        # Todo involve getting actions for both the True and False conditions of the conditional
        self.todos = [GetConditionalActionsGoal(self.context, self.conditional_actions[0], False),
                      GetConditionalActionsGoal(self.context, self.conditional_actions[1], True)]

        # User can provide an initial action to the conditional through the command - if <condition> <action>
        self.setattr("action", action)
        self.setattr("condition", condition)

    def complete(self):
        hasattr(self, "actions")
        self.actions.append(ConditionalAction(self.condition, self.conditional_actions))
        return super().complete()

    def advance(self):
        logger.debug(f"Advancing {self.__class__.__name__}...")
        self._message = None
        if self.todos:
            todo = self.todos.pop()
            if isinstance(todo, GetConditionalActionsGoal) and self.context.current_message == "close":
                self.todos = []
                return

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
            # Add the initial action to the action list that is associated with condition being True
            setattr(value, "actions", self.conditional_actions[1])
            if value.error:
                self.error = value.error
            elif value.is_complete:
                value.complete()
            else:
                self.todos[1].todos.append(value)
            return
        elif (attr == "condition"):
            # If no condition was provided, ask for condition, else set the condition
            if value is None:
                self.todos.append(GetConditionGoal(self.context, self))
            elif value.variable.variable not in self.variables:
                self.error = f"Variable, {value.variable.variable}, used in the condition hasn't been created. Please try again or create the variable first."
            elif isinstance(value.value, ValueOf) and value.value.variable not in self.variables:
                self.error = f"Variable, {value.value.variable}, used in the condition hasn't been created. Please try again or create the variable first."
            elif isinstance(value, ComparisonCondition):
                if isinstance(value.value, str):
                    if value.value in self.variables:
                        value.value = ValueOf(value.value)
                        self.condition = value
                    else:
                        self.error = f"The value {value.value} is not a number, so I cannot compare. Please try again."
                else:
                    self.condition = value
            else:
                self.condition = value
            return
        setattr(self, attr, value)

class GetConditionGoal(BaseGoal):
    """Goal for getting a condition"""
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
        logger.debug(f"Advancing {self.__class__.__name__}...")
        # Check if user actually provided a condition recognized by the NLU
        parsed = self.context.parsed
        if parsed and isinstance(parsed, Condition):
            self.condition = parsed
            self._message = None
        else:
            self.error = "This doesn't seem like a valid condition to me, so I didn't add it. Please try again or add another action."

    def complete(self):
        self.obj.setattr("condition", self.condition)
        return super().complete()
