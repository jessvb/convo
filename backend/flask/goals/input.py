from goals import *

class GetInputGoal(BaseGoal):
    def __init__(self, context, obj, attr, message):
        super().__init__(context)
        self.obj = obj
        self.input = attr
        self.value = None
        self._message = message

    @property
    def is_complete(self):
        return self.value is not None

    @property
    def message(self):
        return "GetInputGoal completed!" if self.is_complete else self._message

    def advance(self):
        print(f"Advancing {self.__class__.__name__}...")
        self.value = self.context.current_message

    def complete(self):
        self.obj.setattr(self.input, self.value)
        return super().complete()
