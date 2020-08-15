import copy
import threading
import time

from app import sio, logger
from error import *
from models import *
from helpers import *

class Execution(object):
    """
    Represents an execution of a procedure

    Executes the procedure in a child thread such that the server does not have to
    wait for execution to finish before performing other actions - this way multiple users
    can send messages at once and allow for users to stop execution of a procedure before it
    finishes - allowing for stopping of infinite loops.
    """
    def __init__(self, context, actions, to_emit=True):
        self.context = context
        self.actions = actions
        self.variables = {}
        self.step = 0
        self.input_needed = None
        self.thread_running = False
        self.finished = False
        self.to_emit = to_emit
        self.first_message_emitted = False

    def run(self, message=None):
        """
        Starts execution

        Execution starts essentially from two different states:
        1. From the beginning of a procedure
        2. After asking for user input, execution starts again with user's next message as input
        """
        if self.input_needed and message:
            # If input was needed, try to parse message and if it's a number try to parse number
            number = parse_number(message)
            self.variables[self.input_needed] = number if number is not None else message
            logger.debug(f"[{self.context.sid}][Execution] Variables after getting input: {str(self.variables)}")
            self.input_needed = None
        self.thread = threading.Thread(target=self.advance)

        # Means if the main thread stops (the server), this thread will also stop
        self.thread.daemon = True
        self.thread_running = True

        if not self.first_message_emitted:
            self.emit("response", { "message": "Procedure started running.", "state": self.context.state, "speak": False })
            logger.debug(f"[{self.context.sid}][Execution] Procedure started running.")
            self.first_message_emitted = True

        logger.debug(f"[{self.context.sid}][Execution] Thread started running.")
        self.thread.start()

    def stop(self):
        """Stop execution"""
        self.thread_running = False

    def finish(self, message=None):
        """Finish up execution"""
        self.stop()
        self.finished = True

        # Transition from "running" state to "home" state
        self.context.transition("finish")
        self.context.execution = None
        if message is not None:
            logger.debug(f"[{self.context.sid}][Execution] Execution stopped with message: {message}")
            self.emit("response", { "message": message, "state": self.context.state })

    def advance(self):
        """Continue execution"""
        while self.thread_running and not self.finished and self.step < len(self.actions):
            action = self.actions[self.step]
            try:
                # Tries to evaluate action
                self.evaluate_action(action)
                self.step += 1
                sio.sleep(0.1)
                if self.input_needed:
                    # If input is needed (i.e. reaches a GetUserInputAction), stop execution and ask user for input
                    self.stop()
                    return
            except KeyError as e:
                # Error when variable referenced does not exist
                logger.debug(f"[{self.context.sid}][Execution] KeyError: {e.args[0]}")
                self.finish(f"Error occured while running. Variable {e.args[0]} did not exist when I was {action.to_nl()}.")
                return
            except ExecutionError as e:
                # Error that happens during execution like infinite loops, etc.
                logger.debug(f"[{self.context.sid}][Execution] ExecutionError: {e.message}")
                self.finish(e.message)
                return

            if self.step >= len(self.actions):
                break

        if not self.finished:
            self.finish("Procedure finished running.")

    def emit(self, event, data):
        """Emit or send message to user via sockets"""
        if not self.to_emit:
            return

        try:
            message = f" with the message: {data['message']}" if "message" in data else "."
            logger.debug(f"[{self.context.sid}][Execution] Emitting '{event}'{message}")
            sio.emit(event, data, room=str(self.context.sid))
        except RuntimeError as e:
            logger.debug(f"[{self.context.sid}][Execution] RuntimeError: {str(e)}")
            if not str(e).startswith("Working outside of request context."):
                raise e

    def evaluate_action(self, action):
        """Evaluates an action"""
        logger.debug(f"[{self.context.sid}][Execution][Evaluating] Evaluating action {str(action)} on step {self.step}.")
        if isinstance(action, SayAction):
            phrase = action.phrase
            if isinstance(action.phrase, ValueOf):
                variable = action.phrase.variable
                phrase = f"The value of {variable} is \"{self.variables[variable]}\"."
            logger.debug(f"[{self.context.sid}][Execution][Evaluating] Saying '{phrase}'")
            self.emit("response", { "message": phrase, "state": self.context.state })
            self.context.add_message(action.phrase)
        elif isinstance(action, GreetAction):
            greeting = "Hello world!"
            logger.debug(f"[{self.context.sid}][Execution][Evaluating] Greeting with '{greeting}'")
            self.emit("response", { "message": greeting, "state": self.context.state })
            self.context.add_message(greeting)
        elif isinstance(action, PlaySoundAction):
            logger.debug(f"[{self.context.sid}][Execution][Evaluating] Playing sound file {action.sound}.")
            self.emit("playSound", { "sound": action.sound, "state": self.context.state })
        elif isinstance(action, GetUserInputAction):
            logger.debug(f"[{self.context.sid}][Execution][Evaluating] Getting user input and setting as {action.variable}.")
            self.input_needed = action.variable
            if action.prompt:
                self.emit("response", { "message": action.prompt, "state": self.context.state })
        elif isinstance(action, CreateVariableAction):
            self.variables[action.variable] = self.variables[action.value.variable] if isinstance(action.value, ValueOf) else action.value
            logger.debug(f"[{self.context.sid}][Execution][Evaluating] Creating variable {action.variable} with value {self.variables[action.variable]}.")
            logger.debug(f"[{self.context.sid}][Execution][Evaluating] Variables after creating variable: {str(self.variables)}")
        elif isinstance(action,GenerateTextAction):
            logger.debug(f"Inside execution.py")
            logger.debug(f"[{self.context.sid}][Execution][Evaluating] Generate text in {action.style} style with {action.prefix} to start with")
            logger.debug(f"[{self.context.sid}][Execution][Evaluating] Text length: {action.length}")
            phrase = f"When I get the model working, I will generate {action.length} of {action.style} styled text that begins with {action.prefix}. Stay tuned! "
            self.emit("response", {"message":phrase,"state":self.context.state})
        elif isinstance(action, SetVariableAction):
            if action.variable in self.variables:
                self.variables[action.variable] = self.variables[action.value.variable] if isinstance(action.value, ValueOf) else action.value
                logger.debug(f"[{self.context.sid}][Execution][Evaluating] Setting variable {action.variable} with value {self.variables[action.variable]}.")
                logger.debug(f"[{self.context.sid}][Execution][Evaluating] Variables after setting variable: {str(self.variables)}")
            else:
                logger.debug(f"[{self.context.sid}][Execution][Evaluating] Variable {action.variable} not found.")
                raise KeyError(action.variable)
        elif isinstance(action, AddToVariableAction) or isinstance(action, SubtractFromVariableAction):
            value = self.variables.get(action.variable)
            if action.variable in self.variables:
                old = self.variables[action.variable]
                factor = 1 if isinstance(action, AddToVariableAction) else -1
                if isinstance(value, float) or isinstance(value, int):
                    self.variables[action.variable] += factor * action.value
                elif isinstance(value, ValueOf):
                    self.variables[action.variable] += factor * self.variables[action.value.variable]
                new = self.variables[action.variable]
                if isinstance(action, AddToVariableAction):
                    logger.debug(f"[{self.context.sid}][Execution][Evaluating] Incrementing variable {action.variable} from {old} to {new}.")
                    logger.debug(f"[{self.context.sid}][Execution][Evaluating] Variables after incrementing variable: {str(self.variables)}")
                else:
                    logger.debug(f"[{self.context.sid}][Execution][Evaluating] Decrementing variable {action.variable} from {old} to {new}.")
                    logger.debug(f"[{self.context.sid}][Execution][Evaluating] Variables after decrementing variable: {str(self.variables)}")
            else:
                logger.debug(f"[{self.context.sid}][Execution][Evaluating] Variable {action.variable} not found.")
                raise KeyError(action.variable)
        elif isinstance(action, ConditionalAction):
            res = action.condition.eval(self.variables)
            logger.debug(f"[{self.context.sid}][Execution][Evaluating] Evaluating condition for if statement.")
            logger.debug(f"[{self.context.sid}][Execution][Evaluating] Variables when evaluating condition: {str(self.variables)}")
            logger.debug(f"[{self.context.sid}][Execution][Evaluating] Condition for if statement ({str(action.condition)}) is " + ("true" if res else "false"))
            self.actions[self.step:self.step + 1] = action.actions[res]
            self.step -= 1
        elif isinstance(action, LoopAction):
            if (action.loop == "until" and isinstance(action.condition, UntilStopCondition)):
                res = False
            else:
                res = action.condition.eval(self.variables)
            logger.debug(f"[{self.context.sid}][Execution][Evaluating] Evaluating condition for {action.loop} loop.")
            logger.debug(f"[{self.context.sid}][Execution][Evaluating] Variables when evaluating condition: {str(self.variables)}")
            logger.debug(f"[{self.context.sid}][Execution][Evaluating] Condition for {action.loop} loop ({str(action.condition)}) is " + ("true" if res else "false"))
            if (action.loop == "until" and not res) or (action.loop == "while" and res):
                self.actions[self.step:self.step] = action.actions
                self.step -= 1
        else:
            raise NotImplementedError

