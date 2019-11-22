from models import *
from goals import *

class CreateVariableActionGoal(BaseGoal):
    def __init__(self, context, name=None, value=None):
        super().__init__(context)
        self.setattr("value", value)
        self.setattr("name", name)

    def complete(self):
        assert hasattr(self, "actions")
        self.actions.append(CreateVariableAction(self.name, self.value))
        return super().complete()

    def setattr(self, attr, value):
        if attr == "name" and value is None:
            self.todos.append(GetInputGoal(self.context, self, attr, f"What do you want to call the variable?"))
        elif attr == "value" and value is None:
            self.todos.append(GetInputGoal(self.context, self, attr, f"What should be the initial value?"))
        setattr(self, attr, value)

class SetVariableActionGoal(BaseGoal):
    def __init__(self, context, name=None, value=None):
        super().__init__(context)
        self.setattr("value", value)
        self.setattr("name", name)

    def complete(self):
        assert hasattr(self, "actions")
        self.actions.append(SetVariableAction(self.name, self.value))
        return super().complete()

    def setattr(self, attr, value):
        if attr == "name" and value is None:
            self.todos.append(GetInputGoal(self.context, self, attr, f"What variable do you want to set?"))
        elif attr == "value" and value is None:
            self.todos.append(GetInputGoal(self.context, self, attr, f"What value do you want to set the variable to?"))
        setattr(self, attr, value)

class IncrementVariableActionGoal(BaseGoal):
    def __init__(self, context, name=None, value=None):
        super().__init__(context)
        self.setattr("value", value)
        self.setattr("name", name)

    def complete(self):
        assert hasattr(self, "actions")
        self.actions.append(IncrementVariableAction(self.name, self.value))
        return super().complete()

    def setattr(self, attr, value):
        if attr == "name" and value is None:
            self.todos.append(GetInputGoal(self.context, self, attr, f"What variable do you want to increment?"))
        elif attr == "value" and value is None:
            self.todos.append(GetInputGoal(self.context, self, attr, f"How much do you want to add?"))
        setattr(self, attr, value)
