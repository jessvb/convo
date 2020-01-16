from utils import to_snake_case
tab = "    "

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

    def python(self):
        properties = [p.name for p in self.properties.values()]
        lines = [
            f"class {to_snake_case(self.name)}(object):",
            f"{tab}def __init__(self, {', '.join(properties)}):"
        ]
        lines.extend([f"{tab}{tab}self.{name} = {name}" for name in properties])
        for procedure in self.procedures.values():
            lines.append("")
            lines.extend([f"{tab}{line}" for line in procedure.python()])
        return lines

    def add_property(self, property):
        self.properties[property.name] = property

    def add_procedure(self, procedure):
        self.procedures[procedure.name] = procedure

    def create(self):
        return Object(self)

class Object(object):
    def __init__(self, klass):
        self.klass = klass
        self.properties = {}

class Property(object):
    def __init__(self, klass, name, type):
        self.name = name
        self.type = type
        self.klass = klass

    def __str__(self):
        return f"({self.name}, {self.type})"

    def json(self):
        return {
            "name": self.name,
            "type": self.type
        }

class ListProperty(Property):
    def __init__(self, klass, name):
        super().__init__(klass, name, "list")
