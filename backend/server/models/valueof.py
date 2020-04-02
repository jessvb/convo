class ValueOf(object):
    """Represents the value of a variable at a moment or time in execution"""
    def __init__(self, variable):
        self.variable = variable

    def eval(self, variables):
        return variables.get(self.variable, None)

    def to_nl(self):
        return f"the value of variable {self.variable}"

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented

        return self.variable == self.variable
