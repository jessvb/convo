import re

ask_what_procedures_regex = "what (.+)?procedures"
ask_what_which_step_regex = "(?:what|which) step(?:.+)?|where am i"

class QuestionAnswer(object):
    def __init__(self, context):
        self.context = context

    def answer(self, question):
        if re.match(ask_what_procedures_regex, question) and self.context.state == "home":
            response = f"You have {len(self.context.procedures)} procedures."
            names = [f"\"{p}\"" for p in self.context.procedures.keys()]
            if len(names) == 0:
                return f"You have no procedures."
            elif len(names) == 1:
                return response + f" It is {names[0]}"
            else:
                return response + f" They are {', '.join(names[:-1])} and {names[-1]}."
        elif re.match(ask_what_which_step_regex, question) and self.context.state == "editing":
            edit = self.context.edit
            if edit.step == -1:
                return "You currently have no steps."
            return f"I am on step {edit.step + 1} where I am {edit.actions[edit.step].to_nl()}"

    @staticmethod
    def is_question(message):
        return message.startswith(("what", "which", "when", "how", "where", "why"))
