from models import *
from goals import *
from goals.inpt import GetInputGoal

class CreateClassGoal(object):
    def __init__(self, context, name=None):
        self.context = context
        self.klass = Class(name)
        self.context.add_class(self.klass)
        self.todos = []

        self.todos.append(GetClassPropertiesGoal(context, self))
        if self.klass.name is None or self.klass.name == "":
            self.todos.append(GetInputGoal(self.context, self, "name", "What do you want to call the class?"))

    @property
    def is_complete(self):
        return len(self.todos) == 0

    @property
    def message(self):
        return "Class created!" if self.is_complete else self.todos[-1].message

    def setattr(self, attr, value):
        if (attr == "name"):
            if value in self.context.classes:
                self.todos.append(GetInputGoal(self.context, self, attr, f"Class {value} already exists. Try another name or say cancel."))
            else:
                self.klass.name = value
        else:
            setattr(self, attr, value)

    def try_complete(self):
        if not self.is_complete:
            self.pursue()

        if self.is_complete:
            print("Completing CreateClass")
            self.context.add_class(self.klass)
            self.context.goals.pop()

        return self.message

    def pursue(self):
        print("Pursuing CreateClass")
        self.todos[-1].try_complete()

    def __str__(self):
        return "create_class" + (f":{str(self.todos[-1])}" if self.todos else "")

class GetClassPropertiesGoal(object):
    def __init__(self, context, goal):
        self.context = context
        self.goal = goal
        self.todos = []
        self.complete = False

    @property
    def is_complete(self):
        return self.complete and len(self.todos) == 0

    @property
    def message(self):
        if self.is_complete:
            return "GetClassPropertiesGoal completed!"

        if len(self.todos) == 0:
            if len(self.goal.klass.properties) > 0:
                return "Any other properties?"
            else:
                return "What properties does it have?"
        else:
            return self.todos[-1].message

    def try_complete(self):
        if not self.is_complete:
            self.pursue()

        if self.is_complete:
            print("Completing GetClassProperties")
            self.goal.todos.pop()

        return self.message

    def pursue(self):
        print("Pursuing GetClassProperties")
        message = self.context.current_message
        if message == "no" and len(self.todos) == 0:
            self.complete = True
        elif len(self.todos) > 0:
            self.todos[-1].try_complete()
        else:
            self.todos.append(GetClassPropertyGoal(self.context, self, self.goal.klass, message))

    def __str__(self):
        return "get_class_properties" + (f":{str(self.todos[-1])}" if self.todos else "")

class GetClassPropertyGoal(object):
    def __init__(self, context, goal, klass, name):
        self.context = context
        self.goal = goal
        self.klass = klass
        self.type = None
        self.todos = []
        self.setattr("name", name)
        self.todos.append(GetInputGoal(context, self, "type", "What is the property type?"))

    @property
    def is_complete(self):
        return len(self.todos) == 0

    @property
    def message(self):
        return "GetClassPropertyGoal completed!" if self.is_complete else self.todos[-1].message

    def setattr(self, attr, value):
        if (attr == "name") and (value == "" or value in self.klass.properties):
            message = "Property name was an empty string. Try again." if value == "" else f"Property {value} already exists. Try another name."
            self.todos.append(GetInputGoal(self.context, self, attr, message))
        else:
            setattr(self, attr, value)

    def try_complete(self):
        if not self.is_complete:
            self.pursue()

        if self.is_complete:
            print("Completing GetClassProperty")
            self.klass.add_property(Property(self.klass, self.name, self.type))
            self.goal.todos.pop()

        return self.message

    def pursue(self):
        print("Pursuing GetClassProperty")
        self.todos[-1].try_complete()

    def __str__(self):
        return "get_class_property" + (f":{str(self.todos[-1])}" if self.todos else "")

class AddClassPropertyGoal(object):
    def __init__(self, context, klass=None, name=None, type=None):
        self.context = context
        self.klass = self.context.classes[klass] if klass is not None and klass in self.context.classes else (self.context.cached if isinstance(self.context.cached, Class) else None)
        self.name = name
        self.type = type
        self.todos = []

        if self.name is None or self.name == "":
            self.todos.append(GetInputGoal(self.context, self, "name", "What do you want to call the property?"))
        if self.type is None or self.type == "":
            self.todos.append(GetInputGoal(self.context, self, "type", "What is the property type?"))
        if self.klass is None:
            self.todos.append(GetInputGoal(self.context, self, "klass", "Which class do you want to add the property to?"))

    @property
    def is_complete(self):
        return len(self.todos) == 0

    @property
    def message(self):
        return "Property added to class! Anything else?" if self.is_complete else self.todos[-1].message

    def setattr(self, attr, value):
        if (attr == "klass"):
            if value not in self.context.classes:
                self.todos.append(GetInputGoal(self.context, self, attr, f"Class {value} does not exist. Try another class or say cancel."))
            else:
                self.klass = self.context.classes[value]
        elif (attr == "name") and value in self.klass.properties:
            self.todos.append(GetInputGoal(self.context, self, attr, f"Property {value} already exists. Try another name or say cancel."))
        else:
            setattr(self, attr, value)

    def try_complete(self):
        if not self.is_complete:
            self.pursue()

        if self.is_complete:
            self.klass.add_property(Property(self.klass, self.name, self.type))
            self.context.goals.pop()

        return self.message

    def pursue(self):
        self.todos[-1].try_complete()

    def __str__(self):
        return "add_class_property" + (f":{str(self.todos[-1])}" if self.todos else "")
