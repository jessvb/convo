from goals import *
from models import *

class ConnectIntentGoal(HomeGoal):
    """
    Goal is to connect an intent to a procedure. If the procedure does not yet exist, creates one. 
    If the intent has associated entities, creates those variables (set to a default value of 0) 
    if they do not already exist for use in the procedure by adding a CreateVariable command to the 
    beginning of the list of actions in the procedure.
    """
    def __init__(self, context, intent_name=None, procedure_name=None):
        super().__init__(context)
        self.context = context
        self.execution = None
        self.new_variables = [] # list of new variables/entities created in the procedure
        self.created_new_procedure = False
        self.setattr("intent_name", intent_name)
        self.setattr("procedure_name", procedure_name)

    @property
    def message(self):
        if self.error:
            return self.error

        if self._message:
            return self._message

        return_message = f"I connected the intent {self.intent_name} to the procedure {self.procedure_name}."

        if self.created_new_procedure:
            return_message += f" The procedure, {self.procedure_name}, did not exist previously, so I created a new procedure."

        if self.context.intents[self.intent_name]:
            for entity in self.context.intents[self.intent_name][::-1]:
                if entity in self.new_variables:
                    new_variable_index = self.entity_already_exists(entity, self.procedure) + 1
                    return_message += f" I created a variable for the entity {entity} that is set to a value of 0 at step {new_variable_index}. This default value will be overriden if I detect a different value for this entity when I recognize this intent."

        return_message += f" What do you want to do now?"

        return return_message if self.is_complete else self.todos[-1].message

    def setattr(self, attr, value):
        if (attr == "intent_name"):
            if not value:
                self.todos.append(GetInputGoal(self.context, self, attr, "Which intent do you want to connect?"))
            elif value not in self.context.intents:
                self.error = f"An intent with the name, {value}, has not been created."
            else:
                self.intent_name = value
            return
        elif (attr == "procedure_name"):
            if not value:
                self.todos.append(GetInputGoal(self.context, self, attr, "Which procedure do you want to connect?"))
            else:
                if value not in self.context.procedures:
                    procedure_to_create = Procedure(value)
                    self.context.procedures[value] = procedure_to_create
                    add_or_update_procedure(self.context.sid, procedure_to_create)
                    self.created_new_procedure = True                  
                self.procedure_name = value
        setattr(self, attr, value)

    def complete(self):
        self.procedure = self.context.procedures[self.procedure_name]
        self.context.intent_to_procedure[self.intent_name] = self.procedure
        self.context.current = self.procedure
        # Transition from "home" state to "editing" state
        self.context.transition(self)

        for entity in self.context.intents[self.intent_name]:
            entity_index = self.entity_already_exists(entity, self.procedure)
            if entity_index == -1:
                create_variable = CreateVariableActionGoal(self.context, entity, 0, True)
                create_variable.actions = self.procedure.actions
                create_variable.variables = self.procedure.variables
                create_variable.complete()
                self.new_variables.append(entity)
        self.context.transition("complete")
        return super().complete()

    def entity_already_exists(self, entity, procedure):
        for index in range(len(procedure.actions)):
            action = procedure.actions[index]
            if type(action) is CreateVariableAction:
                if action.variable == entity:
                    return index
        return -1

class RunIntentGoal(HomeGoal):
    """
    Goal is to run the procedure connected to an intent when the intent is recognized. The goal is only complete when all slots/entities 
    have been filled. Entities are recognized in the procedure by deleting the original action where the entity was first created and set
    to a default value of 0 and then adding in a new action in the same place where the entity is created as a variable again and then 
    set to the value given by the user.
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
                self.procedure = self.context.intent_to_procedure[value]
                for entity in required_entities:
                    if entity not in self.context.entities:
                        self.error = f"The entity, {entity}, has not yet been initialized."
                    elif self.context.entities[entity] == None:
                        self.todos.append(GetEntityInputGoal(self.context, value, entity, f"What is the {entity}?"))
                    else:
                        # Replace the original CreateVariableAction with a new CreateVariableAction at the same index with the entity set to the 
                        # correct value given by the user.
                        for i in range(len(self.procedure.actions)):
                            action = self.procedure.actions[i]
                            if type(action) is CreateVariableAction:
                                if action.variable == entity:
                                    self.procedure.actions[i] = CreateVariableAction(entity, self.context.entities[entity])  
                
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
