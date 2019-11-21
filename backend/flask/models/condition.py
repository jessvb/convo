class Condition(object):
    def __init__(self):
        pass

    def eval(self):
        raise NotImplementedError()

    @property
    def op_func(self):
        raise NotImplementedError()

    def __str__(self):
        return "condition"

class SayCondition(Condition):
    def __init__(self, context, phrase):
        self.context = context
        self.phrase = phrase

    def eval(self):
        return self.op_func(self.context.current_message)

    @property
    def op_func(self):
        return self.phrase.__eq__

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
    def __init__(self, context, variable, op, value):
        self.context = context
        self.variable = variable
        self.value = value
        self.op = op

    def eval(self):
        return self.op_func(self.value)

    @property
    def op_func(self):
        if self.op == "greater than":
            return self.context.variables[variable].value.__gt__
        elif self.op == "less than":
            return self.context.variables[variable].value.__lt__
        elif self.op == "greater than or equal to":
            return self.context.variables[variable].value.__ge__
        elif self.op == "less than or equal to":
            return self.context.variables[variable].value.__le__
        elif self.op == "equal to":
            return self.context.variables[variable].value.__eq__
        return None

    def __str__(self):
        return f"{self.variable} {comparison_ops.get(self.op)} {self.value}"
