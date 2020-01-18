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
        if attr == "name":
            if value is None:
                self.todos.append(GetInputGoal(self.context, self, attr, f"What do you want to call the variable?"))
            else:
                self.name = value
            return
        elif attr == "value":
            if value is None:
                self.todos.append(GetInputGoal(self.context, self, attr, f"What should be the initial value?"))
            else:
                self.value = float(value) if value.isnumeric() else value
            return
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
        if attr == "name":
            if value is None:
                self.todos.append(GetInputGoal(self.context, self, attr, f"What variable do you want to set?"))
            else:
                self.name = value
            return
        elif attr == "value":
            if value is None:
                self.todos.append(GetInputGoal(self.context, self, attr, f"What value do you want to set the variable to?"))
            else:
                self.value = float(value) if value.isnumeric() else value
            return
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
        if attr == "name":
            if value is None:
                self.todos.append(GetInputGoal(self.context, self, attr, f"What variable do you want to increment?"))
            else:
                self.name = value
            return
        elif attr == "value":
            if value is None:
                self.todos.append(GetInputGoal(self.context, self, attr, f"What value do you want to set the variable to?"))
            elif not value.isnumeric():
                self.todos.append(GetInputGoal(self.context, self, attr, f"Not a number. Try again."))
            else:
                self.value = float(value)
            return
