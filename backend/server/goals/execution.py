from goals import *
from models import *

class ExecuteGoal(HomeGoal):
    """
    Goal for executing a procedure

    Note that the execution actually happens once the goal is completed.
    """
    def __init__(self, context, procedure_name=None):
        super().__init__(context)
        self.context = context
        self.execution = None
        self.setattr("name", procedure_name)

    @property
    def message(self):
        if self.error:
            return self.error
        elif self.todos:
            return self.todos[-1].message

    @property
    def is_complete(self):
        return self.context.execution and super().is_complete

    def setattr(self, attr, value):
        if (attr == "name"):
            if value is None:
                self.todos.append(GetInputGoal(self.context, self, attr, "What do you want to run?"))
            elif value not in self.context.procedures:
                self.error = f"The procedure, {value}, hasn't been created, so we can't run it. You can create it by saying, \"create a procedure called {value}.\""
            else:
                self.procedure = self.context.procedures[value]

                # Create the execution with the actions from the desired procedure
                self.execution = Execution(self.context, [copy.copy(a) for a in self.procedure.actions])
                self.context.execution = self.execution
            return
        setattr(self, attr, value)

    def complete(self):
        """
        Complete the goal

        Completion of goal involves:
        1. Transition from "home" state to "executing" state
        2. Execute the procedure
        """
        self.context.transition(self)
        self.execution.run()