class InternalExecution(Execution):
    """Execution that is ran internally without user knowing - used in user study to check advanced scenarios"""
    def __init__(self, context, actions, inputs):
        super().__init__(context, actions)
        self.inputs = inputs
        self.iterinputs = iter(inputs)
        self.emits = []
        self.original_length = len(actions)

    def advance(self):
        while self.step < len(self.actions):
            action = self.actions[self.step]
            try:
                self.evaluate_action(action)
                self.step += 1
                if self.input_needed:
                    message = next(self.iterinputs)
                    number = parse_number(message)
                    self.variables[self.input_needed] = number if number is not None else message
                    logger.debug(f"[{self.context.sid}][Execution] Variables after getting input: {str(self.variables)}")
                    self.input_needed = None
            except KeyError as e:
                logger.debug(f"[{self.context.sid}][Execution] KeyError: {e.args[0]}")
                return "KeyError"
            except ExecutionError as e:
                logger.debug(f"[{self.context.sid}][Execution] ExecutionError: {e.message}")
                return "ExecutionError"
            except StopIteration as e:
                logger.debug(f"[{self.context.sid}][Execution] StopIteration: Too many inputs needed.")
                return "StopIteration"

            if len(self.actions) > self.original_length * 100:
                logger.debug(f"[{self.context.sid}][Execution] Infinite loop detected.")
                return "InfiniteLoop"

        self.finish()
        return None

    def run(self):
        logger.debug(f"[{self.context.sid}][Execution] Starting to check procedure.")
        logger.debug(f"[{self.context.sid}][Execution] Actions: {[str(a) for a in self.actions]}")
        logger.debug(f"[{self.context.sid}][Execution] Inputs: {self.inputs}.")
        return self.advance()

    def finish(self):
        logger.debug(f"[{self.context.sid}][Execution] Finishing checking procedure.")
        logger.debug(f"[{self.context.sid}][Execution] Emits: {self.emits}.")
        self.finished = True

    def emit(self, event, data):
        """Add to list of emits instead of actually sending responses to user"""
        self.emits.append((event, data))
