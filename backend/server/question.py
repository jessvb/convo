import re
from bert import QA

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
        else:
            # Run BERT Q&A for any other question
            model = QA("model")
            context = "Convo is a voice-based system allowing users to develop computer programs by conversing in natural language with a conversational agent. The possible actions in this system are creating programs, editing programs, and receiving system feedback on how your command has impacted your program. The possible commands in this system are creating procedures, constructing loops, creating conditionals, declaring variables, and listening for user input. Convo uses Google's Cloud Speech-To-Text API to recognize voices and transcribe what a user says. Then, the transcribed output is sent to a WebSocket server where the natural language understanding and post-processing occur. Responses are voiced back to users using Google's Speech Synthesis API. Input phrases are mapped to output commands through a dialog manager, which tracks user goals and stores new states accordingly. Convo is still somewhat constrained in its understanding and setup, which may lead to mistakes or lacking features, but it will definitely improve over time! Our end goal is to develop a programming tool targeted for children to lower the barrier to entry to programming."
            out = model.predict(context, question)
            return jsonify({"result":out})["answer"]

    @staticmethod
    def is_question(message):
        """Naively check if input message is potentially a question"""
        return message.lower().startswith(("what", "which", "when", "how", "where", "why"))
