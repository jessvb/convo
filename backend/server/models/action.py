from helpers import to_snake_case
from models.valueof import ValueOf

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

    def to_nl(self):
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

    def to_nl(self):
        return f"setting property {self.property} to {self.value}"

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

    def to_nl(self):
        value = self.value.to_nl() if isinstance(self.value, ValueOf) else self.value
        return f"creating a variable called {self.name} and setting its value to {self.value}"

class SetVariableAction(VariableAction):
    def __init__(self, name, value):
        super().__init__(name, value)

    def to_nl(self):
        value = self.value.to_nl() if isinstance(self.value, ValueOf) else self.value
        return f"setting the value of variable {self.name} to {self.value}"

class AddToVariableAction(VariableAction):
    def __init__(self, name, value):
        super().__init__(name, value)

    def python(self):
        return [f"{self.name} += {self.value}"]

    def to_nl(self):
        value = self.value.to_nl() if isinstance(self.value, ValueOf) else self.value
        return f"adding {value} to variable {self.name}"

class SubtractFromVariableAction(VariableAction):
    def __init__(self, name, value):
        super().__init__(name, value)

    def python(self):
        return [f"{self.name} -= {self.value}"]

    def to_nl(self):
        value = self.value.to_nl() if isinstance(self.value, ValueOf) else self.value
        return f"subtracting {value} from variable {self.name}"

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

    def to_nl(self):
        if isinstance(self.phrase, ValueOf):
            return f"saying the value of the variable {self.phrase.variable}"
        return f"saying the phrase \"{self.phrase}\""

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

    def to_nl(self):
        falses, trues = self.actions
        return f"doing {len(falses) if len(falses) > 0 else 'no'} action(s) when {self.condition.to_nl()} and {len(trues) if len(trues) > 0 else 'no'} action(s) otherwise"

class LoopAction(Action):
    def __init__(self, loop, condition, actions):
        self.loop = loop
        self.condition = condition
        self.actions = actions

    def json(self):
        return {
            "name": str(self),
            "loop": self.loop,
            "condition": str(self.condition),
            "actions": [a.json() for a in self.actions]
        }

    def to_nl(self):
        num_actions = str(len(self.actions)) if len(self.actions) > 0 else 'no'
        return f"doing {num_actions} action{'s' if num_actions != '1' else ''} {self.loop} {self.condition.to_nl()}"

    def python(self):
        if self.loop == "while":
            lines = [f"while {str(self.condition)}:"]
            lines.extend([f"{tab}{line}" for action in self.actions for line in action.python()])
            return lines
        raise NotImplementedError

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

    def to_nl(self):
        return f"creating a list called {self.name}"

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

    def to_nl(self):
        return f"adding {self.value} to list {self.name}"

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

class GetUserInputAction(Action):
    def __init__(self, variable):
        self.variable = variable

    def json(self):
        return {
            "name": str(self),
            "variable": self.variable
        }

    def to_nl(self):
        return f"getting input from user and saving it as variable {self.variable}"

class PlaySoundAction(Action):
    def __init__(self, sound):
        self.sound = sound

    def json(self):
        return {
            "name": str(self),
            "sound": self.sound
        }

    def to_nl(self):
        return f"playing the sound file {self.sound}"
