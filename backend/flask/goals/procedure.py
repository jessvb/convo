from goals import *
from models import *
from goals.inpt import GetInputGoal

class AddClassProcedureGoal(object):
    def __init__(self, context, klass=None, name=None):
        self.context = context
        self.klass = self.context.cached if isinstance(self.context.cached, Class) else self.context.classes.get(klass)
        self.procedure = Procedure(name, klass=self.klass)
        self.todos = []

        self.todos.append(GetProcedureActionsGoal(self.context, self, self.procedure))
        self.setattr("name", name)
        if self.klass is None:
            self.todos.append(GetInputGoal(self.context, self, "klass", "Which class do you want to add the procedure to?"))

    @property
    def is_complete(self):
        return len(self.todos) == 0

    @property
    def message(self):
        return "Procedure added! Anything else?" if self.is_complete else self.todos[-1].message

    def setattr(self, attr, value):
        if (attr == "klass"):
            if value not in self.context.classes:
                self.todos.append(GetInputGoal(self.context, self, attr, f"Class {value} does not exist. Try another class or say cancel."))
            else:
                self.procedure.klass = self.context.classes[value]
                self.klass = self.context.classes[value]
        elif (attr == "name"):
            if value is None:
                self.todos.append(GetInputGoal(self.context, self, attr, f"What do you want to call the procedure?"))
            elif value in self.klass.procedures:
                self.todos.append(GetInputGoal(self.context, self, attr, f"Procedure {value} already exists. Try another name or say cancel."))
            else:
                self.procedure.name = value
        else:
            setattr(self, attr, value)

    def try_complete(self):
        if not self.is_complete:
            self.pursue()

        if self.is_complete:
            print("Completing AddClassProcedureGoal")
            self.klass.add_procedure(self.procedure)
            self.context.goals.pop()

        return self.message

    def pursue(self):
        print("Pursuing AddClassProcedureGoal")
        self.todos[-1].try_complete()

    def __str__(self):
        return "add_class_procedure" + (f":{str(self.todos[-1])}" if self.todos else "")

class GetProcedureActionsGoal(object):
    def __init__(self, context, goal, procedure):
        self.context = context
        self.goal = goal
        self.procedure = procedure
        self.todos = []
        self.no_more_actions = False
        self.error = None

    @property
    def is_complete(self):
        return self.no_more_actions and len(self.todos) == 0

    @property
    def message(self):
        if self.error:
            return self.error

        if self.is_complete:
            return "GetProcedureActionsGoal completed!"

        if len(self.todos) == 0:
            if len(self.procedure.actions) > 0:
                return "Added action! What's next?"
            else:
                return "What do you want to do first?"
        else:
            return self.todos[-1].message

    def try_complete(self):
        if not self.is_complete:
            self.pursue()

        if self.is_complete:
            print("Completing GetProcedureActionsGoal")
            self.goal.todos.pop()

        return self.error if self.error else self.message

    def pursue(self):
        print("Pursuing GetProcedureActionsGoal")
        message = self.context.current_message
        self.error = None
        if message in ["done", "nothing"] and len(self.todos) == 0:
            self.no_more_actions = True
        elif len(self.todos) > 0:
            self.todos[-1].try_complete()
        elif self.context.parsed is None:
            self.error = "Couldn't understand the action. Try again."
        else:
            goal = self.context.parsed
            setattr(goal, "procedure", self.procedure)
            setattr(goal, "actions", self.procedure.actions)
            setattr(goal, "goal", self)
            self.todos.append(goal)
            if goal.is_complete:
                goal.try_complete()

    def __str__(self):
        return "get_actions" + (f":{str(self.todos[-1])}" if self.todos else "")

class SetClassPropertyValueGoal(object):
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
            return "SetClassPropertyValueGoal completed!"

        return self.todos[-1].message

    def setattr(self, attr, value):
        if attr == "name":
            if value is None:
                self.todos.append(GetInputGoal(self.context, self, attr, f"What property do you want to set?"))
            # elif value not in self.procedure.klass.properties:
            #     self.todos.append(GetInputGoal(self.context, self, attr, f"Property {value} doesn't exist. Try another name."))
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
            print("Completing SetClassPropertyValueGoal")
            self.actions.append(SetPropertyValueAction(self.procedure.klass, self.name, self.value))
            self.goal.todos.pop()

        return self.message

    def pursue(self):
        self.todos[-1].try_complete()

    def __str__(self):
        return "set_property_value" + (f":{str(self.todos[-1])}" if self.todos else "")
