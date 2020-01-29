from goals import *
from models import *

class CreateProcedureGoal(HomeGoal):
    def __init__(self, context, name=None):
        super().__init__(context)
        self.context.transition(self)
        self.procedure = Procedure(name, [])
        self.context.current = self.procedure
        self.procedures = self.context.procedures
        self.todos.append(GetProcedureActionsGoal(self.context, self.procedure.actions))
        self.setattr("name", name)

    @property
    def message(self):
        if self.error:
            return self.error

        if self._message:
            return self._message

        return f"I created the procedure. You can say, \"run {self.procedure.name}\" to play it." if self.is_complete else self.todos[-1].message

    def complete(self):
        self.procedures[self.procedure.name] = self.procedure
        self.context.transition("complete")
        self.context.current = None
        logging.debug(f"Procedure: {[str(a) for a in self.procedure.actions]}")
        return super().complete()

    def setattr(self, attr, value):
        if (attr == "name"):
            if value is None:
                self.todos.append(GetInputGoal(self.context, self, attr, "What do you want to call the procedure?"))
            elif value in self.procedures:
                self.error = f"Procedure {value} already exists. Try creating a procedure with another name."
                self.context.transition("complete")
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
                self.todos.append(GetInputGoal(self.context, self, attr, f"Class {value} does not exist. Try another class or say cancel."))
            else:
                self.procedure.klass = self.context.classes[value]
                self.procedures = self.procedure.klass.procedures
                name = self.procedure.name
                if name and name in self.procedures:
                    self.todos.append(GetInputGoal(self.context, self, "name", f"Procedure {name} already exists. Try another name or say cancel."))
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
                self.error = f"Procedure with the name {value} does not exist."
            else:
                self.name = value
            return
        elif (attr == "new_name"):
            if not value:
                self.todos.append(GetInputGoal(self.context, self, attr, "What new name do you want to give the procedure?"))
            elif value in self.context.procedures:
                self.error = f"A procedure with the name {value} already exists."
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

        return f"I deleted the procedure {self.name}. What do you want to do now?" if self.is_complete else self.todos[-1].message

    def complete(self):
        del self.context.procedures[self.name]
        return super().complete()

    def setattr(self, attr, value):
        if (attr == "name"):
            if not value:
                self.todos.append(GetInputGoal(self.context, self, attr, "Which procedure do you want to delete?"))
            elif value not in self.context.procedures:
                self.error = f"Procedure with the name {value} does not exist."
            else:
                self.name = value
            return
        setattr(self, attr, value)
