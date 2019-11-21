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
