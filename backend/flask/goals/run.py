import logging
import flask_socketio
import copy
from goals import *
from models import *
from error import ExecutionError

class RunGoal(HomeGoal):
    def __init__(self, context, name=None):
        super().__init__(context)
        self.context.transition(self)
        self.execution = None
        self.setattr("name", name)

    @property
    def message(self):
        if self.error:
            return self.error

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
                self.error = f"The procedure, {value}, hasn't been created, so we can't run it. You can create it by saying, \"create a procedure called {value}.\""
                self.context.transition("complete")
            else:
                self.name = value
                self.procedure = self.context.procedures[value]
                self.context.execution = ExecutionContext(self.context, [copy.copy(a) for a in self.procedure.actions])
                self.execution = self.context.execution
                todo = self.execution.advance()
                if self.execution.error:
                    self.error = self.execution.error
                    self.context.transition("complete")
                if todo:
                    self.todos.append(todo)
            return
        setattr(self, attr, value)

    def advance(self):
        logging.debug(f"Advancing {self.__class__.__name__}...")
        self._message = None
        if self.todos:
            todo = self.todos.pop()
            todo.advance()
            if todo.is_complete:
                todo.complete()
            else:
                self.todos.append(todo)

        if self.execution and not self.execution.done:
            todo = self.execution.advance()
            if self.execution.error:
                self.error = self.execution.error
                self.context.transition("complete")
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
        self.error = None

    def advance(self):
        while self.step < len(self.actions):
            action = self.actions[self.step]
            try:
                goal = self.evaluate_action(action)
            except KeyError as e:
                self.error = f"Error occured while running. Variable {e.args[0]} did not exist when I was {action.to_nl()}."
                break
            except ExecutionError as e:
                self.error = e.message
                break

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
                phrase = f"The value of {variable} is {self.variables[variable]}."
            logging.info(f"Saying '{phrase}'")
            try:
                flask_socketio.emit("response", { "message": phrase, "state": self.context.state }, room=str(self.context.sid))
                print(f"Emitting to {self.context.sid}")
            except RuntimeError as e:
                if not str(e).startswith("Working outside of request context."):
                    raise e
            self.context.add_message(action.phrase)
        elif isinstance(action, PlaySoundAction):
            logging.info(f"Playing sound file {action.sound}.")
            try:
                flask_socketio.emit("playSound", { "sound": action.sound, "state": self.context.state }, room=str(self.context.sid))
                print(f"Emitting to {self.context.sid}")
            except RuntimeError as e:
                if not str(e).startswith("Working outside of request context."):
                    raise e
        elif isinstance(action, GetUserInputAction):
            logging.info(f"Getting user input and setting as {action.variable}")
            return GetUserInputGoal(self.context, action.variable)
        elif isinstance(action, CreateVariableAction):
            self.variables[action.name] = self.variables[action.value.variable] if isinstance(action.value, ValueOf) else action.value
            logging.info(f"Created variable {action.name} with value {self.variables[action.name]}")
            logging.info(f"Current variables: {str(self.variables)}")
        elif isinstance(action, SetVariableAction):
            if action.name in self.variables:
                self.variables[action.name] = self.variables[action.value.variable] if isinstance(action.value, ValueOf) else action.value
                logging.info(f"Set variable {action.name} with value {self.variables[action.name]}")
                logging.info(f"Current variables: {str(self.variables)}")
            else:
                logging.warning("Variable not found.")
                raise KeyError(action.name)
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
                raise KeyError(action.name)
        elif isinstance(action, ConditionalAction):
            res = action.condition.eval(self.variables)
            logging.info(f"Condition for if statement ({str(action.condition)}) is " + ("true" if res else "false"))
            logging.info(f"Current variables: {str(self.variables)}")
            self.actions[self.step:self.step + 1] = action.actions[res]
            self.step -= 1
        elif isinstance(action, UntilLoopAction):
            res = action.condition.eval(self.variables)
            logging.info(f"Condition for until loop ({str(action.condition)}) is " + ("true" if res else "false"))
            logging.info(f"Current variables: {str(self.variables)}")
            if not res:
                self.actions[self.step:self.step] = action.actions
                self.step -= 1
        elif isinstance(action, WhileLoopAction):
            res = action.condition.eval(self.variables)
            logging.info(f"Condition for while loop ({str(action.condition)}) is " + ("true" if res else "false"))
            logging.info(f"Current variables: {str(self.variables)}")
            if res:
                self.actions[self.step:self.step] = action.actions
                self.step -= 1
