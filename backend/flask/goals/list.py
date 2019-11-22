from goals import *
from models import *

class CreateListActionGoal(BaseGoal):
    def __init__(self, context, name=None):
        super().__init__(context)
        self.setattr("name", name)

    def complete(self):
        assert hasattr(self, "actions")
        self.actions.append(CreateListAction(self.name))
        return super().complete()

    def setattr(self, attr, value):
        if (attr == "name") and value is None:
            self.todos.append(GetInputGoal(self.context, self, attr, f"What do you want to call this list?"))
        setattr(self, attr, value)

class AddToListActionGoal(BaseGoal):
    def __init__(self, context, name=None, value=None):
        super().__init__(context)
        self.setattr("name", name)
        self.setattr("value", value)

    def complete(self):
        assert hasattr(self, "actions")
        self.actions.append(AddToListAction(self.name, self.value))
        return super().complete()

    def setattr(self, attr, value):
        if attr == "name" and value is None:
            self.todos.append(GetInputGoal(self.context, self, attr, f"Which list?"))
        elif attr == "value" and value is None:
            self.todos.append(GetInputGoal(self.context, self, attr, f"What do you want to add?"))
        setattr(self, attr, value)
