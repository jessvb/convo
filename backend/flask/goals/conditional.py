from goals import *
from models import *

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
        elif (attr == "condition") and value is None:
            self.todos.append(GetConditionGoal(self.context, self))
        setattr(self, attr, value)

class GetConditionGoal(BaseGoal):
    def __init__(self, context, obj):
        super().__init__(context)
        self.obj = obj
        self.condition = None

    @property
    def is_complete(self):
        return self.condition is not None

    @property
    def message(self):
        if self.error:
            return self.error

        return "GetConditionGoal completed!" if self.is_complete else "What's the condition?"

    def advance(self):
        print(f"Advancing {self.__class__.__name__}...")
        parsed = self.context.parsed
        if parsed and isinstance(parsed, Condition):
            self.condition = parsed
            self.error = None
        else:
            self.error = "Not a condition. Try again."

    def complete(self):
        self.obj.setattr("condition", self.condition)
        return super().complete()

class GetConditionalActionsGoal(GetActionsGoal):
    def __init__(self, context, actions, condition):
        super().__init__(context, actions)
        self.condition = condition

    @property
    def message(self):
        if self.error:
            return self.error

        if self.is_complete:
            return f"{self.__class__.__name__} completed!"

        if len(self.todos) == 0:
            if len(self.actions) > 0:
                return "Added action to conditional! What's next?"
            elif self.condition:
                return f"What do you want to do first if the condition is true?"
            else:
                return "Would you like to do anything if condition is false? If so, what would you like to do first?"
        else:
            return self.todos[-1].message
