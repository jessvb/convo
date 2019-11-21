from goals import *
from models import *

class GetActionsGoal(BaseGoal):
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
            return f"{self.__class__.__name__} completed!"

        if len(self.todos) == 0:
            return "Added action! Do you want to do anything else?" if len(self.actions) > 0 else "What do you want to do first?"
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

class GetProcedureActionsGoal(GetActionsGoal):
    @property
    def message(self):
        if self.error:
            return self.error

        if self.is_complete:
            return f"{self.__class__.__name__} completed!"

        if len(self.todos) == 0:
            return "Added action to procedure! What's next?" if len(self.actions) > 0 else "What do you want to do first?"
        else:
            return self.todos[-1].message
