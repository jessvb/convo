import json
from actions.base import BaseAction

class VariableAction(BaseAction):
    id = "variable"
    responses = {
        "_ask_name": "What do you want to call the variable?",
        "_complete": "Variable created!"
    }

    def __init__(self, name, value):
        self.allow_nesting = False
        self.required = ["name"]
        self.params = {
            "name": name,
            "value": value
        }

    def _json(self):
        return {
            "action": self.id,
            "params": self.params
        }

    def _python(self):
        name, value = self.params["name"], self.params["value"]
        return f"{name} = {value}"

    def _js(self):
        name, value = self.params["name"], self.params["value"]
        return f"let {name}{f' = {name}' if value is not None else ''};"


class SetVariableAction(VariableAction):
    id = "set_variable"
    responses = {
        "_ask_name": "What variable do you want to set?",
        "_ask_value": "What value do you want to the variable to?",
        "_complete": "Variable set!"
    }

    def __init__(self, name, value):
        self.allow_nesting = False
        self.required = ["name", "value"]
        self.params = {
            "name": name,
            "value": value
        }

    def _js(self):
        name, value = self.params["name"], self.params["value"]
        return f"{name} = {value};"

