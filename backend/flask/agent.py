from transitions import Machine
from editor import ProgramEditor
from parse import AgentParser
from errors import *
import spacy

nlp = spacy.load("en_core_web_sm")

incomplete_input_responses = {
    "make_variable": {
        "name": "What do you want to name the variable?"
    }
}

def get_incomplete_input_response(action_name, input_name):
    return incomplete_input_responses[action_name][input_name]

class Agent(AgentParser):
    def __init__(self):
        AgentParser.__init__(self, nlp)
        self.actions = []
        self.state = "edit"
        self.incomplete_inputs = []

    def parse_message(self, message):
        try:
            if self.state == "incomplete_action":
                action, incomplete_inputs = self.identify_action(message, self.actions[-1])
                self.actions.pop()
            else:
                action, incomplete_inputs = self.identify_action(message)

            self.incomplete_inputs = incomplete_inputs
            self.actions.append(action)

            if len(self.incomplete_inputs) > 0:
                self.state = "incomplete_action"
                return self.ask_for_input(), action
            else:
                self.state = "edit"
                return "Success!", action
        except VariableExistsError as e:
            return e.message, {}

    def ask_for_input(self):
        current_action = self.actions[-1]
        current_input = self.incomplete_inputs[0]

        assert current_action["type"] == current_input[0]

        if current_action["type"] in incomplete_input_responses:
            return get_incomplete_input_response(current_input[0], current_input[1])
        else:
            return "Action type not found."

    def get_info(self):
        return {
            "actions": self.actions,
            "state": self.state,
            "incomplete_inputs": self.incomplete_inputs
        }
