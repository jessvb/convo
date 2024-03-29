import random
import copy
from goals import *
from app import logger

def advanced_scenario_check(execution, error, inputs):
    """Check whether user has completed the advanced scenario given the specific inputs"""
    logger.debug(f"[ScenarioCheck] Inputs: {inputs}")

    if error:
        # If error, did not complete
        logger.debug("[ScenarioCheck] Execution resulted in an error response.")
        return False

    if not execution.finished:
        # If execution indicate not finished, did not complete
        logger.debug("[ScenarioCheck] Execution did not finish.")
        return False

    # Check if the number of inputs corresponded to the number of inputs asked
    get_user_inputs = [emit for emit in execution.emits if emit[0] == "response" and emit[1]["message"] == "Listening for user input..."]
    logger.debug(f"[ScenarioCheck] Emits: {get_user_inputs}")
    if len(get_user_inputs) != len(inputs):
        logger.debug("[ScenarioCheck] Number of times user input is asked is not the same as the number of inputs.")
        return False

    # Check if sound was played the same amount of time as the number of inputs asked
    play_sounds = [emit for emit in execution.emits if emit[0] == "playSound"]
    logger.debug(f"[ScenarioCheck] Sounds: {play_sounds}")
    if len(play_sounds) != len(inputs):
        logger.debug(f"[ScenarioCheck] Number of sound playing is not the same as the number of inputs: {inputs}")
        return False

    # Check if the correct sounds were played
    play_sound_compares = [data[1]["sound"] == inp for (data, inp) in zip(play_sounds, inputs)]
    if not all(play_sound_compares):
        logger.debug(f"[ScenarioCheck] The sounds played were not the correct ones: {play_sounds}")
        return False

    return True

possible_sound_pairs = [("dog", "cat"), ("bird", "cricket"), ("horse", "cow")]
possible_iterations = [3, 4, 5]

def create_practice_scenarios():
    """Generate all parts for practice scenario"""
    practice_scenario = [("create a procedure called hello world", CreateProcedureGoal),
                         ("say hello world", SayActionGoal),
                         ("done", None),
                         ("run hello world", ExecuteGoal)]
    scenarios = {
        "voice-text": practice_scenario,
        "voice": practice_scenario,
        "text": practice_scenario
    }
    return scenarios

def create_novice_scenario(sound_pair):
    """Create a novice scenario given a pair of animal sounds"""
    a, b = sound_pair
    scenario = [
        ("create a procedure called pet sounds", CreateProcedureGoal),
        ("get user input and save it as pet", GetUserInputActionGoal),
        (f"if the value of pet is {a}, play the {a} sound", ConditionalActionGoal),
        ("done", None),
        ("no", None),
        (f"if the value of pet is {b}, play the {b} sound", ConditionalActionGoal),
        ("done", None),
        ("no", None),
        ("done", None),
        ("run pet sounds", ExecuteGoal)
    ]

    return scenario

def create_novice_scenarios():
    """Generate all parts for novice scenario with randomly chosen animal pair"""
    random.shuffle(possible_sound_pairs)
    scenarios = {
        "voice-text": (possible_sound_pairs[0], create_novice_scenario(possible_sound_pairs[0])),
        "voice": (possible_sound_pairs[1], create_novice_scenario(possible_sound_pairs[1])),
        "text": (possible_sound_pairs[2], create_novice_scenario(possible_sound_pairs[2]))
    }
    return scenarios

def create_advanced_scenarios():
    """Generate all parts for advanced scenario with randomly chosen animal pair and iteration number"""
    random.shuffle(possible_sound_pairs)
    random.shuffle(possible_iterations)
    scenarios = {
        "voice-text": (possible_sound_pairs[0], [random.choice(possible_sound_pairs[0]) for _ in range(possible_iterations[0])]),
        "voice": (possible_sound_pairs[1], [random.choice(possible_sound_pairs[1]) for _ in range(possible_iterations[1])]),
        "text": (possible_sound_pairs[2], [random.choice(possible_sound_pairs[2]) for _ in range(possible_iterations[2])])
    }
    return scenarios
