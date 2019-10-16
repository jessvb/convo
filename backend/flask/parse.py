from spacy.matcher import Matcher
from errors import *
import re

class AgentParser(object):
    def __init__(self, nlp):
        matcher = Matcher(nlp.vocab)

        matcher.add("make_variable", None,
                    [{"LEMMA": {"IN": ["make", "create", "add"]}}, {"OP": "?"}, {"LOWER": "variable"}])
        matcher.add("name_variable", None,
                    [{"LEMMA": {"IN": ["call", "name"]}}, {"LOWER": "it"}, {}],
                    [{"LEMMA": {"IN": ["call", "name"]}}, {"LOWER": {"NOT_IN": ["it"]}}],
                    [{"LEMMA": {"IN": ["call", "name"]}}, {"LOWER": "the", "OP": "?"}, {"LOWER": "variable"}, {}])
        matcher.add("set_variable", None,
                    [{"LOWER": "set"}, {"LOWER": "it"}, {"LOWER": "to"}, {"OP": "+"}],
                    [{"LOWER": "set"}, {"LOWER": "the", "OP": "?"}, {"LOWER": "variable"}, {}, {"LOWER": "to"}, {"OP": "+"}],
                    [{"LOWER": "set"}, {"LOWER": {"NOT_IN": ["it"]}}, {"LOWER": "to"}, {"OP": "+"}])

        self.matcher = matcher
        self.nlp = nlp
        self.vocab = nlp.vocab
        self.variables = set()
        self.actions = []
        self.incomplete_inputs = []

    def get_matches(self, message):
        doc = self.nlp(message)
        matches = self.matcher(doc)
        return [(self.vocab.strings[match_id], doc[start:end]) for match_id, start, end in matches]

    def identify_action(self, message, action=None):
        matches = self.get_matches(message)
        if len(matches) < 1:
            raise InputError("No actions detected.")

        for rule, doc in matches:
            if rule == "make_variable":
                action = self.action_create_variable()
            elif rule == "name_variable":
                if not action:
                    raise InputError("Cannot name variable.")
                action = self.action_name_variable(doc, action)
            elif rule == "set_variable":
                action = self.action_set_variable(doc, action)

        if not action:
            raise InputError("Cannot identify action.")

        return action, check_if_incomplete(action)

    def action_name_variable(self, doc, action):
        assert action["type"] == "make_variable"
        name = parse_name_variable(doc)

        if (name in self.variables):
            raise VariableExistsError(name)

        action["inputs"]["name"]["value"] = name
        self.variables.add(name)
        return action

    def action_create_variable(self):
        create_variable = {
            "type": "make_variable",
            "inputs": {
                "name": {
                    "value": None,
                    "required": True
                },
                "value": {
                    "value": None,
                    "required": False
                }
            }
        }

        return create_variable

    def action_set_variable(self, doc, action=None):
        name, value = parse_set_variable(doc.text)

        if action:
            assert action["type"] == "make_variable"
            action["inputs"]["value"]["value"] = value
            return action

        if not name or name == "it":
            if self.actions:
                if self.actions[-1]["type"] == "make_variable":
                    name = self.actions[-1]["inputs"]["name"]
            else:
                raise InputError("Please specify variable.")
        elif name not in self.variables:
            raise InputError(f"Variable {name} does not exist")

        if not value:
            raise InputError("Specific a value to set.")

        return {
            "type": "set_variable",
            "inputs": {
                "value": {
                    "value": value,
                    "required": True
                },
                "name": {
                    "value": name,
                    "required": True
                }
            }
        }

        def action_create_procedure(self):
            create_procedure = {
                "type": "create_procedure",
                "inputs": {
                    "name": None,
                    "steps": []
                }
            }

            return create_procedure

def check_if_incomplete(action):
    return [(action["type"], k)
            for k, v in action["inputs"].items()
            if v["value"] is None and v["required"]]

def parse_set_variable(text):
    pattern = "(?:set(?:.*variable)?)(.+)to(.+)"
    m = re.match(pattern, text)
    name, value = m.group(1, 2)
    return name.strip(), value.strip()

def parse_name_variable(doc):
    # pattern = "(?:(?:name|call)(?:.*(?:it|variable)))?(.+)"
    for i, token in enumerate(doc):
        if token.text == "variable" or token.text == "it":
            return doc[i+1:].text

    for i, token in enumerate(doc):
        if token.lemma_ == "call" or token.lemma_ == "name":
            return doc[i+1:].text

    raise Exception("Cannot parse name.")
