class Error(Exception):
   """Base class for other exceptions"""
   def __init__(self, message):
       self.message = message

class VariableExistsError(Error):
    def __init__(self, name):
        Error.__init__(self, f"Variable {name} already exists. Try another name.")

class InputError(Error):
    def __init__(self, message):
        Error.__init__(self, message)
