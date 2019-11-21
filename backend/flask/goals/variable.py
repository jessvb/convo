from models import *
from utils import *
from goals import *

class InitVariableGoal(object):
    def __init__(self, context, name=None, value=None):
        self.context = context
        self.todos = []
        self.setattr("value", value)
        self.setattr("name", name)

    @property
    def is_complete(self):
        return len(self.todos) == 0

    @property
    def message(self):
        if self.is_complete:
            return "InitVariableGoal completed!"

        return self.todos[-1].message

    def setattr(self, attr, value):
        if attr == "name":
            if value is None:
                self.todos.append(GetInputGoal(self.context, self, attr, f"What do you want to call the variable?"))
            # elif value in self.procedure.variables:
                # self.todos.append(GetInputGoal(self.context, self, attr, f"Variable {value} already exists! Try another name or say cancel."))
            else:
                setattr(self, attr, value)
        elif attr == "value":
            if value is None:
                self.todos.append(GetInputGoal(self.context, self, attr, f"What should be the initial value?"))
            else:
                setattr(self, attr, value)
        else:
            setattr(self, attr, value)

    def try_complete(self):
        if not self.is_complete:
            self.pursue()

        if self.is_complete:
            print("Completing InitVariableGoal")
            self.actions.append(InitVariableAction(self.procedure.klass, self.name, self.value))
            # self.procedure.add_variable(self.name)
            self.goal.todos.pop()

        return self.message

    def pursue(self):
        print("Pursuing InitVariableGoal")
        self.todos[-1].try_complete()

    def __str__(self):
        return "init_variable" + (f":{str(self.todos[-1])}" if self.todos else "")

class SetVariableValueGoal(object):
    def __init__(self, context, name=None, value=None):
        self.context = context
        self.todos = []
        self.setattr("value", value)
        self.setattr("name", name)

    @property
    def is_complete(self):
        return len(self.todos) == 0

    @property
    def message(self):
        if self.is_complete:
            return "SetVariableValueGoal completed!"

        return self.todos[-1].message

    def setattr(self, attr, value):
        if attr == "name":
            if value is None:
                self.todos.append(GetInputGoal(self.context, self, attr, f"What variable do you want to set?"))
            # elif value not in self.procedure.variables:
            #     self.todos.append(GetInputGoal(self.context, self, attr, f"Variable {value} does not exist! Try another name or say cancel."))
            else:
                setattr(self, attr, value)
        elif attr == "value":
            if value is None:
                self.todos.append(GetInputGoal(self.context, self, attr, f"What value do you want to set?"))
            else:
                setattr(self, attr, value)
        else:
            setattr(self, attr, value)

    def try_complete(self):
        if not self.is_complete:
            self.pursue()

        if self.is_complete:
            print("Completing SetVariableValueGoal")
            self.actions.append(SetVariableValueAction(self.procedure.klass, self.name, self.value))
            self.goal.todos.pop()

        return self.message

    def pursue(self):
        print("Pursuing SetVariableValueGoal")
        self.todos[-1].try_complete()

    def __str__(self):
        return "init_variable" + (f":{str(self.todos[-1])}" if self.todos else "")

class IncrementVariableGoal(object):
    def __init__(self, context, name=None, value=None):
        self.context = context
        self.todos = []
        self.setattr("value", value)
        self.setattr("name", name)

    @property
    def is_complete(self):
        return len(self.todos) == 0

    @property
    def message(self):
        if self.is_complete:
            return "IncrementVariableGoal completed!"

        return self.todos[-1].message

    def setattr(self, attr, value):
        if attr == "name":
            if value is None:
                self.todos.append(GetInputGoal(self.context, self, attr, f"What variable do you want to increment?"))
            # elif value not in self.procedure.variables:
            #     self.todos.append(GetInputGoal(self.context, self, attr, f"Variable {value} does not exist! Try another name or say cancel."))
            else:
                setattr(self, attr, value)
        elif attr == "value":
            if value is None:
                self.todos.append(GetInputGoal(self.context, self, attr, f"How much do you want to add?"))
            else:
                setattr(self, attr, value)
        else:
            setattr(self, attr, value)

    def try_complete(self):
        if not self.is_complete:
            self.pursue()

        if self.is_complete:
            print("Completing IncrementVariableGoal")
            self.actions.append(IncrementVariableAction(self.procedure.klass, self.name, self.value))
            self.goal.todos.pop()

        return self.message

    def pursue(self):
        print("Pursuing IncrementVariableGoal")
        self.todos[-1].try_complete()

    def __str__(self):
        return "increment_variable" + (f":{str(self.todos[-1])}" if self.todos else "")

