import copy
from dialog import DialogManager
from goals import *
from models import *

class UserStudyDialogManager(DialogManager):
    def __init__(self, sid, scenario):
        super().__init__(sid)
        self.scenario = scenario
        self.step = 0
        self.reference = DialogManager(sid)
        self.reference.handle_message(self.next_message)

    @property
    def next_message(self):
        if self.step >= len(self.scenario):
            return None

        message = self.scenario[self.step]
        self.step += 1
        return message

    def handle_message(self, message):
        context = copy.deepcopy(self.context)
        response = super().handle_message(message)

        reference_current_goal = self.reference.current_immediate_goal()
        current_goal = self.current_immediate_goal()
        check_state = self.reference.context.state == self.context.state

        if isinstance(current_goal, GetInputGoal):
            parent_goal = self.current_goal()
            while parent_goal.todos[-1] is not current_goal:
                parent_goal = parent_goal.todos[-1]
            if isinstance(parent_goal, ActionGoal):
                if isinstance(reference_current_goal, GetActionsGoal):
                    check_goal = str(parent_goal).startswith(str(reference_current_goal.actions[-1]))
                    if not check_goal:
                        logging.info("Action goal does not match current reference action.")
                        self.reset(copy.deepcopy(context))
                        return "Please follow the instructions on the sidebar."
                    return response
                else:
                    logging.info("Reference currently not getting actions, but action goal is present in context.")
                    self.reset(copy.deepcopy(context))
                    return "Please follow the instructions on the sidebar."
            return response
        elif isinstance(current_goal, GetActionsGoal):
            reference_procedure = self.reference.context.current
            procedure = self.context.current
            check_procedure = procedure and reference_procedure.name == procedure.name
            check_actions = current_goal.actions == reference_current_goal.actions

            if check_procedure and check_state and check_actions:
                next_message = self.next_message
                if next_message:
                    logging.info("Action was correctly added.")
                    self.reference.handle_message(next_message)
                    return response
                logging.info("All steps of the scenario has been accomplished.")
                return "You're done!"
            else:
                logging.info("Not the correct state or correct set of actions.")
                self.reset(copy.deepcopy(context))
                return "Please follow the instructions on the sidebar."
        elif check_state:
            return response
        else:
            logging.info("Not the correct state.")
            self.reset(copy.deepcopy(context))
            return "Please follow the instructions on the sidebar."
