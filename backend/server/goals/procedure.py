from goals import *
from models import *

class CreateProcedureGoal(HomeGoal):
    def __init__(self, context, name=None):
        super().__init__(context)
        self.procedure = Procedure(name, [])
        self.context.current = self.procedure
        self.procedures = self.context.procedures
        self.setattr("name", name)

    @property
    def message(self):
        if self.error:
            return self.error

        if self._message:
            return self._message

        return f"What do you want to happen in the procedure first? You could make me say something. See the sidebar for more options." if self.is_complete else self.todos[-1].message

    def complete(self):
        self.procedures[self.procedure.name] = self.procedure
        self.context.transition(self)
        self.context.current = self.procedure
        self.context.goals.insert(len(self.context.goals) - 2, GetProcedureActionsGoal(self.context, self.procedure))
        return super().complete()

    def cancel(self):
        self.context.current = None

    def setattr(self, attr, value):
        if (attr == "name"):
            if value is None:
                self.todos.append(GetInputGoal(self.context, self, attr, "What do you want to call the procedure?"))
            elif value in self.procedures:
                self.error = f"The name, {value}, has already been used. You can edit the procedure by saying \"edit {value}\"."
            else:
                self.procedure.name = value
            return
        setattr(self, attr, value)

class AddClassProcedureGoal(CreateProcedureGoal):
    def __init__(self, context, name=None, klass=None):
        super().__init__(context, name)
        self.procedures = None
        self.todos = [GetProcedureActionsGoal(self.context, self.procedure.actions)]
        self.setattr("name", name)
        self.setattr("klass", klass)

    def complete(self):
        complete = super().complete()
        self.context.current = self.klass
        return complete

    def setattr(self, attr, value):
        if (attr == "name"):
            super().setattr(attr, value)
            return
        elif (attr == "klass"):
            if value is None:
                self.todos.append(GetInputGoal(self.context, self, attr, "Which class do you want to add the procedure to?"))
            elif value not in self.context.classes:
                self.todos.append(GetInputGoal(self.context, self, attr, f"Class, {value}, hasn't been created. Try another class or say cancel."))
            else:
                self.procedure.klass = self.context.classes[value]
                self.procedures = self.procedure.klass.procedures
                name = self.procedure.name
                if name and name in self.procedures:
                    self.todos.append(GetInputGoal(self.context, self, "name", f"The name, {name}, has already been used. Try another name or say cancel."))
            return
        setattr(self, attr, value)

class RenameProcedureGoal(HomeGoal):
    def __init__(self, context, name=None, new_name=None):
        super().__init__(context)
        self.setattr("new_name", new_name)
        self.setattr("name", name)

    @property
    def message(self):
        if self.error:
            return self.error

        if self._message:
            return self._message

        return f"I renamed procedure {self.name} to {self.new_name}. What do you want to do now?" if self.is_complete else self.todos[-1].message

    def complete(self):
        procedure = self.context.procedures[self.name]
        procedure.name = self.new_name
        self.context.procedures[procedure.name] = procedure
        del self.context.procedures[self.name]
        return super().complete()

    def setattr(self, attr, value):
        if (attr == "name"):
            if not value:
                self.todos.append(GetInputGoal(self.context, self, attr, "Which procedure do you want to rename?"))
            elif value not in self.context.procedures:
                self.error = f"A procedure with the name, {value}, has not been created."
            else:
                self.name = value
            return
        elif (attr == "new_name"):
            if not value:
                self.todos.append(GetInputGoal(self.context, self, attr, "What new name do you want to give the procedure?"))
            elif value in self.context.procedures:
                self.error = f"The name, {value}, has already been used for a procedure."
            else:
                self.new_name = value
        setattr(self, attr, value)

class DeleteProcedureGoal(HomeGoal):
    def __init__(self, context, name=None):
        super().__init__(context)
        self.setattr("name", name)

    @property
    def message(self):
        if self.error:
            return self.error

        if self._message:
            return self._message

        return f"I deleted the procedure, {self.name}. What do you want to do now?" if self.is_complete else self.todos[-1].message

    def complete(self):
        del self.context.procedures[self.name]
        return super().complete()

    def setattr(self, attr, value):
        if (attr == "name"):
            if not value:
                self.todos.append(GetInputGoal(self.context, self, attr, "Which procedure do you want to delete?"))
            elif value not in self.context.procedures:
                self.error = f"A procedure with the name, {value}, has not been created."
            else:
                self.name = value
            return
        setattr(self, attr, value)
