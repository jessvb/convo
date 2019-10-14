class Error(Exception):
   """Base class for other exceptions"""
   pass

class VariableExistsError(Error):
    def __init__(self, name):
        self.message = f"Variable {name} already exists. Try another name."
