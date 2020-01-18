from goals import *
from models import *

class RunGoal(BaseGoal):
    def __init__(self, context, name=None):
        super().__init__(context)
        self.execution = None
        self.setattr("name", name)

    @property
    def message(self):
        return "Program finished running." if self.is_complete else "Advancing program."

    @property
    def is_complete(self):
        return self.execution.done and super().is_complete

    def setattr(self, attr, value):
        if (attr == "name"):
            if value is None:
                self.todos.append(GetInputGoal(self.context, self, attr, "What do want to run?"))
            elif value not in self.context.procedures:
                self.todos.append(GetInputGoal(self.context, self, attr, f"Procedure {value} does not exist. Try another name or say cancel."))
            else:
                print("Creating execution context...")
                self.name = value
                self.procedure = self.context.procedures[value]
                self.execution = ExecutionContext(self.procedure.actions)

                while not self.execution.done:
                    todo = self.execution.advance()
                    if todo:
                        self.todos.append(todo)
                        break
            return
        setattr(self, attr, value)

    def advance(self):
        print(f"Advancing {self.__class__.__name__}...")
        self.error = None
        while not self.execution.done:
            todo = self.execution.advance()
            if todo:
                self.todos.append(todo)
                break
        if self.todos:
            todo = self.todos.pop()
            todo.advance()
            if todo.is_complete:
                todo.complete()
            else:
                self.todos.append(todo)

class ExecutionContext(object):
    def __init__(self, actions):
        self.actions = actions
        self.variables = {}
        self.done = False
        self.step = 0

    def advance(self):
        print("Advancing program")
        while self.step < len(self.actions):
            action = self.actions[self.step]
            self.evaluate_action(action)
            self.step += 1
        self.done = True
        return None
    
    def evaluate_action(self, action):
        print(f"==> Evaluating action {str(action)} on step {self.step}")
        if isinstance(action, SayAction):
            print("Saying", action.phrase)
        if isinstance(action, CreateVariableAction):
            self.variables[action.name] = action.value
            print(f"Created variable {action.name} with value {action.value}")
            print("Current variables:", self.variables)
        elif isinstance(action, SetVariableAction):
            if action.name in self.variables:
                self.variables[action.name] = action.value
                print(f"Set variable {action.name} with value {action.value}")
                print("Current variables:", self.variables)
            else:
                print("Variable not found.")
        elif isinstance(action, IncrementVariableAction):
            value = self.variables.get(action.name)
            if action.name in self.variables and (isinstance(value, float) or isinstance(value, int)):
                old = self.variables[action.name]
                self.variables[action.name] += action.value
                new = self.variables[action.name]
                print(f"Incremented variable {action.name} with value {action.value} from {old} to {new}")
                print("Current variables:", self.variables)
            else:
                print("Variable not found.")
        elif isinstance(action, ConditionalAction):
            res = action.condition.eval(self.variables)
            print("Condition for if statement is " + ("true" if res else "false"))
            self.actions[self.step:self.step + 1] = action.actions[res]
            self.step -= 1
        elif isinstance(action, LoopAction):
            res = action.condition.eval(self.variables)
            print("Condition for while loop is " + ("true" if res else "false"))
            if res:
                self.actions[self.step:self.step] = action.actions
            else:
                self.actions[self.step:self.step + 1] = action.actions
            self.step -= 1
