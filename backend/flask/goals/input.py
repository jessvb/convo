import logging
from goals import *
from models import *
from word2number import w2n

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
        if isinstance(self.context.parsed, ValueOf):
            self.value = self.context.parsed
        else:
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

        if isinstance(self.context.parsed, ValueOf):
            self.value = self.context.parsed
        else:
            message = self.context.current_message
            if message.isnumeric():
                num = float(message)
                self.value = int(message) if num.is_integer() else num
            else:
                try:
                    self.value = w2n.word_to_num(message)
                except ValueError as e:
                    self.value = message

    def complete(self):
        variables = self.context.execution.variables
        variables[self.variable] = variables[self.value.variable] if isinstance(self.value, ValueOf) else self.value
        return super().complete()

class GetUserInputActionGoal(ActionGoal):
    def __init__(self, context, variable):
        super().__init__(context)
        self.variables = self.procedure.variables
        self.setattr("variable", variable)

    def complete(self):
        assert hasattr(self, "actions")
        self.actions.append(GetUserInputAction(self.variable))
        self.variables.add(self.variable)
        return super().complete()

    def setattr(self, attr, value):
        if attr == "variable":
            if value is None:
                self.todos.append(GetInputGoal(self.context, self, attr, f"What name do you want to give this variable?"))
            else:
                self.variable = value
            return
        setattr(self, attr, value)
