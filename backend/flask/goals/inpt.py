class GetInputGoal(object):
    def __init__(self, context, goal, inpt, message):
        self.context = context
        self.goal = goal
        self.input = inpt
        self.value = None
        self._message = message

    @property
    def is_complete(self):
        return self.value is not None

    @property
    def message(self):
        return "Done!" if self.is_complete else self._message

    def try_complete(self):
        if not self.is_complete:
            self.pursue()

        if self.is_complete:
            print(f"Completing GetInputGoal({self.input}, {self.value})")
            self.goal.todos.pop()
            self.goal.setattr(self.input, self.value)

        return self.message

    def pursue(self):
        print("Pursuing GetInputGoal")
        self.value = self.context.current_message

    def __str__(self):
        return "get_input"