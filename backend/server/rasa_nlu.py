from goals import *
from app import logger
import requests
import json

intent_goal = {
    "create_procedure": CreateProcedureGoal,
    "rename_procedure": RenameProcedureGoal,
    "delete_procedure": DeleteProcedureGoal,
    "run_procedure": ExecuteGoal,
    "edit_procedure": EditGoal,
    "say": SayActionGoal,
    "get_user_input": GetInputGoal,
    "play_sound": PlaySoundActionGoal,
    "create_variable": CreateVariableActionGoal,
    "set_variable": SetVariableActionGoal,
    "add_to_variable": AddToVariableActionGoal,
    "subtract_from_variable": SubtractFromVariableActionGoal,
    "go_to_step": GoToStepGoal,
    "delete_step": DeleteStepGoal,
    "add_step": AddStepGoal,
    "change_step": ChangeStepGoal,
    "run_intent": RunIntentGoal
}

intent_entities = {
    "create_procedure": ["procedure_name"],
    "rename_procedure": ["procedure_name", "new_procedure_name"],
    "delete_procedure": ["procedure_name"],
    "run_procedure": ["procedure_name"],
    "edit_procedure": ["procedure_name"],
    "say": ["say_phrase"],
    "play_sound": ["sound"],
    "create_variable": ["variable_name", "variable_value"],
    "set_variable": ["variable_name", "variable_value"],
    "add_to_variable": ["variable_name", "add_value"],
    "subtract_from_variable": ["variable_name", "subtract_value"]
}

class RasaNLU(object):
    """
    NLU that connects with Rasa server to parse messages

    Uses the main function parse_message to connect to Rasa NLU and retrieve intent and entity
    """

    def __init__(self, context, confidence_threshold=0.7):
        self.context = context

        # Threshold for the confidence returned by the Rasa NLU for the top intent
        self.confidence_threshold = confidence_threshold

    def parse_message(self, message):
        logger.debug("Rasa parsing message")
        payload = json.dumps({"text": message.lower()})
        res = None

        try:
            rasa_url = "http://rasa:" + self.context.rasa_port + "/model/parse"
            res = requests.post(rasa_url, data=payload)
        except requests.ConnectionError as e:
            logger.info("Cannot connect to Rasa server.")
            return None

        # If no response from Rasa NLU server, return None
        if (res is None or res.status_code != 200):
            return None

        intents = res.json()
        intent = intents["intent"]
        logger.debug("intents")
        logger.debug(intents)

        if intent["confidence"] < self.confidence_threshold:
            # If confidence is less than threshold, do not use intent
            logger.debug("confidence is less than threshold")
            return None
        original_intent = intent["name"].replace("_", " ")
        if original_intent in self.context.intents:
            for e in intents["entities"]:
                self.context.add_entity(e["entity"], e["value"])
            return RunIntentGoal(self.context, original_intent)
        else:
            goal = intent_goal[intent["name"]]
            entities = {}
            if intents["entities"]:
                entities.update({e["entity"]: self.parse_value(e["value"]) for e in intents["entities"] if e["entity"] in intent_entities[intent["name"]]})

            return goal(self.context, **entities)

    def parse_value(self, message):
        """Try to parse a value which may in the form of a string, a number"""
        value_of = self.parse_value_of(message)
        if value_of:
            return value_of

        number = parse_number(message)
        if number is not None:
            return number

        return message

    def parse_value_of(self, message):
        value_of_regex = "(?:the )?value of (?:(?:the )?variable )?(.+)"
        """Try to parse message of the form "value of <variable>" and return a ValueOf object"""
        if not message:
            return message
        elif re.match(value_of_regex, message):
            match = re.match(value_of_regex, message)
            return ValueOf(variable=group(match, 1))

def group(match, idx):
    if isinstance(idx, int) and len(match.groups()) > 0 and match.group(idx):
        return match.group(idx)
    elif isinstance(idx, list):
        for i in idx:
            res = group(match, i)
            if res:
                return res
    return None
