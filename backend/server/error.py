class Error(Exception):
    def __init__(self):
        pass

class InvalidStateError(Error):
    def __init__(self, goal, state):
        self.goal = goal
        self.state = state
        self.message = f"Cannot create goal {str(goal)} in state {self.state}"

class ExecutionError(Error):
    def __init__(self, message):
        self.message = message
