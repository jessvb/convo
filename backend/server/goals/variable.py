from models import *
from goals import *
from helpers import *
from app import logger

class CreateVariableActionGoal(ActionGoal):
    """Goal for adding a create variable action"""
    def __init__(self, context, name=None, value=None):
        super().__init__(context)
        self.setattr("value", value)
        self.setattr("name", name)

    def complete(self):
        assert hasattr(self, "actions")
        self.actions.append(CreateVariableAction(self.name, self.value))
        self.variables.add(self.name)
        return super().complete()

    def setattr(self, attr, value):
        if attr == "name":
            if value is None:
                self.todos.append(GetInputGoal(self.context, self, attr, f"What do you want to call the variable?"))
            elif value in self.variables:
                self.error = f"The name, {value}, has already been used. Try creating a variable with another name."
            else:
                self.name = value
            return
        elif attr == "value":
            if value is None:
                self.todos.append(GetInputGoal(self.context, self, attr, f"What should be the initial value?"))
            elif isinstance(value, ValueOf):
                if value.variable not in self.variables:
                    self.error = f"Variable, {value}, hasn't been created yet. Try setting it to the value of an existing variable."
                else:
                    self.value = value
            else:
                self.value = value
            return
        setattr(self, attr, value)

class SetVariableActionGoal(ActionGoal):
    """Goal for adding a set variable action"""
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
            elif value not in self.variables:
                self.error = f"Variable, {value}, hasn't been created, so we can't set it yet. You can create it by saying, \"create a variable called {value}.\""
            else:
                self.name = value
            return
        elif attr == "value":
            if value is None:
                self.todos.append(GetInputGoal(self.context, self, attr, f"What value do you want to set the variable to?"))
            elif isinstance(value, ValueOf):
                if value.variable not in self.variables:
                    self.error = f"Variable, {value}, hasn't been created yet. Try setting it to the value of an existing variable."
                else:
                    self.value = value
            else:
                self.value = value
            return
        setattr(self, attr, value)

class AddToVariableActionGoal(ActionGoal):
    """Goal for adding a add to variable action"""
    def __init__(self, context, name=None, value=None):
        super().__init__(context)
        self.setattr("value", value)
        self.setattr("name", name)

    def complete(self):
        assert hasattr(self, "actions")
        self.actions.append(AddToVariableAction(self.name, self.value))
        return super().complete()

    def setattr(self, attr, value):
        if attr == "name":
            if value is None:
                self.todos.append(GetInputGoal(self.context, self, attr, f"What variable do you want to add to?"))
            elif value not in self.variables:
                self.error = f"The variable, {value}, hasn't been created so there is nothing to add to. Try creating the variable first."
            else:
                self.name = value
            return
        elif attr == "value":
            if value is None:
                self.todos.append(GetInputGoal(self.context, self, attr, f"What value do you want to add to the variable?"))
            elif isinstance(value, ValueOf):
                if value.variable not in self.variables:
                    self.error = f"Variable {value} does not exist. Try setting it to the value of an existing variable."
                else:
                    self.value = value
            elif isinstance(value, str):
                self.todos.append(GetInputGoal(self.context, self, attr, f"The value, {value}, isn't a number. Can you try again?"))
            else:
                self.value = value
            return

class SubtractFromVariableActionGoal(ActionGoal):
    """Goal for adding a subtract from variable action"""
    def __init__(self, context, name=None, value=None):
        super().__init__(context)
        self.setattr("value", value)
        self.setattr("name", name)

    def complete(self):
        assert hasattr(self, "actions")
        self.actions.append(SubtractFromVariableAction(self.name, self.value))
        return super().complete()

    def setattr(self, attr, value):
        if attr == "name":
            if value is None:
                self.todos.append(GetInputGoal(self.context, self, attr, f"What variable do you want to subtract from?"))
            elif value not in self.variables:
                self.error = f"The variable, {value}, hasn't been created so there is nothing to subtract it. Try creating the variable first."
            else:
                self.name = value
            return
        elif attr == "value":
            if value is None:
                self.todos.append(GetInputGoal(self.context, self, attr, f"What value do you want to subtract from the variable?"))
            elif isinstance(value, ValueOf):
                if value.variable not in self.variables:
                    self.error = f"Variable {value} does not exist. Try setting it to the value of an existing variable."
                else:
                    self.value = value
            elif isinstance(value, str):
                self.todos.append(GetInputGoal(self.context, self, attr, f"Not a number. Try again."))
            else:
                self.value = value
            return
