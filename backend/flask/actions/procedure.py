import json
from actions.base import BaseAction

class ProcedureAction(BaseAction):
    id = "procedure"
    responses = {
        "_complete_all": "Procedure created!",
        "_ask_inputs_initial": "What inputs do you want? List them one by one."
        "_ask_inputs": "Any other inputs?"
        "_complete_inputs": "Okay, the procedure has inputs now."
        "_ask_actions_initial": "What is the first step?"
        "_ask_actions": "What's the next step?"
        "_complete_procedure": "Okay, the procedure has steps now."
        "_ask_name": "What do you want to call this procedure?"
    }

    def __init__(self, name):
        self.allow_nesting = True
        self.required = ["name"]
        self.params = {
            "name": name,
            "inputs": [],
            "actions": []
        }

    def _json(self):
        return {
            "action": self.id,
            "params": {
                "name": self.params["name"],
                "inputs": self.params["inputs"],
                "actions": [action._json() for action in self.params["actions"]]
            }
        }

    def _python(self):
        builder = []
        builder.append(f"def {self.params["name"]}():")
        builder.extend([f"\t{action._python().replace("\n", "\t")}" for action in self.params["actions"]])
        return "\n".join(builder)

    def _js(self):
        builder = []
        actions = self.params["actions"]
        builder.append(f"function {self.params["name"]}() {{")
        builder.extend([f"\t{action._js().replace("\n", "\t")}" for action in self.params["actions"]])
        builder.append("}")
        return "\n".join(builder)
