from models import *
from goals import *
from userstudy import *
from dialog import *
from client import *

def correct_actions(sound_pair, length):
    return [
        CreateVariableAction("counter", length),
        LoopAction("while", ComparisonCondition(ValueOf("counter"), "greater than", 0), [
            GetUserInputAction("pet"),
            ConditionalAction(EqualityCondition(ValueOf("pet"), sound_pair[0]), [[], [PlaySoundAction(sound_pair[0])]]),
            ConditionalAction(EqualityCondition(ValueOf("pet"), sound_pair[1]), [[], [PlaySoundAction(sound_pair[1])]]),
            SubtractFromVariableAction("counter", 1)
        ])
    ]

def correct_actions2(sound_pair, length):
    return [
        CreateVariableAction("asdf", length),
        LoopAction("while", ComparisonCondition(ValueOf("asdf"), "greater than", 0), [
            GetUserInputAction("pet"),
            ConditionalAction(EqualityCondition(ValueOf("pet"), sound_pair[1]), [[], [PlaySoundAction(sound_pair[1])]]),
            ConditionalAction(EqualityCondition(ValueOf("pet"), sound_pair[0]), [[], [PlaySoundAction(sound_pair[0])]]),
            SubtractFromVariableAction("asdf", 1)
        ])
    ]

def correct_actions3(sound_pair, length):
    return [
        CreateVariableAction("counter", length),
        LoopAction("until", EqualityCondition(ValueOf("counter"), 0), [
            GetUserInputAction("pet"),
            ConditionalAction(EqualityCondition(ValueOf("pet"), sound_pair[1]), [[], [PlaySoundAction(sound_pair[1])]]),
            ConditionalAction(EqualityCondition(ValueOf("pet"), sound_pair[0]), [[], [PlaySoundAction(sound_pair[0])]]),
            SubtractFromVariableAction("counter", 1)
        ])
    ]

def correct_actions4(sound_pair, length):
    return [
        CreateVariableAction("counter", 0),
        LoopAction("until", EqualityCondition(ValueOf("counter"), length), [
            GetUserInputAction("animal"),
            ConditionalAction(EqualityCondition(ValueOf("animal"), sound_pair[1]), [[], [PlaySoundAction(sound_pair[1])]]),
            ConditionalAction(EqualityCondition(ValueOf("animal"), sound_pair[0]), [[], [PlaySoundAction(sound_pair[0])]]),
            AddToVariableAction("counter", 1)
        ])
    ]

def incorrect_actions1(sound_pair, length):
    return [
        CreateVariableAction("counter", length),
        LoopAction("while", ComparisonCondition(ValueOf("counter"), "greater than", 4), [
            GetUserInputAction("pet"),
            ConditionalAction(EqualityCondition(ValueOf("pet"), sound_pair[0]), [[PlaySoundAction(sound_pair[0])], []]),
            ConditionalAction(EqualityCondition(ValueOf("pet"), sound_pair[1]), [[PlaySoundAction(sound_pair[1])], []]),
        ])
    ]

def incorrect_actions2(sound_pair, length):
    return [
        PlaySoundAction(sound_pair[0]),
        PlaySoundAction(sound_pair[1]),
        PlaySoundAction(sound_pair[1]),
        PlaySoundAction(sound_pair[0]),
        PlaySoundAction(sound_pair[0])
    ]

def incorrect_actions3(sound_pair, length):
    return [
        CreateVariableAction("counter", length),
        LoopAction("while", ComparisonCondition(ValueOf("counter"), "greater than", 0), [
            GetUserInputAction("pet"),
            ConditionalAction(EqualityCondition(ValueOf("pet"), sound_pair[0]), [[PlaySoundAction(sound_pair[0])], []]),
            ConditionalAction(EqualityCondition(ValueOf("pet"), sound_pair[1]), [[PlaySoundAction(sound_pair[1])], []]),
            SubtractFromVariableAction("counter", 1)
        ])
    ]

def incorrect_actions4(sound_pair, length):
    return [
        CreateVariableAction("counter", length),
        LoopAction("while", ComparisonCondition(ValueOf("counter"), "greater than", 4), [
            GetUserInputAction("pet"),
            ConditionalAction(EqualityCondition(ValueOf("pet"), sound_pair[0]), [[], [PlaySoundAction(sound_pair[0])]]),
            ConditionalAction(EqualityCondition(ValueOf("pet"), sound_pair[1]), [[], [PlaySoundAction(sound_pair[1])]]),
            SubtractFromVariableAction("counter", 1)
        ])
    ]

def incorrect_actions5(sound_pair, length):
    return [
        CreateVariableAction("counter", length),
        SayAction(ValueOf("counter"))
    ]

def incorrect_actions6(sound_pair, length):
    return []

client = UserStudyClient("test")
corrects = [correct_actions, correct_actions2, correct_actions3, correct_actions4]
incorrects = [incorrect_actions1, incorrect_actions2, incorrect_actions3, incorrect_actions4, incorrect_actions5, incorrect_actions6]

sound_pair, inputs = client.inputs["advanced"]["voice"]

print("=============")
print("Corrects")
for acts in corrects:
    execution = InternalExecution(DialogContext("sid"), acts(sound_pair, len(inputs)), inputs)
    response = execution.run()
    res = advanced_scenario_check(execution, response, inputs)
    print(res)
print("=============")
print("Incorrects")
print("-----------")
for acts in incorrects:
    execution = InternalExecution(DialogContext("sid"), acts(sound_pair, len(inputs)), inputs)
    response = execution.run()
    res = advanced_scenario_check(execution, response, inputs)
    print(res)
print("=============")
