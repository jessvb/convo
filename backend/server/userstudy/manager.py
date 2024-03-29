import copy

from dialog import *
from manage import sio
from app import logger
from goals import *
from models import *
from question import *
from nlu import *

class UserStudyDialogManager(DialogManager):
    """
    Special dialog manager used for practice and novice scenarios in user study.

    The main difference between this dialog manager and the default is the check that occurs after each message from client.
    The manager checks if the user is properly going towards the goal given each message.

    The manager allows for slot-filling in conversations if it goes towards the next goal.
    For example, if instruction was to say "Create a variable called count", the dialog manager would accept "Create a variable"
    followed by "count". However if the second message was not "count" it will still flag as not going towards goal.

    If user strays from scenario completion, the dialog manager resets back to the last state/context that was going towards scenario completion.
    This is done by referencing a default reference dialog manager that is fed the next instruction of the scenario whenever user completes each
    instruction.

    Once scenario is completed, the dialog manager switches to default behavior where user can do whatever.
    """
    def __init__(self, sid, stage, part, scenario):
        super().__init__(sid)
        self.scenario = scenario
        self.stage = stage
        self.part = part
        self.step = 0
        self.reference = DialogManager(sid)
        self.last_parsed_goal = None
        self.backup_context = copy.deepcopy(self.context)
        self.backup_reference_context = copy.deepcopy(self.reference.context)
        logger.debug(f"[{sid}][{stage},{part}] Scenario: \n{scenario}")

    @property
    def scenario_completed(self):
        """Check if scenario is completed"""
        return self.step >= len(self.scenario)

    def reset(self, to_backup=False):
        """Resets the dialog manager"""
        if to_backup:
            # If a backup is provided, resets to the backup
            logger.debug(f"[{self.sid}][{self.stage},{self.part}] User did not follow instructions, so resetting to previous back up.")
            self.context = copy.deepcopy(self.backup_reference_context)
            self.qa = QuestionAnswer(self.context)
            self.nlu = SemanticNLU(self.context)
            self.last_parsed_goal = None
            response = "Conversation and objective has been reset to previous back up. What do you want to do first?"
        else:
            logger.debug(f"[{self.sid}][{self.stage},{self.part}] Resetting the entire conversation and scenario.")
            self.context.reset()
            self.context.procedures = { }
            self.context.execution = None
            self.reference.reset()
            self.reference.context.procedures = { }
            self.reference.context.execution = None
            self.last_parsed_goal = None
            self.step = 0
            response = "Conversation and the objective has been reset. What do you want to do first?"
            sio.emit("stepUpdate", { "step": self.step }, room=str(self.sid))

        self.backup_context = copy.deepcopy(self.context)
        return response

    @property
    def next_message(self):
        """Retrives the next instruction message of the scenario"""
        if self.step >= len(self.scenario):
            return None

        message = self.scenario[self.step][0]
        self.step += 1
        return message

    @property
    def immediate_goal(self):
        """Returns the immediate, lowest-level current goal"""
        current = self.context.current_goal
        while current and current.todos:
            current = current.todos[-1]
        return current

    def handle_message(self, message):
        if self.step >= len(self.scenario):
            logger.debug(f"[{self.sid}][{self.stage},{self.part}] Finished the goal, so using default handling.")
            return super().handle_message(message)

        if not isinstance(self.immediate_goal, GetInputGoal):
            self.backup_context = copy.deepcopy(self.context)
            self.backup_reference_context = copy.deepcopy(self.reference.context)

        self.context.add_message(message)

        response = self.handle_reset(message)
        if response is not None:
            logger.info(f"[{self.sid}][{self.stage},{self.part}] User resetted.")
            return response

        response = self.handle_help(message)
        if response is not None:
            logger.info(f"[{self.sid}][{self.stage},{self.part}] User needed help.")
            return response

        if self.context.state == "executing":
            logger.debug(f"[{self.sid}][{self.stage},{self.part}] Program is currently executing.")
            return self.handle_execution(message)

        response = self.handle_question(message)
        if response is not None:
            logger.info(f"[{self.sid}][{self.stage},{self.part}] User asked a question.")
            return response

        response = self.handle_parse(message)
        if response is not None:
            return response

        response = self.check_goal(message)
        if response is not None:
            return response

        response = self.handle_goal()

        return response

    def handle_parse(self, message):
        if self.step >= len(self.scenario):
            # If scenario is completed, use the default dialog manager to manage conversation
            logger.debug(f"[{self.sid}][{self.stage},{self.part}] User has completed the objective, so parsing normally.")
            return super().handle_parse(message)

        try:
            self.context.parsed = self.nlu.parse_message(message)
        except InvalidStateError as e:
            logger.debug(f"[{self.sid}][{self.stage},{self.part}] Action cannot be done in current state.")
            return "I can't do this right now. Please follow instructions and try again!"

    def check_goal(self, message):
        """Check if message or parsed goal is valid in the scenario"""
        goal = self.context.parsed
        if self.scenario[self.step][1] == type(goal):
            self.last_parsed_goal = goal
            logger.debug(f"[{self.sid}][{self.stage},{self.part}] User goal is the same type of the current objective goal.")
            return None
        elif self.immediate_goal and isinstance(self.immediate_goal, GetInputGoal):
            # It's fine if currently slot-filling
            logger.debug(f"[{self.sid}][{self.stage},{self.part}] Current goal is for getting user input so ignoring.")
            return None
        elif goal:
            # Parsed goal was not the same as scenario at that step
            logger.debug(f"[{self.sid}][{self.stage},{self.part}] User goal does not match the current objective goal.")
            return "I think this is the wrong action. Please follow the instructions and try again!"
        elif self.scenario[self.step][1] is None and message == self.scenario[self.step][0]:
            # If current instruction was simply a message like "done" or "close loop", just check if message is the same as the instruction
            logger.debug(f"[{self.sid}][{self.stage},{self.part}] User message matches the current objective message: {message}")
            return None
        else:
            logger.info(f"[{self.sid}][{self.stage},{self.part}] Did not understand utterance: {self.context.current_message}")
            return "I didn't quite catch that. Please follow the instructions and try again!"

    def handle_reset(self, message):
        """Check for reset"""
        if message.lower() == "reset":
            return self.reset()

    def handle_goal(self):
        if self.step >= len(self.scenario):
            # If scenario is completed, handle goal like in default dialog manager
            logger.debug(f"[{self.sid}][{self.stage},{self.part}] User has completed the objective, so handling goal normally.")
            return super().handle_goal()

        if self.current_goal() is None:
            goal = self.context.parsed
            if goal is None or not isinstance(goal, BaseGoal):
                logger.info(f"[{self.sid}][{self.stage},{self.part}] Did not understand utterance: {self.context.current_message}")
                logger.debug(f"[{self.sid}][{self.stage},{self.part}] No current goal nor parsed goal so could not understand.")
                return "I didn't understand what you were saying. Please try again."
            elif goal.error:
                self.reset(to_backup=True)
                logger.debug(f"[{self.sid}][{self.stage},{self.part}] Current goal had an error.")
                return "I think your action is slightly wrong. Please try again!"
            elif goal.is_complete:
                response = goal.complete()
            else:
                response = goal.message
                self.context.add_goal(goal)
        else:
            goal = self.current_goal()
            goal.advance()

            if goal.error or (self.last_parsed_goal and self.last_parsed_goal.error):
                self.reset(to_backup=True)
                logger.debug(f"[{self.sid}][{self.stage},{self.part}] Current goal had an error.")
                return "I think your action is slightly wrong. Please follow the instructions and try again."
            elif goal.is_complete:
                response = goal.complete()
                self.context.goals.pop()
            else:
                response = goal.message

        if not isinstance(self.immediate_goal, GetInputGoal) and (self.last_parsed_goal and not self.last_parsed_goal.error):
            # If not slot-filling and there's no error in the goal, feed the instruction to the reference dialog manager unless it's to run the program
            next_message = self.next_message
            logger.debug(f"[{self.sid}][{self.stage},{self.part}] Tentatively moving on to step {self.step} of the scenario.")
            if not next_message.startswith("run"):
                # Do not feed a "run" command to reference DM or else program will run twice (one from reference DM and one by the user)
                self.reference.handle_message(next_message)

        if isinstance(self.immediate_goal, GetActionsGoal):
            # Check if current lowest-level goal is to get actions for a procedure, if so, check if the actions are correct as the ones in the reference DM's procedure
            wrong_procedure = isinstance(self.last_parsed_goal, CreateProcedureGoal) and self.context.current.name != self.reference.context.current.name
            wrong_action = self.context.current.actions != self.reference.context.current.actions

            if wrong_procedure or wrong_action:
                # If actions are not the same, reset to the last usable backup for context and undoing the instruction command in the reference DM
                self.reset(to_backup=True)
                self.reference.reset(self.backup_reference_context)
                self.step = max(self.step - 1, 0)
                if wrong_procedure:
                    logger.debug(f"[{self.sid}][{self.stage},{self.part}] Procedure with the wrong name was created. Undoing the step update back to step {self.step}.")
                    return "Not the right procedure. Please follow the instruction and try again."
                else:
                    logger.debug(f"[{self.sid}][{self.stage},{self.part}] Action that was not supposed to be added was added. Undoing the step update back to step {self.step}.")
                    return "Not the right action. Please follow the instruction and try again."

        if not isinstance(self.immediate_goal, GetInputGoal) and (self.last_parsed_goal and not self.last_parsed_goal.error):
            if self.scenario_completed:
                logger.info(f"[{self.sid}][{self.stage},{self.part}] User completed scenario!")
                sio.emit("stageCompleted", room=str(self.sid))
            else:
                logger.debug(f"[{self.sid}][{self.stage},{self.part}] Nothing was wrong, so step can be updated.")
                sio.emit("stepUpdate", { "step": self.step }, room=str(self.sid))

        return response

