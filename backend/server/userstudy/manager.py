import copy

from dialog import *
from manage import sio
from app import logger
from goals import *
from models import *
from question import *
from nlu import *

class UserStudyDialogManager(DialogManager):
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
        logger.info(f"[{sid}][{stage},{part}] Created dialog manager for user studies.")

    @property
    def scenario_completed(self):
        return self.step >= len(self.scenario)

    def reset(self, to_backup=False):
        if to_backup:
            logger.info(f"[{self.sid}][{self.stage}] User did not follow instructions, so resetting to previous back up.")
            self.context = copy.deepcopy(self.backup_reference_context)
            self.qa = QuestionAnswer(self.context)
            self.nlu = SemanticNLU(self.context)
            self.last_parsed_goal = None
            response = "Conversation and objective has been reset to previous back up. What do you want to do first?"
        else:
            logger.info(f"[{self.sid}][{self.stage}] Resetting the entire conversation and scenario.")
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
        if self.step >= len(self.scenario):
            return None

        message = self.scenario[self.step][0]
        self.step += 1
        return message

    @property
    def immediate_goal(self):
        current = self.context.current_goal
        while current and current.todos:
            current = current.todos[-1]
        return current

    def handle_message(self, message):
        if self.step >= len(self.scenario):
            logger.info(f"[{self.sid}][{self.stage}] Finished the goal, so using default handling.")
            return super().handle_message(message)

        if not isinstance(self.immediate_goal, GetInputGoal):
            self.backup_context = copy.deepcopy(self.context)
            self.backup_reference_context = copy.deepcopy(self.reference.context)

        self.context.add_message(message)

        response = self.handle_reset(message)
        if response is not None:
            return response

        response = self.handle_help(message)
        if response is not None:
            return response

            return self.handle_execution(message)

        response = self.handle_question(message)
        if response is not None:
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
            return super().handle_parse(message)

        try:
            self.context.parsed = self.nlu.parse_message(message)
        except InvalidStateError as e:
            logger.info(f"[{self.sid}][{self.stage}] Action cannot be done in current state.")
            return "I cannot do this right now. Please follow instructions and try again!"

    def check_goal(self, message):
        goal = self.context.parsed
        if self.scenario[self.step][1] == type(goal):
            self.last_parsed_goal = goal
            logger.info(f"[{self.sid}][{self.stage}] User goal is the same type of the current objective goal.")
            return None
        elif self.immediate_goal and isinstance(self.immediate_goal, GetInputGoal):
            logger.info(f"[{self.sid}][{self.stage}] Current goal is for getting user input so ignoring.")
            return None
        elif goal:
            logger.info(f"[{self.sid}][{self.stage}] User goal does not match the current objective goal.")
            return "I think this is the wrong action. Please follow the instructions and try again!"
        elif self.scenario[self.step][1] is None and message == self.scenario[self.step][0]:
            logger.info(f"[{self.sid}][{self.stage}] User message matches the current objective message.")
            return None
        else:
            logger.info(f"[{self.sid}][{self.stage}] Goal could not be parsed and message was not recognized.")
            return "I didn't quite catch that. Please follow the instructions and try again!"

    def handle_reset(self, message):
        # Check for reset
        if message.lower() == "reset":
            return self.reset()

    def handle_goal(self):
        if self.step >= len(self.scenario):
            return super().handle_goal()

        if self.current_goal() is None:
            goal = self.context.parsed
            if goal is None or not isinstance(goal, BaseGoal):
                logger.info(f"[{self.sid}][{self.stage}] No current goal nor parsed goal so could not understand.")
                return "I didn't understand what you were saying. Please try again."
            elif goal.error:
                self.reset(to_backup=True)
                logger.info(f"[{self.sid}][{self.stage}] Current goal had an error.")
                return "I think your action is slightly wrong. Please try again!"
            elif goal.is_complete:
                response = goal.complete()
            else:
                response = goal.message
                self.context.add_goal(goal)
        else:
            goal = self.current_goal()
            goal.advance()

            if goal.error or self.last_parsed_goal.error:
                self.reset(to_backup=True)
                logger.info(f"[{self.sid}][{self.stage}] Current goal had an error.")
                return "I think your action is slightly wrong. Please follow the instructions and try again."
            elif goal.is_complete:
                response = goal.complete()
                self.context.goals.pop()
            else:
                response = goal.message

        if not isinstance(self.immediate_goal, GetInputGoal) and not self.last_parsed_goal.error:
            next_message = self.next_message
            logger.info(f"[{self.sid}][{self.stage}] Tentatively moving on to step {self.step} of the scenario.")
            if not next_message.startswith("run"):
                self.reference.handle_message(next_message)

        if isinstance(self.immediate_goal, GetActionsGoal):
            wrong_procedure = isinstance(self.last_parsed_goal, CreateProcedureGoal) and self.context.current.name != self.reference.context.current.name
            wrong_action = self.context.current.actions != self.reference.context.current.actions

            if wrong_procedure or wrong_action:
                self.reset(to_backup=True)
                self.reference.reset(self.backup_reference_context)
                self.step = max(self.step - 1, 0)
                if wrong_procedure:
                    logger.info(f"[{self.sid}][{self.stage}] Procedure with the wrong name was created. Undoing the step update back to step {self.step}.")
                    return "Not the right procedure. Please follow the instruction and try again."
                else:
                    logger.info(f"[{self.sid}][{self.stage}] Action that was not supposed to be added was added. Undoing the step update back to step {self.step}.")
                    return "Not the right action. Please follow the instruction and try again."

        if not isinstance(self.immediate_goal, GetInputGoal) and not self.last_parsed_goal.error:
            if self.scenario_completed:
                logger.info(f"[{self.sid}][{self.stage}] Completed the stage!")
                sio.emit("stageCompleted", room=str(self.sid))
            else:
                logger.info(f"[{self.sid}][{self.stage}] Nothing was wrong, so step can be updated.")
                sio.emit("stepUpdate", { "step": self.step }, room=str(self.sid))

        return response

