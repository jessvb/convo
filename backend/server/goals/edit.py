from app import logger
from goals import *
from models import *
from word2number import w2n

class EditGoal(HomeGoal):
    """Goal for editing procedure"""
    def __init__(self, context, name=None):
        super().__init__(context)

        # Transition from "home" state to "editing" state
        self.context.transition(self)

        # List of editing contexts - representing different scopes
        # For example, there are editing contexts for editing in the top-level procedure and for editing actions in a conditional
        self.edit = []

        # Name of procedure
        self.setattr("name", name)

    @property
    def message(self):
        if self.error:
            return self.error

        if self._message:
            return self._message

        if self.is_complete:
            return f"Done with editing procedure {self.name}."

        if len(self.todos) == 0:
            return self.edit[-1].message
        else:
            return self.todos[-1].message

    @property
    def is_complete(self):
        return len(self.context.edit) == 0 and super().is_complete

    def complete(self):
        message = super().complete()
        self.context.edit = None
        self.context.transition("complete")
        return message

    def cancel(self):
        self.context.edit = None
        self.context.transition("complete")

    def advance(self):
        logger.debug(f"Advancing {self.__class__.__name__}...")
        self._message = None
        if self.todos:
            todo = self.todos.pop()
            if todo.error:
                self._message = todo.error
                return

            todo.advance()
            if todo.is_complete:
                if isinstance(todo, GetInputGoal):
                    todo.complete()
                    return self.edit[-1].message
                else:
                    self._message = todo.complete()
            else:
                self.todos.append(todo)
            return

        if self.context.current_message == "done":
            self.edit.pop()
        elif self.context.current_message in ["step into"]:
            # Step into editing actions in another action like a loop action
            if not self.edit[-1].current:
                self._message = f"There are no steps in the {self.scope} so I cannot do this."
                return
            action = self.edit[-1].current
            if isinstance(action, LoopAction):
                # Currently, only support stepping into a loop action
                self.edit.append(EditContext(self.context, action.actions, in_loop=True))
            else:
                self._message = "You cannot step into this action."
        elif self.context.current_message in ["next step", "continue", "next"]:
            if not self.edit[-1].current:
                self._message = f"There are no steps in the {self.scope} so I cannot do this."
                return
            if self.edit[-1].at_last_step:
                self._message = f"I am already on the last step, {self.edit[-1].actions[self.edit[-1].step].to_nl()}. There is no where for me to go."
                return
            self.edit[-1].next_step()
        elif self.context.current_message in ["previous step", "previous", "go back"]:
            if not self.edit[-1].current:
                self._message = f"There are no steps in the {self.scope} so I cannot do this."
                return
            if self.edit[-1].at_first_step:
                self._message = f"I am already on the first step, {self.edit[-1].actions[self.edit[-1].step].to_nl()}. There is no where for me to go."
                return
            self.edit[-1].prev_step()
        elif not isinstance(self.context.parsed, BaseGoal):
            self._message = "I didn't quite catch that. What do you want me to do?"
        elif self.context.parsed.error is not None:
            self._message = self.context.parsed.error
        elif self.context.parsed._message is not None:
            self._message = self.context.parsed._message
        else:
            if isinstance(self.context.parsed, ActionGoal):
                action = AddStepGoal(self.context)
                action.advance()
            else:
                action = self.context.parsed

            if action.is_complete:
                self._message = action.complete()
            else:
                self.todos.append(action)

    def setattr(self, attr, value):
        if (attr == "name"):
            if value is None:
                self.todos.append(GetInputGoal(self.context, self, attr, "What do you want to edit?"))
            elif value not in self.context.procedures:
                self.error = f"The procedure, {value}, hasn't been created, so there's nothing to edit. You can create it by saying, \"create a procedure called {value}.\""
                self.context.transition("complete")
            else:
                self.name = value
                self.procedure = self.context.procedures[value]
                self.edit = [EditContext(self.context, self.procedure.actions)]
                self.context.edit = self.edit
                self.context.current = self.procedure
            return
        setattr(self, attr, value)

