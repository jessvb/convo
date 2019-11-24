class Procedure(object):
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

    def add_action(self, action):
        self.actions.append(action)

    def add_variable(self, variable):
        self.variables.add(variable)
