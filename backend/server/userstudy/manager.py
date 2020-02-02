import logging
import copy

from dialog import DialogManager
from manage import sio
from goals import *
from models import *
from question import *
from nlu import *

logger = logging.getLogger("gunicorn.error")

class UserStudyDialogManager(DialogManager):
    def __init__(self, sid, stage, scenario):
        super().__init__(sid)
        self.scenario = scenario
        self.stage = stage
        self.step = 0
        self.reference = DialogManager(sid)
        self.last_parsed_goal = None
        self.backup_context = copy.deepcopy(self.context)
        logger.info(f"UserStudyDialogManager created for stage {stage}.")

    @property
    def scenario_completed(self):
        return self.step >= len(self.scenario)

    def reset(self, context=None):
        if context:
            self.context = context
            self.qa = QuestionAnswer(context)
            self.nlu = SemanticNLU(context)
        else:
            self.context.reset()
            self.reference = DialogManager(sid)
            self.step = 0
        self.backup_context = copy.deepcopy(self.context)
        return "Conversation has been reset. What do you want to do first?"

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

    def handle_parse(self, message):
        try:
            self.context.parsed = self.nlu.parse_message(message)
        except InvalidStateError as e:
            logger.info(f"Action cannot be done in current state.")
            return "I cannot do this right now. Please follow instructions and try again!"

    def check_goal(self, message):
        goal = self.context.parsed
        if self.scenario[self.step][1] == type(goal):
            self.last_parsed_goal = goal
            logger.info(f"User goal is the same type of the current objective goal.")
            return None
        elif self.immediate_goal and isinstance(self.immediate_goal, GetInputGoal):
            logger.info(f"Current goal is for getting user input so ignoring.")
            return None
        elif goal:
            logger.info(f"User goal does not match the current objective goal.")
            return "I think this is the wrong action. Please follow the instructions and try again!"
        elif self.scenario[self.step][1] is None and message == self.scenario[self.step][0]:
            logger.info(f"User message matches the current objective message.")
            return None
        else:
            logger.info(f"Goal could not be parsed and message was not recognized.")
            return "I didn't quite catch that. Please follow the instructions and try again!"

    def handle_goal(self):
        backup_reference_context = copy.deepcopy(self.reference.context)

        if self.current_goal() is None:
            goal = self.context.parsed
            if goal is None or not isinstance(goal, BaseGoal):
                return "I didn't understand what you were saying. Please try again."
            elif goal.error:
                self.reset(copy.deepcopy(self.backup_context))
                logger.info(f"Current goal had an error.")
                return "I think your action is slightly wrong. Please follow the instructions and try again!"
            elif goal.is_complete:
                response = goal.complete()
            else:
                response = goal.message
                self.context.add_goal(goal)
        else:
            goal = self.current_goal()
            goal.advance()

            if goal.error or self.last_parsed_goal.error:
                self.reset(copy.deepcopy(self.backup_context))
                logger.info(f"Current goal had an error.")
                return "I think your action is slightly wrong. Please follow the instructions and try again."
            elif goal.is_complete:
                response = goal.complete()
                self.context.goals.pop()
            else:
                response = goal.message

        if not isinstance(self.immediate_goal, GetInputGoal) and not self.last_parsed_goal.error:
            next_message = self.next_message
            logger.info(f"Tentatively moving on to step {self.step} of the scenario.")
            if not next_message.startswith("run"):
                self.reference.handle_message(next_message)

        if isinstance(self.immediate_goal, GetActionsGoal):
            wrong_procedure = isinstance(self.last_parsed_goal, CreateProcedureGoal) and self.context.current.name != self.reference.context.current.name
            wrong_action = self.immediate_goal.actions != self.reference.immediate_goal.actions

            if wrong_procedure or wrong_action:
                self.reset(copy.deepcopy(self.backup_context))
                self.reference.reset(backup_reference_context)
                self.step = max(self.step - 1, 0)
                if wrong_procedure:
                    logger.info(f"Procedure with the wrong name was created. Undoing the step update back to step {self.step}.")
                    return "Not the right procedure. Please follow the instruction and try again."
                else:
                    logger.info(f"Action that was not supposed to be added was added. Undoing the step update back to step {self.step}.")
                    return "Not the right action. Please follow the instruction and try again."

        if not isinstance(self.immediate_goal, GetInputGoal) and not self.last_parsed_goal.error:
            if self.scenario_completed:
                logger.info(f"Stage completed!")
                sio.emit("stageCompleted", room=str(self.sid))
            else:
                logger.info(f"Nothing was wrong, so step can be updated.")
                sio.emit("stepUpdate", { "step": self.step }, room=str(self.sid))

        return response

    def handle_message(self, message):
        if self.step >= len(self.scenario):
            return super().handle_message(message)

        self.context.add_message(message)

        response = self.handle_help(message)
        if response:
            return response

        if self.context.state == "executing":
            return self.handle_execution(message)

        response = self.handle_question(message)
        if response:
            return response

        response = self.handle_parse(message)
        if response:
            return response

        response = self.check_goal(message)
        if response:
            return response

        if not isinstance(self.immediate_goal, GetInputGoal):
            self.backup_context = copy.deepcopy(self.context)

        response = self.handle_goal()

        return response

class UserStudyAdvancedDialogManager(DialogManager):
    def __init__(self, sid, inputs, check):
        super().__init__(sid)
        self.stage = "advanced"
        self.step = 0
        self.inputs = inputs
        logger.info(f"UserStudyDialogManager created for stage {self.stage}.")

    def handle_goal(self):
        if self.current_goal() is None:
            super().handle_goal()
        else:
            goal = self.current_goal()
            goal.advance()
            if goal.error:
                response = goal.error
                self.context.goals.pop()
            elif goal.is_complete:
                if isinstance(goal, EditGoal) or isinstance(goal, GetProcedureActionsGoal):
                    response = self.check_procedure()
                    if response:
                        return "Try again."
                response = goal.complete()
                self.context.goals.pop()
            else:
                response = goal.message

        return response

    def check_procedure(self):
        procedure = self.context.current
        execution = InternalExecution(self.context, procedure.actions, self.inputs)
        response = execution.run()
        valid = self.check(execution, response)
        if not valid:
            return response
