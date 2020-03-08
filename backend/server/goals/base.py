import re
from app import logger
from helpers import to_snake_case
from models import *

class BaseGoal(object):
    def __init__(self, context):
        # Contains subgoals needed to completed before
        # this goal is deemed complete
        self.todos = []

        # Error message if goal encounters an error
        # Usually leads to cancellation or removal of goal
        self.error = None

        # Any message (information or warning) that will be shown to user
        # Usually does not lead to cancellation or removal
        self._message = None

        # Dialog context to retrieve information like procedures and classes
        self.context = context

        # Check if goal is valid in the current state
        self.context.validate_goal(self)
        logger.debug(f"Creating {self.__class__.__name__}...")

    @property
    def is_complete(self):
        """Checks if goal can be completed"""
        return len(self.todos) == 0 and self._message is None and self.error is None

    @property
    def message(self):
        """Message returned to the user"""
        if self.error is not None:
            return self.error

        if self._message is not None:
            return self._message

        return f"{self.__class__.__name__} completed!" if self.is_complete else self.todos[-1].message

    def advance(self):
        """Advances the goal towards completion"""
        logger.debug(f"Advancing {self.__class__.__name__}...")
        self._message = None
        if self.todos:
            # Check for subgoals
            todo = self.todos.pop()
            # Advances the top subgoal
            todo.advance()
            # If error in subgoal, save it to _message so user can see
            if todo.error:
                self._message = todo.error
                return

            if todo.is_complete:
                # If subgoal can be completed, complete the goal
                todo.complete()
            else:
                # If not, add it back to todos
                self.todos.append(todo)

    def complete(self):
        """Complete the goal by performing the last set of actions needed"""
        logger.debug(f"{self.__class__.__name__} completed!")
        return self.message

    def setattr(self, attr, value):
        """
        Slot fills any necessary values

        This is usually where goals implement slot-filling such that if any value
        is not present in the form of a None, this is where a GetInputGoal can be created
        and added to the todos
        """
        setattr(self, attr, value)

    def cancel(self):
        """Perform any actions that are needed for cancelling this goal"""
        return

    def __str__(self):
        name = self.__class__.__name__
        return to_snake_case(name[:-len("Goal")]) + (f":{str(self.todos[-1])}" if self.todos else "")

class HomeGoal(BaseGoal):
    """Base goal class for goals that can be done in the home state"""
    def __init__(self, context):
        super().__init__(context)

class ActionGoal(BaseGoal):
    """Base goal class for goals that involve adding actions to procedures"""
    def __init__(self, context):
        super().__init__(context)
        assert isinstance(self.context.current, Procedure)
        self.procedure = self.context.current
        self.variables = self.procedure.variables

    @property
    def message(self):
        if self.error:
            return self.error

        if self._message:
            return self._message

        return f"Added action!" if self.is_complete else self.todos[-1].message

class StepGoal(BaseGoal):
    """Base goal class for goals relating to editing steps"""
    def __init__(self, context):
        super().__init__(context)
        self.edit = self.context.edit
        self.current_edit = self.context.edit[-1]
        self.scope = self.current_edit.scope
