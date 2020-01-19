import logging
from goals import *

class GetInputGoal(BaseGoal):
    def __init__(self, context, obj, attr, message):
        super().__init__(context)
        self.obj = obj
        self.input = attr
        self.value = None
        self._message = message

    @property
    def is_complete(self):
        return self.value is not None

    @property
    def message(self):
        return "GetInputGoal completed!" if self.is_complete else self._message

    def advance(self):
        logging.debug(f"Advancing {self.__class__.__name__}...")
        self.value = self.context.current_message

    def complete(self):
        self.obj.setattr(self.input, self.value)
        return super().complete()

class GetUserInputGoal(BaseGoal):
    def __init__(self, context, variable):
        super().__init__(context)
        self.variable = variable
        self.value = None
    
    @property
    def is_complete(self):
        return self.value is not None

    @property
    def message(self):
        return "GetUserInputGoal completed!" if self.is_complete else ""

    def advance(self):
        logging.debug(f"Advancing {self.__class__.__name__}...")
        self.value = self.context.current_message

    def complete(self):
        self.context.execution.variables[self.variable] = self.value
        return super().complete()
