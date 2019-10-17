from editor import ProgramEditor
from nlu import DebugNLU
from handler import ProcedureHandler

class DialogManager(object):
    def __init__(self):
        self.editor = ProgramEditor()
        self.nlu = DebugNLU()
        self.conversation = []
        self.stack = []

    def add(self, message):
        try:
            self.conversation.append(("U", message))

            action = self.nlu.identify_action(message)
            if self.stack:
                if action.id != self.stack[-1].id and not action.allow_nesting:
                    raise Exception("Complete current action first before proceeding.")
                action = self.nlu.edit_action(message, self.stack.pop())

            is_complete, response = action.is_complete()

            if is_complete:
                self.editor.add(action)
            else:
                self.stack.append(action)
        except Exception as e:
            response = str(e)
        finally:
            self.conversation.append(("A", response))
            return response
