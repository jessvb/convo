import re

ask_what_procedures_regex = "what (.+)?procedures"
ask_what_which_step_regex = "(?:what|which) step(?:.+)?|where am i"

class QuestionAnswer(object):
    def __init__(self, context):
        self.context = context

    def answer(self, question):
        if re.match(ask_what_procedures_regex, question.lower()) and self.context.state == "home":
            response = f"You have {len(self.context.procedures)} procedures."
            names = [f"\"{p}\"" for p in self.context.procedures.keys()]
            if len(names) == 0:
                return f"You have no procedures."
            elif len(names) == 1:
                return response + f" It is {names[0]}"
            else:
                return response + f" They are {', '.join(names[:-1])} and {names[-1]}."
        elif re.match(ask_what_which_step_regex, question.lower()) and self.context.state == "editing":
            edit = self.context.edit
            if not edit.current:
                return "You currently do not have any actions."

            if edit.at_first_step:
                step_message = f"I am on the first {'and only ' if edit.at_last_step else ''}step"
            elif edit.at_last_step:
                step_message = "I am on the last step"
            else:
                step_message = f"I am on step {edit.step + 1}"
            return f"{step_message}, where I am {edit.current.to_nl()}."

    @staticmethod
    def is_question(message):
        return message.lower().startswith(("what", "which", "when", "how", "where", "why"))
