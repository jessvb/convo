from models import *
from goals import *

class CreateClassGoal(BaseGoal):
    def __init__(self, context, name=None):
        super().__init__(context)
        self.klass = Class(name)
        self.context.current = self.klass
        self.todos = [GetClassPropertiesGoal(context, self.klass)]
        self.setattr("name", name)

    @property
    def message(self):
        return f"Created class {self.klass.name}!" if self.is_complete else self.todos[-1].message

    def complete(self):
        self.context.add_class(self.klass)
        return super().complete()

    def setattr(self, attr, value):
        if (attr == "name"):
            if value is None:
                self.todos.append(GetInputGoal(self.context, self, "name", "What do you want to call the class?"))
            elif value in self.context.classes:
                self.todos.append(GetInputGoal(self.context, self, attr, f"Class {value} already exists. Try another name or say cancel."))
            else:
                self.klass.name = value
            return
        setattr(self, attr, value)

class GetClassPropertiesGoal(BaseGoal):
    def __init__(self, context, klass):
        super().__init__(context)
        self.klass = klass
        self.done = False

    @property
    def is_complete(self):
        return self.done and super().is_complete

    @property
    def message(self):
        if self.is_complete:
            return "GetClassPropertiesGoal completed!"

        if len(self.todos) == 0:
            return "Any other properties?" if len(self.klass.properties) > 0 else "What properties does it have?"
        else:
            return self.todos[-1].message

    def advance(self):
        if self.todos:
            super().advance()
            return

        print(f"Advancing {self.__class__.__name__}...")
        if self.context.current_message == "no":
            self.done = True
        else:
            self.todos.append(GetClassPropertyGoal(self.context, self.context.current_message, self.klass))

class GetClassPropertyGoal(BaseGoal):
    def __init__(self, context, name, klass):
        super().__init__(context)
        self.klass = klass
        self.setattr("name", name)
        self.setattr("value", None)

    def complete(self):
        self.klass.add_property(Property(self.klass, self.name, self.type))
        return super().complete()

    def setattr(self, attr, value):
        if (attr == "name") and value in self.klass.properties:
            self.todos.append(GetInputGoal(self.context, self, attr, f"Property {value} already exists. Try another name."))
        elif (attr == "value") and value is None:
            self.todos.append(GetInputGoal(self.context, self, "type", "What is the property type?"))
        setattr(self, attr, value)

class AddClassPropertyGoal(BaseGoal):
    def __init__(self, context, klass=None, name=None, type=None):
        super().__init__(context)
        self.setattr("type", type)
        self.setattr("name", name)
        self.setattr("klass", klass)

    @property
    def message(self):
        return f"Property {self.name} added to class {self.klass.name}! Anything else?" if self.is_complete else self.todos[-1].message

    def complete(self):
        self.klass.add_property(Property(self.klass, self.name, self.type))
        return super().complete()

    def setattr(self, attr, value):
        if (attr == "klass"):
            if value is None:
                self.todos.append(GetInputGoal(self.context, self, attr, "Which class do you want to add the property to?"))
            elif value not in self.context.classes:
                self.todos.append(GetInputGoal(self.context, self, attr, f"Class {value} does not exist. Try another class or say cancel."))
            else:
                self.klass = self.context.classes[value]
                if hasattr(self, "name") and self.name in self.klass.properties:
                    self.todos.append(GetInputGoal(self.context, self, "name", f"Property {self.name} already exists. Try another name or say cancel."))
            return
        elif (attr == "name"):
            if value is None:
                self.todos.append(GetInputGoal(self.context, self, attr, "What do you want to call the property?"))
            elif hasattr(self, "klass") and value in self.klass.properties:
                self.todos.append(GetInputGoal(self.context, self, attr, f"Property {value} already exists. Try another name or say cancel."))
                return
        elif (attr == "type") and value is None:
            self.todos.append(GetInputGoal(self.context, self, "type", "What is the property type?"))
        setattr(self, attr, value)

class SetClassPropertyActionGoal(BaseGoal):
    def __init__(self, context, name=None, value=None):
        super().__init__(context)
        self.setattr("value", value)
        self.setattr("name", name)

    def complete(self):
        assert hasattr(self, "actions")
        self.actions.append(SetPropertyAction(self.name, self.value))
        return super().complete()

    def setattr(self, attr, value):
        if attr == "name" and value is None:
            self.todos.append(GetInputGoal(self.context, self, attr, f"What property do you want to set?"))
        elif attr == "value" and value is None:
            self.todos.append(GetInputGoal(self.context, self, attr, f"What value do you want to set the property to?"))
        setattr(self, attr, value)
