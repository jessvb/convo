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
        if self.op == ">":
            return self.context.variables[variable].value.__gt__
        elif self.op == "<":
            return self.context.variables[variable].value.__lt__
        else:
            return self.context.variables[variable].value.__eq__
        return None

    def __str__(self):
        return f"{self.variable} {self.op} {self.value}"
