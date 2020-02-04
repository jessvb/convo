import logging
from models import *
from goals import *
from client import *
from userstudy import *
from dialog import *
from models import *

client = UserStudyClient("scenario")
sound_pair, inputs = client.inputs["advanced"]["voice-text"]

conversation = [
    "create a procedure called events",
    "create a variable called count",
    "0",
    "create a while loop",
    f"while count is less than {len(inputs)}",
    "add 1 to 10",
    "add 1/2 count",
    "add 1/2 count",
    "add 1/2 count",
    "10 + 1",
    "add to variable",
    "count",
    "1",
    "get user input",
    "animal",
    f"if animal is {sound_pair[0]} play the {sound_pair[0]} song",
    f"if animal is {sound_pair[0]} play the {sound_pair[0]} sound",
    "if the nevermind",
    "done",
    "no",
    f"if animal is {sound_pair[1]} play the {sound_pair[1]} sound",
    "done",
    "no",
    "closed loop",
    "done",
    "run events",
    f"{sound_pair[0]}"
]

client.dm = UserStudyAdvancedDialogManager("scenario", inputs, advanced_scenario_check)
dm = client.dm

for m in conversation:
    print(m)
    res = dm.handle_message(m)
    print("==>", res)
    time.sleep(1)

time.sleep(2)