class UserStudyAdvancedDialogManager(DialogManager):
    def __init__(self, sid, part, inputs, check):
        super().__init__(sid)
        self.stage = "advanced"
        self.part = part
        self.inputs = inputs
        self.check = check
        logger.info(f"[{sid}][{self.stage}] Created dialog manager for user studies.")

    def reset(self, context=None):
        if context is not None:
            logger.info(f"[{self.sid}][{self.stage}] Resetting conversation and scenario back to a specific context.")
            self.context = context
            self.qa = QuestionAnswer(context)
            self.nlu = SemanticNLU(context)
        else:
            logger.info(f"[{self.sid}][{self.stage}] Resetting the entire conversation and scenario.")
            self.context.reset()
            self.context.procedures = { }
            self.context.execution = None
        return "Conversation has been reset. What do you want to do first?"

    def handle_goal(self):
        if self.current_goal() is None:
            response = super().handle_goal()
        else:
            logger.info(f"[{self.sid}][{self.stage}] Handling goal {self.current_goal()}")
            goal = self.current_goal()
            goal.advance()
            if goal.error:
                logger.info(f"[{self.sid}][{self.stage}] Error with the goal {goal}.")
                response = goal.error
                self.context.goals.pop()
            elif goal.is_complete:
                if isinstance(goal, EditGoal) or isinstance(goal, GetProcedureActionsGoal):
                    logger.info(f"[{self.sid}][{self.stage}] User done with editing or creating goal so checking procedure.")
                    valid = self.check_procedure()
                    procedure_name = self.context.current.name
                    if valid:
                        sio.emit("stageCompleted", room=str(self.sid))
                        response = f"Looks like you achieved the goal! You can try running the procedure by saying, \"run {procedure_name}\"."
                    else:
                        response = f"Hmm, I checked your procedure, and it doesn't seem to meet the goal. You can test the procedure by saying, \"run {procedure_name}\", or edit it by saying \"edit {procedure_name}\"."
                    goal.complete()
                    self.context.goals.pop()
                    return response
                logger.info(f"[{self.sid}][{self.stage}] Goal {goal} was completed.")
                response = goal.complete()
                self.context.goals.pop()
            else:
                logger.info(f"[{self.sid}][{self.stage}] Goal {goal} not completed.")
                response = goal.message
        return response

    def check_procedure(self):
        procedure = self.context.current
        logger.info(f"[{self.sid}][{self.stage}] Checking procedure {procedure.name} to see if it passes.")
        execution = InternalExecution(self.context, [copy.copy(a) for a in procedure.actions], self.inputs)
        logger.info(f"[{self.sid}][{self.stage}] Internally executing procedure {procedure.name}.")
        response = execution.run()
        logger.info(f"[{self.sid}][{self.stage}] Using the advanced check function for unit testing procedure {procedure.name}.")
        valid = self.check(execution, response, self.inputs)
        if valid:
            logger.info(f"[{self.sid}][{self.stage}] Procedure {procedure.name} met the objectives and passed.")
        else:
            logger.info(f"[{self.sid}][{self.stage}] Procedure {procedure.name} did not meet the objectives.")
        return valid
