from error import *
from models import *

class Condition(object):
    def __init__(self):
        pass

    def __str__(self):
        return "condition"

class SayCondition(Condition):
    def __init__(self, phrase):
        self.phrase = phrase

    def eval(self, phrase):
        return self.phrase == phrase

    def __str__(self):
        return f"'{self.phrase}'"

comparison_ops = {
    "greater than": ">",
    "less than": "<",
    "greater than or equal to": ">=",
    "less than or equal to": "<="
}

class EqualityCondition(Condition):
    def __init__(self, variable, value, negation=False):
        self.variable = variable
        self.value = value
        self.negation = negation

    def eval(self, variables):
        variable = variables[self.variable]
        value = variables[self.value.variable] if isinstance(self.value, ValueOf) else self.value
        if type(value) != type(variable):
            if isinstance(value, str) or isinstance(variable, str):
                raise ExecutionError(f"The values {value} and {variable} cannot be compared.")

        return variable != value if self.negation else variable == value

    def __str__(self):
        value = f"the value of {self.value.variable}" if isinstance(self.value, ValueOf) else self.value
        return f"{self.variable} {'!' if self.negation else '='}= {value}"

    def to_nl(self):
        value = f"the value of {self.value.variable}" if isinstance(self.value, ValueOf) else self.value
        return f"variable {self.variable} is {'not ' if self.negation else ''}equal to {value}"

class ComparisonCondition(Condition):
    def __init__(self, variable, op, value):
        self.variable = variable
        self.value = value
        self.op = op

    def eval(self, variables):
        variable = variables[self.variable]
        value = variables[self.value.variable] if isinstance(self.value, ValueOf) else self.value
        if type(value) != type(variable):
            if isinstance(value, str) or isinstance(variable, str):
                raise ExecutionError(f"The values {value} and {variable} cannot be compared.")

        if self.op == "greater than":
            return variable > value
        elif self.op == "less than":
            return variable < value
        elif self.op == "greater than or equal to":
            return variable >= value
        elif self.op == "less than or equal to":
            return variable <= value
        return False

    def __str__(self):
        value = f"the value of {self.value.variable}" if isinstance(self.value, ValueOf) else self.value
        return f"{self.variable} {comparison_ops.get(self.op)} {value}"

    def to_nl(self):
        value = f"the value of {self.value.variable}" if isinstance(self.value, ValueOf) else self.value
        return f"variable {self.variable} is {self.op} {value}"
