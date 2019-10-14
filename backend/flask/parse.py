from spacy.matcher import Matcher
from errors import *

class AgentParser(object):
    def __init__(self, nlp):
        matcher = Matcher(nlp.vocab)

        matcher.add("make_variable", None,
                    [{"LEMMA": {"IN": ["make", "create"]}}, {"OP": "?"}, {"LOWER": "variable"}])
        matcher.add("name_variable", None,
                    [{"LEMMA": {"IN": ["call", "name"]}}, {"LOWER": "it"}, {}],
                    [{"LEMMA": {"IN": ["call", "name"]}}, {"LOWER": {"NOT_IN": ["it"]}}],
                    [{"LEMMA": {"IN": ["call", "name"]}}, {"LOWER": "the", "OP": "?"}, {"LOWER": "variable"}, {}])
        matcher.add("set_variable", None,
                    [{"LOWER": "set"}, {"LOWER": "it"}, {"LOWER": "to"}, {"OP": "*"}],
                    [{"LOWER": "set"}, {"LOWER": "variable"}, {}, {"LOWER": "to"}, {"OP": "*"}],
                    [{"LOWER": "set"}, {"LOWER": {"NOT_IN": ["it"]}}, {"LOWER": "to"}, {"OP": "*"}])

        self.matcher = matcher
        self.nlp = nlp
        self.vocab = nlp.vocab
        self.variables = set()

    def get_matches(self, message):
        doc = self.nlp(message)
        matches = self.matcher(doc)
        return [(self.vocab.strings[match_id], doc[start:end]) for match_id, start, end in matches]

    def identify_action(self, message, action=None):
        matches = self.get_matches(message)
        if len(matches) < 1:
            raise Exception("No actions detected.")

        for rule, doc in matches:
            if rule == "make_variable":
                action = self.action_create_variable()
            elif rule == "name_variable":
                if not action:
                    raise Exception("Cannot name variable.")
                action = self.action_name_variable(doc, action)
            elif rule == "set_variable":
                action = self.action_set_variable(doc, action)

        if not action:
            raise Exception("Cannot identify action.")

        return action, check_if_incomplete(action)

    def action_name_variable(self, doc, action):
        assert action["type"] == "make_variable"
        name = parse_name(doc)

        if (name in self.variables):
            raise VariableExistsError(name)

        action["inputs"]["name"]["value"] = name
        self.variables.add(name)
        return action

    def action_create_variable(self):
        create_variable = {
            "type": "make_variable",
            "inputs" : {
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

    def action_set_variable(self, doc=None, action=None):
        if action:
            assert action["type"] == "make_variable"
            action["inputs"]["value"]["value"] = parse_value(doc)
            return action
        else:
            return {
                "type": "set_variable",
                "inputs": {
                    "value": {
                        "value": None,
                        "required": True
                    },
                    "name": {
                        "value": None,
                        "required": False
                    }
                }
            }

def check_if_incomplete(action):
    return [(action["type"], k)
            for k, v in action["inputs"].items()
            if v["value"] is None and v["required"]]

def parse_value(doc):
        text = doc.text
        return text[text.index("to") + 2:].strip()

def parse_name(doc):
    if len(doc) == 1:
        return doc[0].text

    if "variable" in doc.text:
        return doc.text[doc.text.index("variable") + len("variable"):].strip()

    for token in doc:
        if token.dep_ == "oprd":
            return token.text

    raise Exception("Cannot parse name.")
