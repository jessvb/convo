import logging
from goals import *

logger = logging.getLogger("gunicorn.error")

practice_scenario = [
    ("create a procedure called hello world", CreateProcedureGoal),
    ("say hello world", SayActionGoal),
    ("done", None),
    ("run hello world", ExecuteGoal)
]

novice_scenario = [
    ("create a procedure called pet sounds", CreateProcedureGoal),
    ("get user input and save it as pet", GetUserInputActionGoal),
    ("if pet is dog play the dog sound", ConditionalActionGoal),
    ("done", None),
    ("no", None),
    ("if pet is cat, play the cat sound", ConditionalActionGoal),
    ("done", None),
    ("no", None),
    ("done", None),
    ("run pet sounds", ExecuteGoal)
]

def advanced_scenario_check(execution, response, inputs):
    if response:
        logger.info("Execution resulted in an error response.")
        return False

    if not execution.finished:
        logger.info("Execution did not finish.")
        return False

    pet_sounds = {
        "dog": "dog",
        "cat": "cat"
    }

    get_user_inputs = [emit for emit in execution.emits if emit[0] == "response" and emit[1]["message"] == "Listening for user input..."]
    if len(get_user_inputs) != len(inputs):
        logger.info("Number of times user input is asked is not the same as the number of inputs.")
        return False

    play_sounds = [emit for emit in execution.emits if emit[0] == "playSound"]
    if len(play_sounds) != len(inputs):
        logger.info("Number of sound playing is not the same as the number of inputs.")
        return False

    play_sound_outputs = [(inp, data[1]["sound"]) for (data, inp) in zip(play_sounds, inputs)]
    play_sound_compares = [pet in pet_sounds and pet_sounds[pet] == sound for (pet, sound) in play_sound_outputs]
    if not all(play_sound_compares):
        logger.info(f"The sounds played were not the correct ones: {play_sound_compares}")
        return False

    return True

userstudy_scenarios = {
    "practice": practice_scenario,
    "novice": novice_scenario,
    "advanced": (["dog", "cat", "cat", "dog", "dog"], advanced_scenario_check)
}
