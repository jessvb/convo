class ProgramEditor(object):
    def __init__(self):
        self.actions = []
        self.variables = set()
        self.incompletes = []

    def add(self, action):
        if action.id == "variable":
            name = action.params["name"]
            if name in self.variables:
                raise Exception(f"Variable with name {name} already exists.")
            self.variables.add(name)
        elif action.id == "set_variable":
            name = action.params["name"]
            if name not in self.variables:
                raise Exception(f"Variable {name} does not exist.")

        self.actions.append(action)

    def _info(self):
        return {
            "actions": [action._json() for action in self.actions]
        }

    def _python(self):
        return "\n".join([action._python() for action in self.actions])

    def _js(self):
        return "\n".join([action._js() for action in self.actions])
