from helpers import to_snake_case
tab = "    "

class Procedure(object):
    """Represents a procedure"""
    def __init__(self, name, actions=None, klass=None):
        self.name = name
        self.actions = [] if actions is None else actions
        self.variables = set()
        self.lists = {}
        self.klass = klass

    def __str__(self):
        return f"Procedure {self.name}: {len(self.actions)}"

    def json(self):
        return {
            "name": self.name,
            "actions": [a.json() for a in self.actions]
        }

    def python(self):
        lines = [f"def {to_snake_case(self.name)}({'' if self.klass is None else 'self'}):"]
        lines.extend([f"{tab}{line}" for action in self.actions for line in action.python()])
        return lines

    def add_action(self, action):
        self.actions.append(action)

    def add_variable(self, variable):
        self.variables.add(variable)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented

        return self.actions == self.actions and self.variables == self.variables
