from goals import *
from models import *

class LoopActionGoal(BaseGoal):
    def __init__(self, context, condition=None, action=None):
        super().__init__(context)
        self.loop_actions = []
        self.todos = [GetLoopActionsGoal(self.context, self.loop_actions)]
        self.setattr("action", action)
        self.setattr("condition", condition)

    def complete(self):
        hasattr(self, "actions")
        self.actions.append(LoopAction(self.condition, self.loop_actions))
        return super().complete()

    def setattr(self, attr, value):
        if (attr == "action") and value:
            setattr(value, "actions", self.loop_actions)
            if value.is_complete:
                value.complete()
            else:
                self.todos[0].append(value)
            return
        elif (attr == "condition") and value is None:
            self.todos.append(GetConditionGoal(self.context, self))
        setattr(self, attr, value)

class GetLoopActionsGoal(GetActionsGoal):
    @property
    def message(self):
        if self.error:
            return self.error

        if self.is_complete:
            return f"{self.__class__.__name__} completed!"

        if len(self.todos) == 0:
            if len(self.actions) > 0:
                return "Added action! Do you want to do anything else in the loop? If yes, what's next? If no, say done."
            else:
                return "What do you want to do first in the loop?"
        else:
            return self.todos[-1].message
