from editor import ProgramEditor
from nlu import DebugNLU

class DialogManager(object):
    def __init__(self):
        self.editor = ProgramEditor()
        self.nlu = DebugNLU()
        self.conversation = []
        self.stack = []

    def add(self, message):
        try:
            self.conversation.append(("U", message))

            if self.stack:
                action = self.nlu.edit_action(message, self.stack.pop())
            else:
                action = self.nlu.identify_action(message)

            is_complete, response = action.is_complete()
            if is_complete:
                self.editor.add(action)
            else:
                self.stack.append(action)
        except Exception as e:
            response = str(e)
        finally:
            self.conversation.extend(("A", response))
            return response
