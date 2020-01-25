from goals import *
from models import *

class EditGoal(BaseGoal):
    def __init__(self, context, name=None):
        super().__init__(context)
        self.edit = None
        self.setattr("name", name)

    @property
    def message(self):
        if self.error:
            return self.error

        if self._message:
            return self._message

        if self.is_complete:
            return "Done with editing program."

        if len(self.todos) == 0:
            return self.edit.message()
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

    def advance(self):
        if self.todos:
            super().advance()
            return

        logging.debug(f"Advancing {self.__class__.__name__}...")
        self._message = None
        if self.context.current_message == "done":
            self.edit.done = True
        elif self.context.current_message in ["next step", "continue", "next"]:
            self.edit.next_step()
        elif self.context.current_message in ["previous step", "previous", "go back"]:
            self.edit.prev_step()
        elif not isinstance(self.context.parsed, BaseGoal):
            self._message = "I didn't quite catch that. What do you want me to do?"
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

    def setattr(self, attr, value):
        if (attr == "name"):
            if value is None:
                self.todos.append(GetInputGoal(self.context, self, attr, "What do you want to edit?"))
            elif value not in self.context.procedures:
                self.error = f"The procedure, {value}, hasn't been created, so there's nothing to edit. You can create it by saying, \"create a procedure called {value}.\""
            else:
                self.name = value
                self.procedure = self.context.procedures[value]
                self.context.edit = EditContext(self.context, self.procedure.actions)
                self.edit = self.context.edit
            return
        setattr(self, attr, value)

class EditContext(object):
    def __init__(self, context, actions):
        self.context = context
        self.actions = actions
        self.step = 0 if self.actions else -1
        self.done = False
        logging.debug(f"Actions: {[str(a) for a in actions]}")

    @property
    def current(self):
        return self.actions[self.step] if self.step >= 0 else None

    @property
    def at_last_step(self):
        return self.step == len(self.actions) - 1

    @property
    def at_first_step(self):
        return self.step == 0

    def message(self):
        if self.current:
            if self.at_last_step:
                step_message = "I am on the last step"
            elif self.at_first_step:
                step_message = "I am on the first step"
            else:
                step_message = f"I am on step {self.step}"
            return f"{step_message}, where I am {self.current.to_nl()}. What do you want to do?"
        else:
            return f"There are currently no actions. What do you want to do?"

    def next_step(self):
        if len(self.actions) != 0 and not self.at_last_step:
            self.step += 1

    def prev_step(self):
        if len(self.actions) != 0 and not self.at_first_step:
            self.step -= 1
