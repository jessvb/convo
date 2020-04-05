import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import json
from helpers import convert_to_dict, convert_to_object
from models import *

say_condition = SayCondition("say")
equality_condition = EqualityCondition("equality", 0, True)
comparison_condition = ComparisonCondition("comparison", ">", ValueOf("value"))

create_variable_action = CreateVariableAction("create", 5)
set_variable_action = SetVariableAction("set", ValueOf("value"))
add_to_variable_action = AddToVariableAction("add", 1)
subtract_from_variable_action = SubtractFromVariableAction("subtract", 2)
say_action = SayAction("say")
get_user_input_action = GetUserInputAction("input")
play_sound_action = PlaySoundAction("sound")

conditional_action = ConditionalAction(say_condition,
    [[create_variable_action, say_action], [add_to_variable_action, subtract_from_variable_action]])
while_loop_action = LoopAction("while", equality_condition, [say_action, get_user_input_action, play_sound_action])
until_loop_action = LoopAction("until", comparison_condition, [])

procedure = Procedure("example", [conditional_action, while_loop_action, until_loop_action])

data = json.dumps(procedure, default=convert_to_dict, indent=4)
print(data)

deserialized = json.loads(data, object_hook=convert_to_object)
print(deserialized == procedure)
