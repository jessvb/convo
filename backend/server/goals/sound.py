from goals import *
from models import *
import random

available_sounds = set([
    "dog",
    "cat",
    "horse",
    "cow",
    "bird",
    "cricket"
])

random_sound_words = set([
    "random",
    "any",
    "a",
    "animal",
])

class PlaySoundActionGoal(ActionGoal):
    """Goal for adding a play sound action"""
    def __init__(self, context, sound=None):
        super().__init__(context)
        self.setattr("sound", sound)

    def complete(self):
        assert hasattr(self, "actions")
        self.actions.append(PlaySoundAction(self.sound))
        return super().complete()

    def setattr(self, attr, value):
        if attr == "sound":
            if value is None:
                self.todos.append(GetInputGoal(self.context, self, attr, "What sound do you want me to play?"))
            else:
                if value in random_sound_words:
                    sound = random.choice(list(available_sounds))
                else:
                    sound = value.replace("sound", "").replace("the", "").strip()
                if sound not in available_sounds:
                    self.error = f"I cannot play the {value} sound. I might not have this sound file."
                else:
                    self.sound = sound
            return
        setattr(self, attr, value)
