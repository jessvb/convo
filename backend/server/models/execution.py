import logging
import copy
import threading
import time

from app import sio
from error import *
from models import *
from helpers import *

logger = logging.getLogger("gunicorn.error")

class Execution(object):
    def __init__(self, context, actions, to_emit=True):
        self.context = context
        self.actions = actions
        self.variables = {}
        self.step = 0
        self.input_needed = None
        self.thread_running = False
        self.finished = False
        self.to_emit = to_emit

    def run(self, message=None):
        if self.input_needed and message:
            self.variables[self.input_needed] = parse_number(message)
            logger.info(f"Current variables: {str(self.variables)}")
            self.input_needed = None
        self.thread = threading.Thread(target=self.advance)
        self.thread.daemon = True
        self.thread_running = True
        self.thread.start()

    def stop(self):
        self.thread_running = False

    def finish(self, message=None):
        self.stop()
        self.finished = True
        self.context.transition("finish")
        self.context.execution = None
        if message:
            self.emit("response", { "message": message, "state": self.context.state })

    def advance(self):
        while self.thread_running and not self.finished and self.step < len(self.actions):
            action = self.actions[self.step]
            try:
                self.evaluate_action(action)
                self.step += 1
                sio.sleep(0.5)
                if self.input_needed:
                    self.stop()
                    return
            except KeyError as e:
                self.finish(f"Error occured while running. Variable {e.args[0]} did not exist when I was {action.to_nl()}.")
                return
            except ExecutionError as e:
                self.finish(e.message)
                return

            if self.step >= len(self.actions):
                break

        if not self.finished:
            self.finish("Procedure finished running.")

    def emit(self, event, data):
        if not self.to_emit:
            return

        try:
            message = f" with the message: {data['message']}" if "message" in data else ""
            logger.info(f"Emitting event {event} to client {self.context.sid}{message}.")
            sio.emit(event, data, room=str(self.context.sid))
        except RuntimeError as e:
            logger.info(e)
            if not str(e).startswith("Working outside of request context."):
                raise e

    def evaluate_action(self, action):
        logger.info(f"==> Evaluating action {str(action)} on step {self.step}")
        if isinstance(action, SayAction):
            phrase = action.phrase
            if isinstance(action.phrase, ValueOf):
                variable = action.phrase.variable
                phrase = f"The value of {variable} is \"{self.variables[variable]}\"."
            logger.info(f"Saying '{phrase}'")
            self.emit("response", { "message": phrase, "state": self.context.state })
            self.context.add_message(action.phrase)
        elif isinstance(action, PlaySoundAction):
            logger.info(f"Playing sound file {action.sound}.")
            self.emit("playSound", { "sound": action.sound, "state": self.context.state })
        elif isinstance(action, GetUserInputAction):
            logger.info(f"Getting user input and setting as {action.variable}")
            self.input_needed = action.variable
            self.emit("response", { "message": "Listening for user input...", "state": self.context.state })
        elif isinstance(action, CreateVariableAction):
            self.variables[action.name] = self.variables[action.value.variable] if isinstance(action.value, ValueOf) else action.value
            logger.info(f"Created variable {action.name} with value {self.variables[action.name]}")
            logger.info(f"Current variables: {str(self.variables)}")
        elif isinstance(action, SetVariableAction):
            if action.name in self.variables:
                self.variables[action.name] = self.variables[action.value.variable] if isinstance(action.value, ValueOf) else action.value
                logger.info(f"Set variable {action.name} with value {self.variables[action.name]}")
                logger.info(f"Current variables: {str(self.variables)}")
            else:
                logger.info("Variable not found.")
                raise KeyError(action.name)
        elif isinstance(action, AddToVariableAction) or isinstance(action, SubtractFromVariableAction):
            value = self.variables.get(action.name)
            if action.name in self.variables:
                old = self.variables[action.name]
                factor = 1 if isinstance(action, AddToVariableAction) else -1
                if isinstance(value, float) or isinstance(value, int):
                    self.variables[action.name] += factor * action.value
                elif isinstance(value, ValueOf):
                    self.variables[action.name] += factor * self.variables[action.value.variable]
                new = self.variables[action.name]
                if isinstance(action, AddToVariableAction):
                    logger.info(f"Incremented variable {action.name} from {old} to {new}")
                else:
                    logger.info(f"Decremented variable {action.name} from {old} to {new}")
                logger.info(f"Current variables: {str(self.variables)}")
            else:
                logger.info("Variable not found.")
                raise KeyError(action.name)
        elif isinstance(action, ConditionalAction):
            res = action.condition.eval(self.variables)
            logger.info(f"Condition for if statement ({str(action.condition)}) is " + ("true" if res else "false"))
            logger.info(f"Current variables: {str(self.variables)}")
            self.actions[self.step:self.step + 1] = action.actions[res]
            self.step -= 1
        elif isinstance(action, LoopAction):
            res = action.condition.eval(self.variables)
            logger.info(f"Condition for {action.loop} loop ({str(action.condition)}) is " + ("true" if res else "false"))
            logger.info(f"Current variables: {str(self.variables)}")
            if (action.loop == "until" and not res) or (action.loop == "while" and res):
                self.actions[self.step:self.step] = action.actions
                self.step -= 1
        else:
            raise NotImplementedError
