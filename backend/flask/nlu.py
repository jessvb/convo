from actions.variable import VariableAction, SetVariableAction

class DebugNLU(object):
    def __init__(self):
        self.name = "debug"

    def identify_action(self, message):
        parsed = self.parse(message)
        action = parsed["action"]
        params = parsed["params"]

        if action == "variable":
            return VariableAction(**params)
        elif action == "set_variable":
            return SetVariableAction(**params)
        elif action == "procedure":
            return ProcedureAction(**params)

        raise Exception("No action found.")

    def edit_action(self, message, action):
        parsed = self.parse(message)
        params = parsed["params"]
        action.set_params(params)
        return action

    def parse(self, message):
        args = [arg if arg else None for arg in message.split(",")]
        action = args[0]
        params = {}

        if action == "variable" or action == "set_variable":
            params["name"] = args[1]
            params["value"] = args[2]
        elif action == "procedure":
            params["name"] = args[1]

        return {
            "action": action,
            "params": params
        }
