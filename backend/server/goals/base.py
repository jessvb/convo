import re
import logging
from helpers import to_snake_case
from models import *

class BaseGoal(object):
    def __init__(self, context):
        self.todos = []
        self.error = None
        self.context = context
        self.context.validate_goal(self)
        self._message = None
        logging.debug(f"Creating {self.__class__.__name__}...")

    @property
    def is_complete(self):
        return len(self.todos) == 0 and self._message is None and self.error is None

    @property
    def message(self):
        if self.error:
            return self.error

        if self._message:
            return self._message

        return f"{self.__class__.__name__} completed!" if self.is_complete else self.todos[-1].message

    def advance(self):
        logging.debug(f"Advancing {self.__class__.__name__}...")
        self._message = None
        if self.todos:
            todo = self.todos.pop()
            todo.advance()
            if todo.error:
                self._message = todo.error
                return

            if todo.is_complete:
                todo.complete()
            else:
                self.todos.append(todo)

    def complete(self):
        logging.debug(f"{self.__class__.__name__} completed!")
        return self.message

    def setattr(self, attr, value):
        setattr(self, attr, value)

    def __str__(self):
        name = self.__class__.__name__
        return to_snake_case(name[:-len("Goal")]) + (f":{str(self.todos[-1])}" if self.todos else "")

class HomeGoal(BaseGoal):
    def __init__(self, context):
        super().__init__(context)

class ActionGoal(BaseGoal):
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
    def __init__(self, context):
        super().__init__(context)
        self.edit = self.context.edit
