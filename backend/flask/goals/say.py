from models import *
from goals import *

class SayGoal(object):
    def __init__(self, context, phrase=None):
        self.context = context
        self.todos = []
        self.setattr("phrase", phrase)

    @property
    def is_complete(self):
        return len(self.todos) == 0

    @property
    def message(self):
        if self.is_complete:
            return "SayGoal completed!"

        return self.todos[-1].message

    def setattr(self, attr, value):
        if attr == "phrase":
            if value is None:
                self.todos.append(GetInputGoal(self.context, self, attr, f"What do you want me to say?"))
            else:
                self.phrase = value
        else:
            setattr(self, attr, value)

    def try_complete(self):
        if not self.is_complete:
            self.pursue()

        if self.is_complete:
            print("Completing SayGoal")
            self.actions.append(SayAction(self.phrase))
            self.goal.todos.pop()

        return self.message

    def pursue(self):
        print("Pursuing SayGoal")
        self.todos[-1].try_complete()

    def __str__(self):
        return "say" + (f":{str(self.todos[-1])}" if self.todos else "")