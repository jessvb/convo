class Error(Exception):
    def __init__(self):
        pass

class InvalidStateError(Error):
    def __init__(self):
        self.message = "Cannot do in this state."