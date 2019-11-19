from goals import *
from models import *

class CreateConditionalGoal(object):
    def __init__(self, context, condition=None, action=None):
        self.context = context
        self.todos = []
        self.conditional_actions = [[], []]
        self.error = None
        self.condition = condition
        self.procedure = None

        if action is not None:
            self.conditional_actions[0].append(action)

        self.todos.append(GetConditionalActionsGoal(self.context, self, 0))
        self.todos.append(GetConditionalActionsGoal(self.context, self, 1))

        if condition is None:
            self.todos.append(GetConditionGoal(self.context, self))

    @property
    def is_complete(self):
        return len(self.todos) == 0

    @property
    def message(self):
        if self.error:
            return self.error

        if self.is_complete:
            return "Goal completed!"

        return self.todos[-1].message

    def try_complete(self):
        if not self.is_complete:
            self.pursue()

        if self.is_complete:
            print("Completing CreateConditionalGoal")
            self.actions.append(ConditionalAction(self.condition, self.conditional_actions))
            self.goal.todos.pop()

        return self.message

    def pursue(self):
        print("Pursuing CreateConditionalGoal")
        self.todos[-1].try_complete()

    def __str__(self):
        return "create_conditional" + (f":{str(self.todos[-1])}" if self.todos else "")

class GetConditionGoal(object):
    def __init__(self, context, goal):
        self.context = context
        self.goal = goal
        self.procedure = self.goal.procedure
        self.condition = None
        self.error = None

    @property
    def is_complete(self):
        return self.condition is not None

    @property
    def message(self):
        if self.error is not None:
            return self.error

        if self.is_complete:
            return "Goal completed!"

        return "What's the condition?"

    def try_complete(self):
        self.error = None
        if not self.is_complete:
            self.pursue()

        if self.is_complete:
            print("Completing GetConditionGoal")
            self.goal.condition = self.condition
            self.goal.todos.pop()

        return self.message

    def pursue(self):
        print("Pursuing GetConditionGoal")
        condition = self.context.parsed
        if condition is not None and isinstance(condition, Condition):
            self.condition = condition
        else:
            self.error = "Not a condition. Try again."

    def __str__(self):
        return "get_condition"

class GetConditionalActionsGoal(object):
    def __init__(self, context, goal, index):
        self.todos = []
        self.context = context
        self.goal = goal
        self.condition_idx = index
        self.error = None
        self.no_more_actions = False
        self.procedure = None

    @property
    def is_complete(self):
        return self.no_more_actions and len(self.todos) == 0

    @property
    def message(self):
        if self.error is not None:
            return self.error

        if self.is_complete:
            return "Goal completed!"

        if len(self.todos) == 0:
            if len(self.goal.conditional_actions[self.condition_idx]) > 0:
                return "Added action! What's next?"
            else:
                return f"What do you want to do first if the condition is {'not ' if self.condition_idx == 0 else ''}true?"
        else:
            return self.todos[-1].message

    def try_complete(self):
        if not self.is_complete:
            self.pursue()

        if self.is_complete:
            print("Completing GetConditionalActionsGoal")
            self.goal.todos.pop()

        return self.error if self.error else self.message

    def pursue(self):
        print("Pursuing GetConditionalActionsGoal")
        message = self.context.current_message
        self.error = None
        if message in ["done", "nothing"] and len(self.todos) == 0:
            self.no_more_actions = True
        elif len(self.todos) > 0:
            self.todos[-1].try_complete()
        elif self.context.parsed is None:
            self.error = "Couldn't understand the action. Try again."
        else:
            goal = self.context.parsed
            setattr(goal, "procedure", self.goal.procedure)
            setattr(goal, "actions", self.goal.conditional_actions[self.condition_idx])
            setattr(goal, "goal", self)
            self.todos.append(goal)

    def __str__(self):
        return "get_actions" + (f":{str(self.todos[-1])}" if self.todos else "")