class EditContext(object):
    """
    Context for editing

    Currently, EditContext only supports stepping into loops so the two types of EditContexts are
    within loops and within the overall procedure
    """
    def __init__(self, context, actions, in_loop=False):
        # Dialog context"""
        self.context = context

        # Action list in which all editing will be done
        self.actions = actions

        # Step in the action list
        self.step = 0 if self.actions else -1
        self.done = False

        if in_loop:
            self.scope = f"loop"
        else:
            self.scope = f"procedure"
        logger.debug(f"Actions: {[str(a) for a in actions]}")

    @property
    def current(self):
        return self.actions[self.step] if self.step >= 0 else None

    @property
    def at_last_step(self):
        return self.step == len(self.actions) - 1

    @property
    def at_first_step(self):
        return self.step == 0

    @property
    def message(self):
        if self.current:
            if self.at_first_step:
                step_message = f"I am on the first {'and only ' if self.at_last_step else ''}step"
            else:
                step_message = f"I am on step {self.step + 1}"
                if self.at_last_step:
                    step_message += " which is the last step"
            return f"{step_message} of the {self.scope}, where I am {self.current.to_nl()}. What do you want to do? You can say 'done' if you are finished editing."
        else:
            return f"There are currently no actions in the {self.scope}. What do you want to do?"

    def next_step(self):
        """Go to next step"""
        if len(self.actions) != 0 and not self.at_last_step:
            self.step += 1

    def prev_step(self):
        """Go to previous step"""
        if len(self.actions) != 0 and not self.at_first_step:
            self.step -= 1

    def to_step(self, step):
        """Go to a specified step"""
        assert isinstance(step, int) and step >= -1 and step <= len(self.actions) - 1
        self.step = len(self.actions) - 1 if step == -1 else step

    def remove_current_step(self):
        """Remove the current step"""
        new = self.step
        if self.step == len(self.actions) - 1:
            new = self.step - 1
        action = self.actions[self.step]
        if isinstance(action, CreateVariableAction):
            self.context.current.variables.remove(action.name)
        del self.actions[self.step]
        self.step = new
        return action

    def add_step(self, action, step=None):
        """Add a new step after the current step"""
        if step is not None:
            self.actions[step:step] = action
        else:
            self.step += 1
            self.actions[self.step:self.step] = action

class GoToStepGoal(StepGoal):
    """Go to step during editing"""
    def __init__(self, context, step=None):
        super().__init__(context)
        if not self.current_edit.current:
            self.error = f"There are no steps in the {self.scope} so I cannot do this."
            return
        self.setattr("step", step)

    def complete(self):
        if self.step == "next":
            if self.current_edit.at_last_step:
                return f"I am already on the last step of the {self.scope}, {self.current_edit.actions[self.current_edit.step].to_nl()}. There is no where for me to go."
            self.current_edit.next_step()
        elif self.step == "previous":
            if self.current_edit.at_first_step:
                return f"I am already on the first step of the {self.scope}, {self.current_edit.actions[self.current_edit.step].to_nl()}. There is no where for me to go."
            self.current_edit.prev_step()
        elif self.step == "first":
            self.current_edit.to_step(0)
        elif self.step == "last":
            self.current_edit.to_step(-1)
        else:
            self.current_edit.to_step(self.step)

        step_message = f"the {self.step} step" if isinstance(self.step, str) else f"step {self.step + 1}"
        return f"Going to {step_message} of the {self.scope}, where I am {self.current_edit.actions[self.current_edit.step].to_nl()}."

    def setattr(self, attr, value):
        if (attr == "step"):
            if value is None:
                self.todos.append(GetInputGoal(self.context, self, attr, f"Which step in the {self.scope} do you want to go to?"))
            else:
                step = value.replace("step", "").replace("the", "").strip()
                try:
                    step = w2n.word_to_num(step) - 1
                    if not isinstance(step, int):
                        self.error = f"Step {step + 1} is not a step."
                    elif step >= len(self.current_edit.actions) - 1:
                        self.error = f"I cannot go to step {step + 1}. There are only {len(self.current_edit.actions)} steps."
                    else:
                        self.step = step
                except ValueError as e:
                    if step in ["last", "first", "next", "previous"]:
                        self.step = step
                    else:
                        self.error = f"Step {step} is not a step."
            return
        setattr(self, attr, value)

