import re
from utils import to_snake_case

class BaseGoal(object):
    def __init__(self, context):
        self.error = None
        self.context = context
        self.todos = []

    @property
    def is_complete(self):
        return len(self.todos) == 0

    @property
    def message(self):
        if self.error:
            return self.error
        return f"{self.__class__.__name__} completed!" if self.is_complete else self.todos[-1].message

    def advance(self):
        print(f"Advancing {self.__class__.__name__}...")
        self.error = None
        if self.todos:
            todo = self.todos.pop()
            todo.advance()
            if todo.is_complete:
                todo.complete()
            else:
                self.todos.append(todo)

    def complete(self):
        print(f"{self.__class__.__name__} completed!")
        return self.message

    def setattr(self, attr, value):
        setattr(self, attr, value)

    def __str__(self):
        name = self.__class__.__name__
        return to_snake_case(name[:-len("Goal")]) + (f":{str(self.todos[-1])}" if self.todos else "")
