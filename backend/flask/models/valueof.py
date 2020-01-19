class ValueOf(object):
    def __init__(self, variable):
        self.variable = variable

    def eval(self, variables):
        return variables.get(self.variable, None)
