from goals import *
from models import *

class AddClassProcedureGoal(BaseGoal):
    def __init__(self, context, klass=None, name=None):
        super().__init__(context)
        self.procedure = Procedure(name, [])
        self.context.current = self.procedure

        self.todos = [GetProcedureActionsGoal(self.context, self.procedure.actions)]
        self.setattr("name", name)
        self.setattr("klass", klass)

    @property
    def message(self):
        return "Procedure added! Anything else?" if self.is_complete else self.todos[-1].message

    def complete(self):
        self.procedure.klass.add_procedure(self.procedure)
        self.context.current = None
        return super().complete()

    def setattr(self, attr, value):
        if (attr == "klass"):
            if value is None:
                self.todos.append(GetInputGoal(self.context, self, attr, "Which class do you want to add the procedure to?"))
            elif value not in self.context.classes:
                self.todos.append(GetInputGoal(self.context, self, attr, f"Class {value} does not exist. Try another class or say cancel."))
            else:
                self.procedure.klass = self.context.classes[value]
                if hasattr(self, "name") and self.name in self.klass.properties:
                    self.todos.append(GetInputGoal(self.context, self, "name", f"Procedure {self.name} already exists. Try another name or say cancel."))
            return
        elif (attr == "name"):
            if value is None:
                self.todos.append(GetInputGoal(self.context, self, attr, "What do you want to call the procedure?"))
            elif hasattr(self, "klass") and value in self.klass.properties:
                self.todos.append(GetInputGoal(self.context, self, attr, f"Procedure {value} already exists. Try another name or say cancel."))
            else:
                self.procedure.name = value
            return
        setattr(self, attr, value)

class CreateGeneralProcedureGoal(BaseGoal):
    def __init__(self, context, name=None):
        super().__init__(context)
        self.procedure = Procedure(name, [])
        self.context.current = self.procedure

        self.todos.append(GetProcedureActionsGoal(self.context, self.procedure.actions))
        self.setattr("name", name)

    @property
    def message(self):
        return "Procedure added! Anything else?" if self.is_complete else self.todos[-1].message

    def complete(self):
        self.context.add_procedure(self.procedure)
        self.context.current = None
        return super().complete()

    def setattr(self, attr, value):
        if (attr == "name"):
            if value is None:
                self.todos.append(GetInputGoal(self.context, self, attr, f"What do you want to call the procedure?"))
            elif value in self.context.procedures:
                self.todos.append(GetInputGoal(self.context, self, attr, f"Procedure {value} already exists. Try another name or say cancel."))
            else:
                self.procedure.name = value
            return
        setattr(self, attr, value)

class GetProcedureActionsGoal(BaseGoal):
    def __init__(self, context, actions):
        super().__init__(context)
        self.actions = actions
        self.done = False

    @property
    def is_complete(self):
        return self.done and super().is_complete

    @property
    def message(self):
        if self.error:
            return self.error

        if self.is_complete:
            return "GetProcedureActionsGoal completed!"

        if len(self.todos) == 0:
            return "Added action to procedure! What's next?" if len(self.actions) > 0 else "What do you want to do first?"
        else:
            return self.todos[-1].message

    def advance(self):
        if self.todos:
            super().advance()
            return

        print(f"Advancing {self.__class__.__name__}...")
        self.error = None
        if self.context.current_message in ["done", "nothing"]:
            self.done = True
        elif self.context.parsed is None:
            self.error = "Couldn't understand the action. Try again."
        else:
            action = self.context.parsed
            setattr(action, "actions", self.actions)
            if action.is_complete:
                action.complete()
            else:
                self.todos.append(action)
