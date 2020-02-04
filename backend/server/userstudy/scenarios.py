import random
import copy
from goals import *
from app import logger

def advanced_scenario_check(execution, response, inputs):
    if response:
        logger.info("Execution resulted in an error response.")
        return False

    if not execution.finished:
        logger.info("Execution did not finish.")
        return False

    get_user_inputs = [emit for emit in execution.emits if emit[0] == "response" and emit[1]["message"] == "Listening for user input..."]
    if len(get_user_inputs) != len(inputs):
        logger.info("Number of times user input is asked is not the same as the number of inputs.")
        return False

    play_sounds = [emit for emit in execution.emits if emit[0] == "playSound"]
    if len(play_sounds) != len(inputs):
        logger.info("Number of sound playing is not the same as the number of inputs.")
        return False

    play_sound_compares = [data[1]["sound"] == inp for (data, inp) in zip(play_sounds, inputs)]
    if not all(play_sound_compares):
        logger.info(f"The sounds played were not the correct ones: {play_sound_compares}")
        return False

    return True

possible_sound_pairs = [("dog", "cat"), ("bird", "cricket"), ("horse", "cow")]
possible_iterations = [3, 4, 5]

def create_practice_scenarios():
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
    random.shuffle(possible_sound_pairs)
    scenarios = {
        "voice-text": (possible_sound_pairs[0], create_novice_scenario(possible_sound_pairs[0])),
        "voice": (possible_sound_pairs[1], create_novice_scenario(possible_sound_pairs[1])),
        "text": (possible_sound_pairs[2], create_novice_scenario(possible_sound_pairs[2]))
    }
    return scenarios

def create_advanced_scenarios():
    random.shuffle(possible_sound_pairs)
    random.shuffle(possible_iterations)
    scenarios = {
        "voice-text": (possible_sound_pairs[0], [random.choice(possible_sound_pairs[0]) for _ in range(possible_iterations[0])]),
        "voice": (possible_sound_pairs[1], [random.choice(possible_sound_pairs[1]) for _ in range(possible_iterations[1])]),
        "text": (possible_sound_pairs[2], [random.choice(possible_sound_pairs[2]) for _ in range(possible_iterations[2])])
    }
    return scenarios
