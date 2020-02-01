import logging
import copy

from dialog import DialogManager
from goals import *
from models import *
from question import *
from nlu import *

class UserStudyDialogManager(DialogManager):
    def __init__(self, sid, scenario):
        super().__init__(sid)
        self.scenario = scenario
        self.step = 0
        self.reference = DialogManager(sid)
        self.last_parsed_goal = None
        self.backup_context = copy.deepcopy(self.context)

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
            return "I cannot do this right now. Please follow instructions and try again!"

    def check_goal(self, message):
        goal = self.context.parsed
        if self.scenario[self.step][1] == type(goal):
            self.last_parsed_goal = goal
            return None
        elif self.immediate_goal and isinstance(self.immediate_goal, GetInputGoal):
            return None
        elif goal:
            return "I think this is the wrong action. Please follow the instructions and try again!"
        elif self.scenario[self.step][1] is None and message == self.scenario[self.step][0]:
            return None
        else:
            return "I didn't quite catch that. Please follow the instructions and try again!"

    def handle_goal(self):
        if self.current_goal() is None:
            self.backup_context = copy.deepcopy(self.context)
            return super().handle_goal()
        else:
            if not isinstance(self.immediate_goal, GetInputGoal):
                self.backup_context = copy.deepcopy(self.context)

            goal = self.current_goal()
            goal.advance()

            if goal.error or self.last_parsed_goal.error:
                self.reset(copy.deepcopy(self.backup_context))
                return "I think your action is slightly wrong. Please follow the instructions and try again!"
            elif goal.is_complete:
                response = goal.complete()
                self.context.goals.pop()
            else:
                response = goal.message

            backup_reference_context = copy.deepcopy(self.reference.context)
            if not isinstance(self.immediate_goal, GetInputGoal) and not self.last_parsed_goal.error:
                next_message = self.next_message
                self.reference.handle_message(next_message)

            if isinstance(self.immediate_goal, GetActionsGoal):
                if self.immediate_goal.actions != self.reference.immediate_goal.actions:
                    self.reset(copy.deepcopy(self.backup_context))
                    self.reference.reset(backup_reference_context)
                    self.step = max(self.step - 1, 0)
                    return "Not the right action."

            return response

    def handle_message(self, message):
        if self.step >= len(self.scenario):
            return super().handle_message(message)

        print("===========================")
        logging.info(f"Message: {message}")
        logging.info(f"State: {self.context.state}")
        logging.info(f"Goal: {self.context.current_goal}")
        logging.info(f"Step: {self.step}")

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

        response = self.handle_goal()

        print("---------------------------------")
        logging.info(f"Response: {response}")
        logging.info(f"State: {self.context.state}")
        logging.info(f"Goal: {self.context.current_goal}")
        logging.info(f"Step: {self.step}")

        return response
