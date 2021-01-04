from goals import *
from models import *

class ConnectIntentGoal(HomeGoal):
    """
    Goal is to connect an intent to a procedure. 

    """
    def __init__(self, context, intent_name=None, procedure_name=None):
        super().__init__(context)
        self.context = context
        self.execution = None
        self.setattr("intent_name", intent_name)
        self.setattr("procedure_name", procedure_name)

    @property
    def message(self):
        if self.error:
            return self.error

        if self._message:
            return self._message

        return f"I connected the intent {self.intent_name} to the procedure {self.procedure_name}. What do you want to do now?" if self.is_complete else self.todos[-1].message

    def setattr(self, attr, value):
        if (attr == "intent_name"):
            if not value:
                self.todos.append(GetInputGoal(self.context, self, attr, "Which intent do you want to connect?"))
            elif value not in self.context.intents:
                logger.debug("context intents")
                logger.debug(self.context.intents)
                self.error = f"An intent with the name, {value}, has not been created."
            else:
                self.intent_name = value
            return
        elif (attr == "procedure_name"):
            if not value:
                self.todos.append(GetInputGoal(self.context, self, attr, "Which procedure do you want to connect?"))
            elif value not in self.context.procedures:
                logger.debug(value)
                logger.debug(self.context.procedures)
                self.error = f"The procedure with the name, {value}, has not been created."
            else:
                self.procedure_name = value
        setattr(self, attr, value)

    def complete(self):
        procedure = self.context.procedures[self.procedure_name]
        self.context.intent_to_procedure[self.intent_name] = procedure
        return super().complete()

class RunIntentGoal(HomeGoal):
    """
    Goal is to run the procedure connected to an intent when the intent is recognized. The goal is only complete when all slots/entities have been filled.
    """
    def __init__(self, context, intent_name=None):
        super().__init__(context)
        self.context = context
        self.setattr("intent_name", intent_name)

    @property
    def message(self):
        if self.error:
            return self.error
        elif self.todos:
            return self.todos[-1].message

    def setattr(self, attr, value):
        if (attr == "intent_name"):
            if value is None:
                self.todos.append(GetInputGoal(self.context, self, attr, "What intent do you want to recognize?"))
            elif value in self.context.intents and value not in self.context.intent_to_procedure:
                self.error = f"The intent, {value}, has been created but hasn't been connected to a procedure, so we can't run it. You can connect it by saying, \"connect the intent {value} to the procedure [procedure name].\""
            else:
                required_entities = self.context.intents[value]
                for entity in required_entities:
                    if entity not in self.context.entities:
                        self.error = f"The entity, {entity}, has not yet been initialized."
                    elif self.context.entities[entity] == None:
                        self.todos.append(GetEntityInputGoal(self.context, entity, f"What is the {entity}?"))
                self.procedure = self.context.intent_to_procedure[value]
            return
        setattr(self, attr, value)

    def complete(self):
        """
        Complete the goal

        Completion of goal involves:
        1. Transition from "home" state to "executing" state
        2. Execute the procedure
        """
        execute = ExecuteGoal(self.context, self.procedure.name)
        return execute.complete()
