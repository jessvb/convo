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
    "equal to": "=",
    "greater than or equal to": ">=",
    "less than or equal to": "<="
}

class ComparisonCondition(Condition):
    def __init__(self, variable, op, value):
        self.variable = variable
        self.value = value
        self.op = op

    def eval(self, variables):
        variable = variables[self.variable]
        if self.op == "greater than":
            return variable > self.value
        elif self.op == "less than":
            return variable < self.value
        elif self.op == "greater than or equal to":
            return variable >= self.value
        elif self.op == "less than or equal to":
            return variable <= self.value
        elif self.op == "equal to":
            return variable == self.value
        return False

    def __str__(self):
        return f"{self.variable} {comparison_ops.get(self.op)} {self.value}"
