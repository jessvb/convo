import logging
import re
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

        if self._message:
            return self._message

        if self.is_complete:
            return f"{self.__class__.__name__} completed!"

        if len(self.todos) == 0:
            return "Added action! Do you want to do anything else in the procedure?" \
                if len(self.actions) > 0 \
                    else "What do you want to happen in the procedure first? You could make me say something. See the sidebar for more options."
        else:
            return self.todos[-1].message

    def advance(self):
        if self.todos:
            super().advance()
            return

        logging.debug(f"Advancing {self.__class__.__name__}...")
        self._message = None
        if self.context.current_message in ["done", "nothing", "no"]:
            self.done = True
        elif not isinstance(self.context.parsed, BaseGoal):
            self._message = "I didn't quite catch that. What action did you want me to add?"
        elif self.context.parsed.error:
            self._message = self.context.parsed.error
        elif self.context.parsed._message:
            self._message = self.context.parsed._message
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

        if self._message:
            return self._message

        if self.is_complete:
            return f"{self.__class__.__name__} completed!"

        if len(self.todos) == 0:
            if self.condition:
                if len(self.actions) > 0:
                    return "Added action to whenever the condition is true. Anything else? You can say 'done' if you are finished."
                else:
                    return "What do you want to do first if the condition is true?"
            else:
                if len(self.actions) > 0:
                    return "Added action to whenever the condition is false. Anything else? You can say 'done' if you are finished."
                else:
                    return "Would you like to do anything if condition is false? If so, what would you like to do first?"
        else:
            return self.todos[-1].message

class GetLoopActionsGoal(GetActionsGoal):
    @property
    def message(self):
        if self.error:
            return self.error

        if self._message:
            return self._message

        if self.is_complete:
            return f"{self.__class__.__name__} completed!"

        if len(self.todos) == 0:
            if len(self.actions) == 0:
                return "What do you want to do first in the loop?"
            elif len(self.actions) == 1:
                return "Added action! Do you want to do anything else in the loop? If yes, what's next? If no, say \"close loop\"."
            else:
                return "Added action! Do you want to do anything else in the loop?"
        else:
            return self.todos[-1].message

    def advance(self):
        if self.todos:
            super().advance()
            return

        logging.debug(f"Advancing {self.__class__.__name__}...")
        self._message = None
        if self.context.current_message in ["close loop"]:
            self.done = True
        elif not isinstance(self.context.parsed, BaseGoal):
            self._message = "I didn't quite catch that. What action did you want me to add?"
        elif self.context.parsed.error is not None:
            self._message = self.context.parsed.error
        elif self.context.parsed._message is not None:
            self._message = self.context.parsed._message
        else:
            action = self.context.parsed
            setattr(action, "actions", self.actions)
            if action.is_complete:
                action.complete()
            else:
                self.todos.append(action)

class GetProcedureActionsGoal(GetActionsGoal):
    @property
    def message(self):
        if self.error:
            return self.error

        if self._message:
            return self._message

        if self.is_complete:
            return f"{self.__class__.__name__} completed!"

        if len(self.todos) == 0:
            return "Added action! Do you want to do anything else?" \
                if len(self.actions) > 0 \
                    else "What do you want to happen in the procedure first? You could make me say something. See the sidebar for more options."
        else:
            return self.todos[-1].message
