from models import *
from goals import *

class AnalyzeSentimentAnalysisActionGoal(ActionGoal):
    """Goal for adding a say action"""
    def __init__(self, context, phrase=None):
        super().__init__(context)
        self.setattr("phrase", phrase)
        # self.setattr("variable", None)

    def complete(self):
        assert hasattr(self, "actions")
        self.actions.append(AnalyzeSentimentAnalysisAction(self.phrase))

        return super().complete()

    def setattr(self, attr, value):
        if attr == "phrase":
            if value is None:
                self.todos.append(GetInputGoal(self.context, self, attr, f"What do you want me to analyze the sentiment of?"))
            elif isinstance(value, ValueOf):
                if value.variable not in self.variables:
                    self.error = f"Variable, {value.variable}, hasn't been created. Try using an existing variable if you want to try again."
                    return
                self.phrase = value
            else:
                self.phrase = value
            return
        # if attr == "variable":
        #     if value is None:
        #         self.todos.append(GetInputGoal(self.context, self, attr, f"What do you want to call the variable?"))
        #     elif value in self.variables:
        #         self.error = f"The name, {value}, has already been used. Try creating a variable with another name."
        #     else:
        #         self.name = value
        #     return
        setattr(self, attr, value)
