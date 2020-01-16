from utils import to_snake_case
tab = "    "

class Action(object):
    def __init__(self):
        raise NotImplementedError

    def __str__(self):
        name = self.__class__.__name__
        return to_snake_case(name[:-len("Action")])

    def json(self):
        return { "name": str(self) }

    def python(self):
        raise NotImplementedError

class SetPropertyAction(Action):
    def __init__(self, property, value):
        self.property = property
        self.value = value

    def json(self):
        return {
            "name": str(self),
            "property": self.property,
            "value": self.value
        }
    
    def python(self):
        return [f"{self.property} = {self.value}"]

class VariableAction(Action):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def json(self):
        return {
            "name": str(self),
            "variable": self.name,
            "value": self.value
        }

    def python(self):
        return [f"{self.name} = {self.value}"]

class CreateVariableAction(VariableAction):
    def __init__(self, name, value):
        super().__init__(name, value)

class SetVariableAction(VariableAction):
    def __init__(self, name, value):
        super().__init__(name, value)

class IncrementVariableAction(VariableAction):
    def __init__(self, name, value):
        super().__init__(name, value)
    
    def python(self):
        return [f"{self.name} += {self.value}"]

class SayAction(Action):
    def __init__(self, phrase):
        self.phrase = phrase

    def json(self):
        return {
            "name": str(self),
            "phrase": self.phrase
        }

    def python(self):
        return [f"say(\"{self.phrase}\")"]

class ConditionalAction(Action):
    def __init__(self, condition, actions):
        self.condition = condition
        self.actions = actions

    def json(self):
        return {
            "name": str(self),
            "condition": str(self.condition),
            "actions_true": [a.json() for a in self.actions[1]],
            "actions_false": [a.json() for a in self.actions[0]]
        }

    def python(self):
        lines = [f"if {str(self.condition)}:"]
        lines.extend([f"{tab}{line}" for action in self.actions[1] for line in action.python()])
        lines.append("else:")
        lines.extend([f"{tab}{line}" for action in self.actions[0] for line in action.python()])
        return lines

class LoopAction(Action):
    def __init__(self, condition, actions):
        self.condition = condition
        self.actions = actions

    def json(self):
        return {
            "name": str(self),
            "condition": str(self.condition),
            "actions": [a.json() for a in self.actions]
        }

    def python(self):
        lines = [f"while {str(self.condition)}:"]
        lines.extend([f"{tab}{line}" for action in self.actions for line in action.python()])
        return lines

class CreateListAction(Action):
    def __init__(self, name):
        self.name = name

    def json(self):
        return {
            "name": str(self),
            "list": self.name
        }

    def python(self):
        return [f"{self.name} = []"]

class AddToListAction(Action):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def json(self):
        return {
            "name": str(self),
            "list": self.name,
            "value": self.value
        }

    def python(self):
        return [f"{self.name}.append({self.value})"]

class AddToListPropertyAction(Action):
    def __init__(self, property, value):
        self.property = name
        self.value = value

    def json(self):
        return {
            "name": str(self),
            "property": self.property,
            "value": self.value
        }

    def python(self):
        return [f"{self.property}.append({self.value})"]