class UserStudyAdvancedDialogManager(DialogManager):
    """
    Special dialog manager used for advanced scenarios in user study

    The main difference between this dialog manager and the default is the addition of a procedure check after user is done creating or editing a procedure.
    The DM checks if the completed procedure completes the scenario using the check function
    """
    def __init__(self, sid, part, inputs, check):
        super().__init__(sid)
        self.stage = "advanced"
        self.part = part
        self.inputs = inputs
        self.check = check
        logger.info(f"[{sid}][{self.stage},{self.part}] Inputs: {inputs}")

    def reset(self, context=None):
        if context is not None:
            logger.debug(f"[{self.sid}][{self.stage},{self.part}] Resetting conversation and scenario back to a specific context.")
            self.context = context
            self.qa = QuestionAnswer(context)
            self.nlu = SemanticNLU(context)
        else:
            logger.debug(f"[{self.sid}][{self.stage},{self.part}] Resetting the entire conversation and scenario.")
            self.context.reset()
            self.context.procedures = { }
            self.context.execution = None
        return "Conversation has been reset. What do you want to do first?"

    def handle_goal(self):
        if self.current_goal() is None:
            response = super().handle_goal()
        else:
            logger.debug(f"[{self.sid}][{self.stage},{self.part}] Handling goal {self.current_goal()}")
            goal = self.current_goal()
            goal.advance()
            if goal.error:
                logger.debug(f"[{self.sid}][{self.stage},{self.part}] Error with the goal {goal}.")
                response = goal.error
                self.context.goals.pop()
            elif goal.is_complete:
                if isinstance(goal, EditGoal) or isinstance(goal, GetProcedureActionsGoal):
                    logger.debug(f"[{self.sid}][{self.stage},{self.part}] User done with editing or creating goal so checking procedure.")
                    valid, res = self.check_procedure()
                    procedure_name = self.context.current.name
                    if valid:
                        logger.info(f"[{self.sid}][{self.stage},{self.part}] User completed scenario!")
                        sio.emit("stageCompleted", room=str(self.sid))
                        response = f"Looks like you achieved the goal! You can try running the procedure by saying, \"run {procedure_name}\"."
                    else:
                        # Procedure does not match behavior of reference or encountered an error during execution
                        logger.info(f"[{self.sid}][{self.stage},{self.part}] User did have a correct procedure.")
                        err_res = "Hmm, I checked your procedure, and it doesn't seem to meet the goal."
                        if res is not None:
                            if res == "StopIteration":
                                err_res = "Hmm, I checked your procedure, and it seems to have too many iterations."
                            elif res == "InfiniteLoop":
                                err_res = "Hmm, I checked your procedure, and it seems you may have an infinite loop."
                        response = f"{err_res} You can test the procedure by saying, \"run {procedure_name}\", or edit it by saying \"edit {procedure_name}\"."
                    goal.complete()
                    self.context.goals.pop()
                    return response
                response = goal.complete()
                self.context.goals.pop()
            else:
                response = goal.message
        return response

    def check_procedure(self):
        """Check procedure to see if it meets the objective and completes the advanced scenario"""
        procedure = self.context.current
        logger.debug(f"[{self.sid}][{self.stage},{self.part}] Checking procedure {procedure.name} to see if it passes.")
        execution = InternalExecution(self.context, [copy.copy(a) for a in procedure.actions], self.inputs)
        logger.debug(f"[{self.sid}][{self.stage},{self.part}] Internally executing procedure {procedure.name}.")
        response = execution.run()
        logger.debug(f"[{self.sid}][{self.stage},{self.part}] Using the advanced check function for unit testing procedure {procedure.name}.")
        valid = self.check(execution, response, self.inputs)
        if valid:
            logger.debug(f"[{self.sid}][{self.stage},{self.part}] Procedure {procedure.name} met the objectives and passed.")
        else:
            logger.debug(f"[{self.sid}][{self.stage},{self.part}] Procedure {procedure.name} did not meet the objectives.")
        return valid, response
