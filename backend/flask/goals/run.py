import logging
from goals import *
from models import *

class RunGoal(BaseGoal):
    def __init__(self, context, name=None):
        super().__init__(context)
        self.execution = None
        self.setattr("name", name)

    @property
    def message(self):
        return "Program finished running." if self.is_complete else (self.todos[-1].message if self.todos else None)

    @property
    def is_complete(self):
        return self.context.execution and self.context.execution.done and super().is_complete

    def complete(self):
        message = super().complete()
        logging.debug(f"End of execution variables: {self.execution.variables}")
        self.context.execution = None
        self.context.transition("complete")
        return message

    def setattr(self, attr, value):
        if (attr == "name"):
            if value is None:
                self.todos.append(GetInputGoal(self.context, self, attr, "What do you want to run?"))
            elif value not in self.context.procedures:
                self.todos.append(GetInputGoal(self.context, self, attr, f"Procedure {value} does not exist. Try another name or say cancel."))
            else:
                self.name = value
                self.procedure = self.context.procedures[value]
                self.context.execution = ExecutionContext(self.context, self.procedure.actions)
                self.execution = self.context.execution
                self.advance()
            return
        setattr(self, attr, value)

    def advance(self):
        logging.debug(f"Advancing {self.__class__.__name__}...")
        self.error = None
        if self.todos:
            todo = self.todos.pop()
            todo.advance()
            if todo.is_complete:
                todo.complete()
                self.advance()
            else:
                self.todos.append(todo)

        if self.execution and not self.execution.done:
            todo = self.execution.advance()
            if todo:
                self.todos.append(todo)

class ExecutionContext(object):
    def __init__(self, context, actions):
        self.context = context
        self.actions = actions
        logging.debug(f"Actions: {[str(a) for a in actions]}")
        self.variables = {}
        self.done = False
        self.step = 0

    def advance(self):
        while self.step < len(self.actions):
            action = self.actions[self.step]
            goal = self.evaluate_action(action)
            self.step += 1
            if goal:
                return goal
        self.done = True
    
    def evaluate_action(self, action):
        logging.info(f"==> Evaluating action {str(action)} on step {self.step}")
        if isinstance(action, SayAction):
            phrase = action.phrase
            if isinstance(action.phrase, ValueOf):
                variable = action.phrase.variable
                phrase = f"The value of {variable} is {self.variables[variable]}"
            logging.info(f"Saying '{phrase}'")
            self.context.add_message(action.phrase)
        elif isinstance(action, GetUserInputAction):
            logging.info(f"Getting user input and setting as {action.variable}")
            return GetUserInputGoal(self.context, action.variable)
        elif isinstance(action, CreateVariableAction):
            self.variables[action.name] = self.variables[action.value.variable] if isinstance(action.value, ValueOf) else action.value
            logging.info(f"Created variable {action.name} with value {self.variables[action.name]}")
            logging.info("Current variables:", self.variables)
        elif isinstance(action, SetVariableAction):
            if action.name in self.variables:
                self.variables[action.name] = self.variables[action.value.variable] if isinstance(action.value, ValueOf) else action.value
                logging.info(f"Set variable {action.name} with value {self.variables[action.name]}")
                logging.info("Current variables:", self.variables)
            else:
                logging.warning("Variable not found.")
        elif isinstance(action, IncrementVariableAction):
            value = self.variables.get(action.name)
            if action.name in self.variables:
                old = self.variables[action.name]
                if isinstance(value, float) or isinstance(value, int):
                    self.variables[action.name] += action.value
                elif isinstance(value, ValueOf):
                    self.variables[action.name] += self.variables[action.value.variable]
                new = self.variables[action.name]
                logging.info(f"Incremented variable {action.name} from {old} to {new}")
                logging.info(f"Current variables: {str(self.variables)}")
            else:
                logging.warning("Variable not found.")
        elif isinstance(action, ConditionalAction):
            res = action.condition.eval(self.variables)
            logging.info("Condition for if statement is " + ("true" if res else "false"))
            self.actions[self.step:self.step + 1] = action.actions[res]
            self.step -= 1
        elif isinstance(action, LoopAction):
            res = action.condition.eval(self.variables)
            logging.info("Condition for while loop is " + ("true" if res else "false"))
            if res:
                self.actions[self.step:self.step] = action.actions
            else:
                self.actions[self.step:self.step + 1] = action.actions
            self.step -= 1
