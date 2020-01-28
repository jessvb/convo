class Error(Exception):
    def __init__(self):
        pass

class InvalidStateError(Error):
    def __init__(self, message):
        self.message = message

class ExecutionError(Error):
    def __init__(self, message):
        self.message = message
