class BaseAction(object):
    def __init__(self):
        self.allow_nesting = False
        self.required = []
        self.params = {}
        self.responses = {}

    def is_complete(self):
        for param in self.required:
            if self.params[param] is None:
                return False, self.responses[f"_ask_{param}"]
        return True, self.responses["_complete"]

    def set_params(self, params):
        for param, value in params.items():
            if value is not None and param in self.params:
                self.params[param] = value

    def _python(self):
        raise NotImplementedError

    def _js(self):
        raise NotImplementedError

class ProcedureAction(BaseAction):
    def __init__(self):
        pass

class ListAction(BaseAction):
    def __init__(self):
        pass

class AddListAction(BaseAction):
    def __init__(self):
        pass