class DeleteStepGoal(StepGoal):
    """Delete step during editing"""
    def __init__(self, context):
        super().__init__(context)
        if len(self.current_edit.actions) == 0:
            self.error = f"There are no actions or steps in the {self.scope} that you can delete."

    def complete(self):
        message = f"Deleted step {self.current_edit.step + 1} of the {self.scope}, where I was {self.current_edit.actions[self.current_edit.step].to_nl()}. "
        self.current_edit.remove_current_step()
        if self.current_edit.current:
            message += f"Now step {self.current_edit.step + 1} is where I am {self.current_edit.actions[self.current_edit.step].to_nl()}."
        else:
            message += f"Now there are no more actions in the {self.scope}."
        return message

class AddStepGoal(StepGoal):
    """Add step during editing"""
    def __init__(self, context):
        super().__init__(context)
        self.context.transition(self)
        self.actions = []

    @property
    def is_complete(self):
        return len(self.actions) == 1 and super().is_complete

    @property
    def message(self):
        if self.error:
            return self.error

        if self._message:
            return self._message

        if self.todos:
            return self.todos[-1].message
        else:
            return f"What action do you want to add to the {self.scope}?"

    def complete(self):
        if not self.current_edit.current:
            message = f"I added the action, which is the first action."
        else:
            message = f"I added the action after step {self.current_edit.step + 1}."
        self.current_edit.add_step(self.actions)
        self.context.transition("complete")
        return f"{message} I am at step {self.current_edit.step + 1} in the {self.scope} where I am {self.actions[0].to_nl()}."

    def cancel(self):
        self.context.transition("complete")

    def advance(self):
        if self.todos:
            super().advance()
            return

        logger.debug(f"Advancing {self.__class__.__name__}...")
        self._message = None
        if not isinstance(self.context.parsed, BaseGoal):
            self._message = f"I didn't quite catch that. What action did you want me to add to the {self.scope}?"
        elif self.context.parsed.error is not None:
            self._message = self.context.parsed.error
        elif self.context.parsed._message is not None:
            self._message = self.context.parsed._message
        else:
            action = self.context.parsed
            setattr(action, "actions", self.actions)
            if action.is_complete:
                action.complete()
            else:
                self.todos.append(action)

class ChangeStepGoal(StepGoal):
    """Change step during editing"""
    def __init__(self, context):
        super().__init__(context)
        if len(self.current_edit.actions) == 0:
            self.error = f"There are no actions or steps in the {self.scope} that you can delete."
        self.context.transition(self)
        self.step = self.current_edit.step
        self.original_action = self.current_edit.remove_current_step()
        self.actions = []

    @property
    def is_complete(self):
        return len(self.actions) == 1 and super().is_complete

    @property
    def message(self):
        if self.error:
            return self.error

        res = "What action do you want to replace the current step with?"
        if self._message:
            return f"{self._message} {res}"

        if self.todos:
            return self.todos[-1].message
        else:
            return res

    def complete(self):
        self.current_edit.step = self.step
        self.current_edit.actions[self.step:self.step] = self.actions
        self.context.transition("complete")
        return f"Changed step {self.current_edit.step + 1} in the {self.scope}, where I am now {self.actions[0].to_nl()}."

    def cancel(self):
        self.current_edit.step = self.step
        self.current_edit.actions[self.step:self.step] = [self.original_action]
        self.context.transition("complete")

    def advance(self):
        if self.todos:
            super().advance()
            return

        logger.debug(f"Advancing {self.__class__.__name__}...")
        self._message = None
        if not isinstance(self.context.parsed, BaseGoal):
            self._message = "I didn't quite catch that."
        elif self.context.parsed.error is not None:
            self._message = self.context.parsed.error
        elif self.context.parsed._message is not None:
            self._message = self.context.parsed._message
        else:
            action = self.context.parsed
            setattr(action, "actions", self.actions)
            if action.is_complete:
                action.complete()
            else:
                self.todos.append(action)
