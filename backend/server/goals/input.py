from app import logger
from goals import *
from models import *
from helpers import *

class GetInputGoal(BaseGoal):
    """Goal for getting user input"""
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
        logger.debug(f"Advancing {self.__class__.__name__}...")
        if self.context.parsed and isinstance(self.context.parsed, ValueOf):
            self.value = self.context.parsed
        else:
            message = self.context.current_message
            number = parse_number(message)
            self.value = number if number is not None else message

    def complete(self):
        self.obj.setattr(self.input, self.value)
        return super().complete()

class GetUserInputGoal(BaseGoal):
    """Goal for getting user input during execution of a procedure"""
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
        logger.debug(f"Advancing {self.__class__.__name__}...")

        if self.context.parsed and isinstance(self.context.parsed, ValueOf):
            self.value = self.context.parsed
        else:
            message = self.context.current_message
            number = parse_number(message)
            self.value = number if number is not None else message

    def complete(self):
        variables = self.context.execution.variables
        variables[self.variable] = variables[self.value.variable] if isinstance(self.value, ValueOf) else self.value
        return super().complete()

class GetEntityInputGoal(HomeGoal):
    """Goal for getting user entity input during recognition of an intent"""
    def __init__(self, context, intent, entity, message):
        super().__init__(context)
        self.intent = intent
        self.entity = entity
        self._message = message
        self.value = None
        self.procedure = self.context.intent_to_procedure[self.intent]

    @property
    def is_complete(self):
        return self.value is not None

    @property
    def message(self):
        return "GetEntityInputGoal completed!" if self.is_complete else self._message

    def advance(self):
        logger.debug(f"Advancing {self.__class__.__name__}...")

        if self.context.parsed and isinstance(self.context.parsed, ValueOf):
            self.value = self.context.parsed
        else:
            message = self.context.current_message
            number = parse_number(message)
            self.value = number if number is not None else message

    def complete(self):
        logger.debug(self.context.entities)
        self.context.entities[self.entity] = self.context.execution.variables[self.value.variable] if isinstance(self.value, ValueOf) else self.value
        for i in range(len(self.procedure.actions)):
            action = self.procedure.actions[i]
            if type(action) is CreateVariableAction:
                if action.variable == self.entity:
                    # replace this action
                    self.procedure.actions[i] = CreateVariableAction(self.entity, self.context.entities[self.entity])
        return super().complete()

class GetUserInputActionGoal(ActionGoal):
    """Goal for adding action to get user input"""
    def __init__(self, context, variable, prompt=None):
        super().__init__(context)
        self.variables = self.procedure.variables
        self.setattr("variable", variable)
        self.setattr("prompt", prompt)

    def complete(self):
        assert hasattr(self, "actions")
        self.actions.append(GetUserInputAction(self.variable, self.prompt))
        self.variables.add(self.variable)
        return super().complete()

    def setattr(self, attr, value):
        if attr == "variable":
            if value is None:
                self.todos.append(GetInputGoal(self.context, self, attr, f"What variable name do you want to save the input as?"))
            else:
                self.variable = value
            return
        elif attr == "prompt":
            if value is None:
                self.todos.append(GetInputGoal(self.context, self, attr, f"What do you want me to say when asking for input?"))
            else:
                self.prompt = None if value == "nothing" else value
            return
        setattr(self, attr, value)
