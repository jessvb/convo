import re

ask_what_procedures_regex = "what (.+)?procedures"
ask_what_which_step_regex = "(?:what|which) step(?:.+)?|where am i"

class QuestionAnswer(object):
    """Question and answering module"""
    def __init__(self, context):
        self.context = context

    def answer(self, question):
        """Return response to supported questions"""
        if re.match(ask_what_procedures_regex, question.lower()) and self.context.state == "home":
            # Question about what procedures user has
            response = f"You have {len(self.context.procedures)} procedures."
            names = [f"\"{p}\"" for p in self.context.procedures.keys()]
            if len(names) == 0:
                return f"You have no procedures."
            elif len(names) == 1:
                return response + f" It is {names[0]}"
            else:
                return response + f" They are {', '.join(names[:-1])} and {names[-1]}."
        elif re.match(ask_what_which_step_regex, question.lower()) and self.context.state == "editing":
            # Question about what step user is on during editing
            edit = self.context.edit[-1]
            if not edit.current:
                return f"You currently do not have any actions in the {edit.scope}."

            if edit.at_first_step:
                step_message = f"I am on the first {'and only ' if edit.at_last_step else ''}step"
            elif edit.at_last_step:
                step_message = "I am on the last step"
            else:
                step_message = f"I am on step {edit.step + 1}"
            return f"{step_message} of the {edit.scope}, where I am {edit.current.to_nl()}."

    @staticmethod
    def is_question(message):
        """Naively check if input message is potentially a question"""
        return message.lower().startswith(("what", "which", "when", "how", "where", "why"))
