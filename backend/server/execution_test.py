from models import *
from goals import *
from userstudy import *
from dialog import *

correct_actions = [
    CreateVariableAction("counter", 5),
    LoopAction("while", ComparisonCondition(ValueOf("counter"), "greater than", 0), [
        GetUserInputAction("pet"),
        ConditionalAction(EqualityCondition(ValueOf("pet"), "dog"), [[], [PlaySoundAction("dog")]]),
        ConditionalAction(EqualityCondition(ValueOf("pet"), "cat"), [[], [PlaySoundAction("cat")]]),
        SubtractFromVariableAction("counter", 1)
    ])
]

correct_actions2 = [
    CreateVariableAction("asdf", 5),
    LoopAction("while", ComparisonCondition(ValueOf("asdf"), "greater than", 0), [
        GetUserInputAction("pet"),
        ConditionalAction(EqualityCondition(ValueOf("pet"), "cat"), [[], [PlaySoundAction("cat")]]),
        ConditionalAction(EqualityCondition(ValueOf("pet"), "dog"), [[], [PlaySoundAction("dog")]]),
        SubtractFromVariableAction("asdf", 1)
    ])
]

correct_actions3 = [
    CreateVariableAction("counter", 5),
    LoopAction("until", EqualityCondition(ValueOf("counter"), 0), [
        GetUserInputAction("pet"),
        ConditionalAction(EqualityCondition(ValueOf("pet"), "cat"), [[], [PlaySoundAction("cat")]]),
        ConditionalAction(EqualityCondition(ValueOf("pet"), "dog"), [[], [PlaySoundAction("dog")]]),
        SubtractFromVariableAction("counter", 1)
    ])
]

correct_actions4 = [
    CreateVariableAction("counter", 0),
    LoopAction("until", EqualityCondition(ValueOf("counter"), 5), [
        GetUserInputAction("animal"),
        ConditionalAction(EqualityCondition(ValueOf("animal"), "cat"), [[], [PlaySoundAction("cat")]]),
        ConditionalAction(EqualityCondition(ValueOf("animal"), "dog"), [[], [PlaySoundAction("dog")]]),
        AddToVariableAction("counter", 1)
    ])
]

incorrect_actions1 = [
    CreateVariableAction("counter", 5),
    LoopAction("while", ComparisonCondition(ValueOf("counter"), "greater than", 4), [
        GetUserInputAction("pet"),
        ConditionalAction(EqualityCondition(ValueOf("pet"), "dog"), [[PlaySoundAction("dog")], []]),
        ConditionalAction(EqualityCondition(ValueOf("pet"), "cat"), [[PlaySoundAction("cat")], []]),
    ])
]

incorrect_actions2 = [
    PlaySoundAction("dog"),
    PlaySoundAction("cat"),
    PlaySoundAction("cat"),
    PlaySoundAction("dog"),
    PlaySoundAction("dog")
]

incorrect_actions3 = [
    CreateVariableAction("counter", 5),
    LoopAction("while", ComparisonCondition(ValueOf("counter"), "greater than", 0), [
        GetUserInputAction("pet"),
        ConditionalAction(EqualityCondition(ValueOf("pet"), "dog"), [[PlaySoundAction("dog")], []]),
        ConditionalAction(EqualityCondition(ValueOf("pet"), "cat"), [[PlaySoundAction("cat")], []]),
        SubtractFromVariableAction("counter", 1)
    ])
]

incorrect_actions4 = [
    CreateVariableAction("counter", 5),
    LoopAction("while", ComparisonCondition(ValueOf("counter"), "greater than", 4), [
        GetUserInputAction("pet"),
        ConditionalAction(EqualityCondition(ValueOf("pet"), "dog"), [[], [PlaySoundAction("dog")]]),
        ConditionalAction(EqualityCondition(ValueOf("pet"), "cat"), [[], [PlaySoundAction("cat")]]),
        SubtractFromVariableAction("counter", 1)
    ])
]

incorrect_actions5 = [
    CreateVariableAction("counter", 5),
    SayAction(ValueOf("counter"))
]

incorrect_actions6 = [
]

inputs, check = userstudy_scenarios["advanced"]

# def checking(actions):
#     execution = InternalExecution(DialogContext("sid"), actions, inputs)
#     response = execution.run()

#     if response:
#         print("Response incorrect.")
#         return False

#     if not execution.finished:
#         print("Program not finished.")
#         return False

#     pet_sounds = {
#         "dog": "dog",
#         "cat": "cat"
#     }

#     get_user_inputs = [emit for emit in execution.emits if emit[0] == "response" and emit[1]["message"] == "Listening for user input..."]
#     if len(get_user_inputs) != len(inputs):
#         print("Number of getting inputs and provided inputs not the same.")
#         return False

#     play_sounds = [emit for emit in execution.emits if emit[0] == "playSound"]
#     if len(play_sounds) != len(inputs):
#         print("Number of play sounds not the same as number of provided inputs.")
#         return False

#     play_sound_outputs = [(inp, data[1]["sound"]) for (data, inp) in zip(play_sounds, inputs)]
#     play_sound_compares = [pet in pet_sounds and pet_sounds[pet] == sound for (pet, sound) in play_sound_outputs]
#     if not all(play_sound_compares):
#         print("Played sounds are not correct.")
#         return False

#     return True

corrects = [correct_actions, correct_actions2, correct_actions3, correct_actions4]
incorrects = [incorrect_actions1, incorrect_actions2, incorrect_actions3, incorrect_actions4, incorrect_actions5, incorrect_actions6]

print("=============")
print("Corrects")
for acts in corrects:
    execution = InternalExecution(DialogContext("sid"), acts, inputs)
    response = execution.run()
    res = check(execution, response, inputs)
    if res:
        print(res)
print("=============")
print("Incorrects")
print("-----------")
for acts in incorrects:
    execution = InternalExecution(DialogContext("sid"), acts, inputs)
    response = execution.run()
    res = check(execution, response, inputs)
    if res:
        print(res)
print("=============")
