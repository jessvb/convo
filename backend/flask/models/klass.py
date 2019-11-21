class Class(object):
    def __init__(self, name, properties=None, procedures=None):
        self.name = name
        self.properties = properties if properties else {}
        self.procedures = procedures if procedures else {}

    def __str__(self):
        return f"Class {self.name}: {[str(p) for p in self.properties.values()]} : {[str(p) for p in self.procedures.values()]}"

    def json(self):
        return {
            "name": self.name,
            "properties": [p.json() for p in self.properties.values()],
            "procedures": [p.json() for p in self.procedures.values()]
        }

    def add_property(self, property):
        self.properties[property.name] = property

    def add_procedure(self, procedure):
        self.procedures[procedure.name] = procedure

    def create(self):
        return Object(self)

class Object(object):
    def __init__(self, klass):
        self.klass = klass

class Property(object):
    def __init__(self, klass, name, typ):
        self.name = name
        self.type = typ
        self.klass = klass

    def __str__(self):
        return f"({self.name}, {self.type})"

    def json(self):
        return {
            "name": self.name,
            "type": self.type
        }
