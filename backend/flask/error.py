class Error(Exception):
    def __init__(self):
        pass

class InvalidStateError(Error):
    def __init__(self, state, goal):
        self.message = f"Cannot perform goal {goal} in state {state}"

class ExecutionError(Error):
    def __init__(self, message):
        self.message = message
