from error import *
from models import *

class Condition(object):
    """Represents a condition"""
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

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented

        return self.phrase == other.phrase

comparison_ops = {
    "greater than": ">",
    "less than": "<",
    "greater than or equal to": ">=",
    "less than or equal to": "<="
}

class EqualityCondition(Condition):
    """Represents an equality condition"""

    def __init__(self, variable, value, negation=False):
        # Variable to retrieve when evaluating
        self.variable = variable

        # Value to compare against
        self.value = value

        # Whether is is == or !=
        self.negation = negation

    def eval(self, variables):
        """
        Evaluate the variable

        Assumes that the variable to evaluate is in variables
        """
        variable = variables[self.variable.variable]
        value = variables[self.value.variable] if isinstance(self.value, ValueOf) else self.value
        if type(value) != type(variable):
            if isinstance(value, str) or isinstance(variable, str):
                raise ExecutionError(f"The values {value} and {variable} cannot be compared.")

        return variable != value if self.negation else variable == value

    def __str__(self):
        value = f"the value of {self.value.variable}" if isinstance(self.value, ValueOf) else self.value
        return f"{self.variable.variable} {'!' if self.negation else '='}= {value}"

    def to_nl(self):
        value = f"the value of {self.value.variable}" if isinstance(self.value, ValueOf) else self.value
        return f"variable {self.variable.variable} is {'not ' if self.negation else ''}equal to {value}"

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented

        return self.variable == other.variable and self.value == other.value and self.negation == other.negation

class ComparisonCondition(Condition):
    """Represents an comparison condition"""
    def __init__(self, variable, op, value):
        # Variable to retrieve when evaluating
        self.variable = variable

        # Value to compare against
        self.value = value

        # Operator to evaluate with - includes >, >=, <, <=
        self.op = op

    def eval(self, variables):
        """
        Evaluate the variable

        Assumes that the variable to evaluate is in variables
        """
        variable = variables[self.variable.variable]
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
        return f"{self.variable.variable} {comparison_ops.get(self.op)} {value}"

    def to_nl(self):
        value = f"the value of {self.value.variable}" if isinstance(self.value, ValueOf) else self.value
        return f"variable {self.variable.variable} is {self.op} {value}"

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented

        return self.variable == other.variable and self.value == other.value and self.op == other.op
