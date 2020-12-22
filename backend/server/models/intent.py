from helpers import to_snake_case
tab = "    "

class Intent(object):
    """Represents an intent"""
    def __init__(self, name, entities=None):
        self.name = name
        # List of all entities required for this intent.
        self.entities = entities if entities else []

    def __str__(self):
        return f"Intent {self.name}: {self.entities}"

    def json(self):
        return {
            "name": self.name,
            "entities": [a.json() for a in self.entities]
        }

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented

        return self.name == self.name and self.entities == self.entities
