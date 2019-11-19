class Action(object):
    def __init__(self):
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError

    def json(self):
        raise NotImplementedError

class SetPropertyValueAction(Action):
    def __init__(self, klass, property, value):
        self.klass = klass
        self.property = property
        self.value = value

    def __str__(self):
        return f"set_property_value"

    def json(self):
        return {
            "name": str(self),
            "property": self.property,
            "value": self.value
        }

class InitVariableAction(Action):
    def __init__(self, klass, name, value):
        self.klass = klass
        self.name = name
        self.value = value

    def __str__(self):
        return f"init_variable"

    def json(self):
        return {
            "name": str(self),
            "variable": self.name,
            "value": self.value
        }

class SetVariableValueAction(Action):
    def __init__(self, klass, name, value):
        self.klass = klass
        self.name = name
        self.value = value

    def __str__(self):
        return f"set_variable_value"

    def json(self):
        return {
            "name": str(self),
            "variable": self.name,
            "value": self.value
        }

class IncrementVariableAction(Action):
    def __init__(self, klass, name, value):
        self.klass = klass
        self.name = name
        self.value = value

    def __str__(self):
        return f"increment_variable"

    def json(self):
        return {
            "name": str(self),
            "variable": self.name,
            "value": self.value
        }

class SayAction(Action):
    def __init__(self, phrase):
        self.phrase = phrase

    def __str__(self):
        return f"say"

    def json(self):
        return {
            "name": str(self),
            "phrase": self.phrase
        }

class ConditionalAction(Action):
    def __init__(self, condition, actions):
        self.condition = condition
        self.actionsFalse, self.actionsTrue = actions

    def __str__(self):
        return f"conditional"

    def json(self):
        return {
            "name": str(self),
            "condition": str(self.condition),
            "actions_true": [a.json() for a in self.actionsTrue],
            "actions_false": [a.json() for a in self.actionsFalse]
        }

class LoopAction(Action):
    def __init__(self, condition, actions):
        self.condition = condition
        self.actions = actions

    def __str__(self):
        return f"loop"

    def json(self):
        return {
            "name": str(self),
            "condition": str(self.condition),
            "actions": [a.json() for a in self.actions]
        }
