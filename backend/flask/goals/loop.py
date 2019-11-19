from goals import *
from models import *

class CreateLoopGoal(object):
    def __init__(self, context, condition=None, action=None):
        self.context = context
        self.todos = []
        self.loop_actions = []
        self.error = None
        self.condition = condition
        self.procedure = None

        if action is not None:
            self.loop_actions[0].append(action)

        self.todos.append(GetLoopActionsGoal(self.context, self))
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
            print("Completing CreateLoopGoal")
            self.actions.append(LoopAction(self.condition, self.loop_actions))
            self.goal.todos.pop()

        return self.message

    def pursue(self):
        print("Pursuing CreateLoopGoal")
        self.todos[-1].try_complete()

    def __str__(self):
        return "create_loop" + (f":{str(self.todos[-1])}" if self.todos else "")

class GetLoopActionsGoal(object):
    def __init__(self, context, goal):
        self.todos = []
        self.context = context
        self.goal = goal
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
            if len(self.goal.loop_actions) > 0:
                return "Added action! What's next?"
            else:
                return f"What do you want to do first in the loop?"
        else:
            return self.todos[-1].message

    def try_complete(self):
        if not self.is_complete:
            self.pursue()

        if self.is_complete:
            print("Completing GetLoopActionsGoal")
            self.goal.todos.pop()

        return self.error if self.error else self.message

    def pursue(self):
        print("Pursuing GetLoopActionsGoal")
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
            setattr(goal, "actions", self.goal.loop_actions)
            setattr(goal, "goal", self)
            self.todos.append(goal)

    def __str__(self):
        return "get_actions" + (f":{str(self.todos[-1])}" if self.todos else "")
