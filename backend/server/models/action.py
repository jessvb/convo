from helpers import to_snake_case
from models.valueof import ValueOf
from app import logger

tab = "    "

class Action(object):
    """Represents an action in a procedure"""
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

    def __eq__(self, other):
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

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented

        return self.property == other.property and self.value == other.value

class VariableAction(Action):
    def __init__(self, variable, value):
        self.variable = variable
        self.value = value

    def json(self):
        return {
            "name": str(self),
            "variable": self.variable,
            "value": self.value
        }

    def python(self):
        return [f"{self.variable} = {self.value}"]

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented

        return self.variable == other.variable and self.value == other.value

class CreateVariableAction(VariableAction):
    def __init__(self, variable, value):
        super().__init__(variable, value)

    def to_nl(self):
        value = self.value.to_nl() if isinstance(self.value, ValueOf) else self.value
        return f"creating a variable called {self.variable} and setting its value to {self.value}"

class SetVariableAction(VariableAction):
    def __init__(self, variable, value):
        super().__init__(variable, value)

    def to_nl(self):
        value = self.value.to_nl() if isinstance(self.value, ValueOf) else self.value
        return f"setting the value of variable {self.variable} to {self.value}"

class AddToVariableAction(VariableAction):
    def __init__(self, variable, value):
        super().__init__(variable, value)

    def python(self):
        return [f"{self.variable} += {self.value}"]

    def to_nl(self):
        value = self.value.to_nl() if isinstance(self.value, ValueOf) else self.value
        return f"adding {value} to variable {self.variable}"

class SubtractFromVariableAction(VariableAction):
    def __init__(self, variable, value):
        super().__init__(variable, value)

    def python(self):
        return [f"{self.variable} -= {self.value}"]

    def to_nl(self):
        value = self.value.to_nl() if isinstance(self.value, ValueOf) else self.value
        return f"subtracting {value} from variable {self.variable}"

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

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented

        return self.phrase.lower() == other.phrase.lower()

class GreetAction(Action):
    def __init__(self):
        return
        #self.phrase = phrase <- don't need to init anything here, since there's
        # nothing to set! see SayAction for an example where you do set 
        # something

    def json(self):
        return {
            "name": str(self),
            #"phrase": self.phrase <- since we don't have any attributes, we 
            # don't need this (see SayAction for an example with an attribute)
        }

    def __str__(self):
        # String representation of the class
        name = self.__class__.__name__
        # Default is the just converting to snake case and removing "Action"
        # For AnotherCustomAction, the __str__ would return "another_custom"
        return to_snake_case(name[:-len("Action")])


    def python(self):
        # String representation of potential corresponding Python code
        # Currently not too important, since no Python support yet
        return [f"greet(\"Hello world!\")"]


    def to_nl(self):
        # The "natural language" representation of the action
        # Essentially, what is this action doing in simple terms:
        return "greeting the user with \"Hello world!\""
        
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

        if len(trues) == 1 and \
            not isinstance(trues[0], ConditionalAction) and \
            (len(falses) == 0 or (len(falses) == 1 and not isinstance(falses[0], ConditionalAction))):

            nl = f"{trues[0].to_nl()} if {self.condition.to_nl()}"
            if len(falses) == 1:
                nl += f" else I am {falses[0].to_nl()}"
            return nl

        num_falses = len(falses) if len(falses) > 0 else 'no'
        num_trues = len(trues) if len(trues) > 0 else 'no'
        return f"doing {num_trues} action(s) when {self.condition.to_nl()} and {num_falses} action(s) otherwise"

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented

        return self.condition == other.condition and self.actions[0] == other.actions[0] and self.actions[1] == other.actions[1]

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
        return f"doing {num_actions} action{'s' if num_actions != '1' else ''} in a loop {self.loop} {self.condition.to_nl()}"

    def python(self):
        if self.loop == "while":
            lines = [f"while {str(self.condition)}:"]
            lines.extend([f"{tab}{line}" for action in self.actions for line in action.python()])
            return lines
        raise NotImplementedError

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented

        return self.loop == self.loop and self.condition == other.condition and self.actions == self.actions

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

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented

        return self.name == self.name

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

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented

        return self.name == other.name and self.value == other.value

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

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented

        return self.property == other.property and self.value == other.value

class GetUserInputAction(Action):
    def __init__(self, variable, prompt):
        self.variable = variable
        self.prompt = prompt

    def json(self):
        return {
            "name": str(self),
            "variable": self.variable,
            "prompt": self.prompt
        }

    def to_nl(self):
        return f"listening for input and saving it as {self.variable}"

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented

        return self.variable == other.variable and self.prompt == other.prompt

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

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented

        return self.sound == other.sound

class TextAction(Action):
    def __init__(self,style,length,prefix):
        logger.debug(f"reaching the textAction class")
        self.style = style
        self.length = length
        self.prefix = prefix

    def json(self):
        return {
            "style":self.style,
            "length":self.length,
            "prefix":str(prefix)

        }
    
    def python(self):#what's the purpose for this function?
        return [f"generate text based on {self.style} that is {self.length} long with prefix {self.prefix}"]

    def to_nl(self):
        return f"generate text based on {self.style} that is {self.length} long with prefix {self.prefix}"

    def __eq__(self,other):
        if not isinstance(other, type(self)):
            return NotImplemented

        return self.style == other.style and self.length == other.length and self.prefix == other.prefix
    

class GenerateTextAction(TextAction):
    def __init__(self,style,length,prefix):
        logger.debug(f"hitting the generate text action class")
        super.__init__(style,length,prefix)

    def to_nl(self):
        return f"generate text based on {self.style} that is {self.length} long with prefix {self.prefix}"
