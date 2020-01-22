from models import *
from goals import *
from word2number import w2n

class CreateVariableActionGoal(ActionGoal):
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
                self.todos.append(GetInputGoal(self.context, self, attr, f"Variable {value} already exists. Try another name or say cancel."))
            else:
                self.name = value
            return
        elif attr == "value":
            if value is None:
                self.todos.append(GetInputGoal(self.context, self, attr, f"What should be the initial value?"))
            elif isinstance(value, ValueOf):
                if value.variable not in self.variables:
                    self.todos.append(GetInputGoal(self.context, self, attr, f"Variable {value.variable} does not exist. Try another variable or value."))
                else:
                    self.value = value
            elif value.isnumeric():
                num = float(value)
                self.value = int(num) if num.is_integer() else num
            else:
                try:
                    self.value = w2n.word_to_num(value)
                except ValueError as e:
                    self.value = value
            return
        setattr(self, attr, value)

class SetVariableActionGoal(ActionGoal):
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
                self.todos.append(GetInputGoal(self.context, self, attr, f"Variable {value} does not exist. Create the variable first or say cancel."))
            else:
                self.name = value
            return
        elif attr == "value":
            if value is None:
                self.todos.append(GetInputGoal(self.context, self, attr, f"What value do you want to set the variable to?"))
            elif isinstance(value, ValueOf):
                if value.variable not in self.variables:
                    self.todos.append(GetInputGoal(self.context, self, attr, f"Variable {value.variable} does not exist. Try another variable or value."))
                else:
                    self.value = value
            elif value.isnumeric():
                num = float(value)
                self.value = int(num) if num.is_integer() else num
            else:
                try:
                    self.value = w2n.word_to_num(value)
                except ValueError as e:
                    self.value = value
            return
        setattr(self, attr, value)

class IncrementVariableActionGoal(ActionGoal):
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
            elif value not in self.variables:
                self.todos.append(GetInputGoal(self.context, self, attr, f"Variable {value} does not exist. Create the variable first and try again or say cancel."))
            else:
                self.name = value
            return
        elif attr == "value":
            if value is None:
                self.todos.append(GetInputGoal(self.context, self, attr, f"What value do you want to set the variable to?"))
            elif isinstance(value, ValueOf):
                if value.variable not in self.variables:
                    self.todos.append(GetInputGoal(self.context, self, attr, f"Variable {value.variable} does not exist. Try another variable or value."))
                else:
                    self.value = value
            elif value.isnumeric():
                num = float(value)
                self.value = int(num) if num.is_integer() else num
            else:
                try:
                    self.value = w2n.word_to_num(value)
                except ValueError as e:
                    self.todos.append(GetInputGoal(self.context, self, attr, f"Not a number. Try again."))
            return
