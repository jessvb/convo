from app import logger
from goals import *
from models import *
from word2number import w2n

class EditGoal(HomeGoal):
    def __init__(self, context, name=None):
        super().__init__(context)
        self.context.transition(self)
        self.edit = None
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
            return self.edit.message
        else:
            return self.todos[-1].message

    @property
    def is_complete(self):
        return self.context.edit and self.context.edit.done and super().is_complete

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
                    return self.edit.message
                else:
                    self._message = todo.complete()
            else:
                self.todos.append(todo)
            return

        if self.context.current_message == "done":
            self.edit.done = True
        elif self.context.current_message in ["next step", "continue", "next"]:
            if not self.edit.current:
                self._message = "There are no steps in the procedure for me to go."
                return
            if self.edit.at_last_step:
                self._message = f"I am already on the last step, {self.edit.actions[self.edit.step].to_nl()}. There is no where for me to go."
                return
            self.edit.next_step()
        elif self.context.current_message in ["previous step", "previous", "go back"]:
            if not self.edit.current:
                self._message = "There are no steps in the procedure for me to go."
                return
            if self.edit.at_first_step:
                self._message = f"I am already on the first step, {self.edit.actions[self.edit.step].to_nl()}. There is no where for me to go."
                return
            self.edit.prev_step()
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
                self.context.edit = EditContext(self.context, self.procedure.actions)
                self.edit = self.context.edit
                self.context.current = self.procedure
            return
        setattr(self, attr, value)

class EditContext(object):
    def __init__(self, context, actions):
        self.context = context
        self.actions = actions
        self.step = 0 if self.actions else -1
        self.done = False
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
            return f"{step_message}, where I am {self.current.to_nl()}. What do you want to do? You can say 'done' if you are finished editing."
        else:
            return f"There are currently no actions. What do you want to do?"

    def next_step(self):
        if len(self.actions) != 0 and not self.at_last_step:
            self.step += 1

    def prev_step(self):
        if len(self.actions) != 0 and not self.at_first_step:
            self.step -= 1

    def to_step(self, step):
        assert isinstance(step, int) and step >= -1 and step <= len(self.actions) - 1
        self.step = len(self.actions) - 1 if step == -1 else step

    def remove_current_step(self):
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
        if step is not None:
            self.actions[step:step] = action
        else:
            self.step += 1
            self.actions[self.step:self.step] = action

class GoToStepGoal(StepGoal):
    def __init__(self, context, step=None):
        super().__init__(context)
        if not self.context.edit.current:
            self.error = "There are no steps in the procedure for me to go."
            return
        self.setattr("step", step)

    def complete(self):
        if self.step == "next":
            if self.edit.at_last_step:
                return f"I am already on the last step, {self.edit.actions[self.edit.step].to_nl()}. There is no where for me to go."
            self.edit.next_step()
        elif self.step == "previous":
            if self.edit.at_first_step:
                return f"I am already on the first step, {self.edit.actions[self.edit.step].to_nl()}. There is no where for me to go."
            self.edit.prev_step()
        elif self.step == "first":
            self.edit.to_step(0)
        elif self.step == "last":
            self.edit.to_step(-1)
        else:
            self.edit.to_step(self.step)

        step_message = f"the {self.step} step" if isinstance(self.step, str) else f"step {self.step + 1}"
        return f"Going to {step_message}, where I am {self.edit.actions[self.edit.step].to_nl()}."

    def setattr(self, attr, value):
        if (attr == "step"):
            if value is None:
                self.todos.append(GetInputGoal(self.context, self, attr, "Which step do you want to go to?"))
            else:
                step = value.replace("step", "").replace("the", "").strip()
                try:
                    step = w2n.word_to_num(step) - 1
                    if not isinstance(step, int):
                        self.error = f"Step {step + 1} is not a step."
                    elif step >= len(self.edit.actions) - 1:
                        self.error = f"I cannot go to step {step + 1}. There are only {len(self.edit.actions)} steps."
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
    def __init__(self, context):
        super().__init__(context)
        if len(self.edit.actions) == 0:
            self.error = "There are no actions or steps that you can delete."

    def complete(self):
        message = f"Deleted step {self.edit.step + 1}, where I was {self.edit.actions[self.edit.step].to_nl()}. "
        self.edit.remove_current_step()
        if self.edit.current:
            message += f"Now step {self.edit.step + 1} is where I am {self.edit.actions[self.edit.step].to_nl()}."
        else:
            message += f"Now there are no more actions in the procedure."
        return message

class AddStepGoal(StepGoal):
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
            return "What action do you want to add?"

    def complete(self):
        if not self.edit.current:
            message = f"I added the action, which is the first action in the procedure."
        else:
            message = f"I added the action after step {self.edit.step + 1}."
        self.edit.add_step(self.actions)
        self.context.transition("complete")
        return f"{message} I am at step {self.edit.step + 1} where I am {self.actions[0].to_nl()}."

    def cancel(self):
        self.context.transition("complete")

    def advance(self):
        if self.todos:
            super().advance()
            return

        logger.debug(f"Advancing {self.__class__.__name__}...")
        self._message = None
        if not isinstance(self.context.parsed, BaseGoal):
            self._message = "I didn't quite catch that. What action did you want me to add?"
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
    def __init__(self, context):
        super().__init__(context)
        if len(self.edit.actions) == 0:
            self.error = "There are no actions or steps that you can delete."
        self.context.transition(self)
        self.step = self.edit.step
        self.original_action = self.edit.remove_current_step()
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
            return "What action do you want to replace the current step with?"

    def complete(self):
        self.edit.step = self.step
        self.edit.actions[self.step:self.step] = self.actions
        self.context.transition("complete")
        return f"Changed step {self.edit.step + 1}, where I am now {self.actions[0].to_nl()}."

    def cancel(self):
        self.edit.step = self.step
        self.edit.actions[self.step:self.step] = [self.original_action]
        self.context.transition("complete")

    def advance(self):
        if self.todos:
            super().advance()
            return

        logger.debug(f"Advancing {self.__class__.__name__}...")
        self._message = None
        if not isinstance(self.context.parsed, BaseGoal):
            self._message = "I didn't quite catch that. What do you want to replace the current step with?"
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
