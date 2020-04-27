import re
from app import logger
from goals import *
from models import *
from db_manage import add_or_update_procedure

class GetActionsGoal(BaseGoal):
    """Agent goal to get actions from user"""
    def __init__(self, context, actions):
        super().__init__(context)
        self.done = False

        # The list that actions should be added to when associated goal is completed
        self.actions = actions

    @property
    def is_complete(self):
        return self.done and super().is_complete

    @property
    def message(self):
        if self.error is not None:
            return self.error

        if self._message is not None:
            return self._message

        if len(self.todos) == 0:
            if len(self.actions) > 0:
                return "Do you want to do anything else in the procedure?"
            else:
                return "What do you want to happen first in the procedure? You could make me say something. See the sidebar for more options."
        else:
            return self.todos[-1].message

    def advance(self):
        if self.todos:
            super().advance()
            return

        logger.debug(f"Advancing {self.__class__.__name__}...")
        self._message = None
        if self.context.current_message in ["done", "nothing", "no"]:
            # Check if user indicated that they are done with adding actions
            self.done = True
        elif not isinstance(self.context.parsed, BaseGoal):
            self._message = "I didn't quite catch that. What action did you want me to add?"
        elif self.context.parsed.error:
            self._message = self.context.parsed.error
        elif self.context.parsed._message:
            self._message = self.context.parsed._message
        else:
            action = self.context.parsed

            # Set the property "actions" for the ActionGoal so the ActionGoal can add its corresponding Action to the list
            setattr(action, "actions", self.actions)
            if action.is_complete:
                action.complete()
                self._message = "Added action to the procedure! Do you want to do anything else?"
            else:
                self.todos.append(action)

class GetConditionalActionsGoal(GetActionsGoal):
    """Agent goal to get actions that are in a conditional from user"""
    def __init__(self, context, actions, condition):
        super().__init__(context, actions)

        # Either True or False, meaning which part of the conditional is the actions in
        self.condition = condition

    @property
    def message(self):
        if self.error is not None:
            return self.error

        if self._message is not None:
            return self._message

        if self.is_complete:
            return f"{self.__class__.__name__} completed!"

        if len(self.todos) == 0:
            if self.condition:
                if len(self.actions) > 0:
                    return """
                        Anything else if condition is true?
                        You can say 'done' to move on to adding actions if the condition is false.
                        You can say 'close' if you are entirely finished.
                    """
                else:
                    return "What do you want to do first if the condition is true?"
            else:
                if len(self.actions) > 0:
                    return "Anything else if condition is false? You can say 'done' if you are finished."
                else:
                    return "Would you like to do anything if condition is false? If so, what would you like to do first?"
        else:
            return self.todos[-1].message

    def advance(self):
        if self.todos:
            super().advance()
            return

        logger.debug(f"Advancing {self.__class__.__name__}...")
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
                condition_phrase = "true" if self.condition else "false"
                self._message = f"Added action to whenever the condition is {condition_phrase}. Anything else? You can say 'done' if you are finished."
            else:
                self.todos.append(action)

class GetLoopActionsGoal(GetActionsGoal):
    """Agent goal to get actions that are in a loop from user"""
    @property
    def message(self):
        if self.error is not None:
            return self.error

        if self._message is not None:
            return self._message

        if self.is_complete:
            return f"{self.__class__.__name__} completed!"

        if len(self.todos) == 0:
            if len(self.actions) == 0:
                return "What do you want to do first in the loop?"
            elif len(self.actions) == 1:
                return "Anything else in the loop? If yes, what's next? If no, say \"close loop\"."
            else:
                return "Anything else in the loop? If no, say \"close loop\"."
        return self.todos[-1].message

    def advance(self):
        if self.todos:
            super().advance()
            return

        logger.debug(f"Advancing {self.__class__.__name__}...")
        self._message = None
        if self.context.current_message in ["close loop", "no", "done", "closed loop", "close the loop"]:
            self.done = True
        elif re.match("close.{1,6}loop", self.context.current_message):
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
                if len(self.actions) == 1:
                    return "Added action to the loop! Anything else? If yes, what's next? If no, say \"close loop\"."
                else:
                    return "Added action to the loop! Anything else? If no, say \"close loop\"."
            else:
                self.todos.append(action)

class GetProcedureActionsGoal(GetActionsGoal):
    """Agent goal to get actions for procedure from user"""
    def __init__(self, context, procedure):
        super().__init__(context, procedure.actions)

        # The procedure that actions are being added to
        self.procedure = procedure

    @property
    def message(self):
        if self.error is not None:
            return self.error

        if self._message is not None:
            return self._message

        if self.is_complete:
            return f"I finished creating the procedure. You can say, \"run {self.procedure.name}\" to play it."

        if len(self.todos) == 0:
            if len(self.actions) > 0:
                return "Do you want to do anything else in the procedure?"
            else:
                return "What do you want to do first in the procedure? You could make me say something. See the sidebar for more options."
        else:
            return self.todos[-1].message

    def complete(self):
        """
        Completes the goal

        Completion of this goal involves:
        1. Transition from "creating" state to "home" state
        2. Setting current back to None
        """
        add_or_update_procedure(self.context.sid, self.procedure)

        self.context.current = None
        self.context.transition("complete")
        logger.debug(f"Procedure: {[str(a) for a in self.procedure.actions]}")
        return super().complete()

    def cancel(self):
        self.context.transition("complete")
        self.context.current = None
