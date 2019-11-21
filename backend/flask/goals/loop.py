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

class GetLoopActionsGoal(BaseGoal):
    def __init__(self, context, actions):
        super().__init__(context)
        self.done = False
        self.actions = actions

    @property
    def is_complete(self):
        return self.done and super().is_complete

    @property
    def message(self):
        if self.error:
            return self.error

        if self.is_complete:
            return "GetLoopActionsGoal completed!"

        if len(self.todos) == 0:
            if len(self.actions) > 0:
                return "Added action! Do you want to anything else in the loop? If yes, what's next? If no, say done."
            else:
                return f"What do you want to do first in the loop?"
        else:
            return self.todos[-1].message

    def advance(self):
        if self.todos:
            super().advance()
            return

        print(f"Advancing {self.__class__.__name__}...")
        self.error = None

        if self.context.current_message in ["done", "nothing"]:
            self.done = True
        elif self.context.parsed is None:
            self.error = "Couldn't understand the action. Try again."
        else:
            action = self.context.parsed
            setattr(action, "actions", self.actions)
            if action.is_complete:
                action.complete()
            else:
                self.todos.append(action)
