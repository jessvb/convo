class Error(Exception):
    """Custom base error for server"""
    def __init__(self):
        pass

class InvalidStateError(Error):
    """For errors that occur from attempting to perform a goal in the wrong state"""
    def __init__(self, goal, state):
        self.goal = goal
        self.state = state
        self.message = f"Cannot create goal {str(goal)} in state {self.state}"

class ExecutionError(Error):
    """For errors that occur during execution of procedures"""
    def __init__(self, message):
        self.message = message
