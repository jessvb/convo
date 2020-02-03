import logging
from models import *
from goals import *
from client import *
from userstudy import *
from dialog import *
from models import *

conversation = [
    "create a procedure",
    "advance",
    "create a variable",
    "counter",
    "0",
    "well counter is less than 5 add 1/2 counter",
    "while counter is less than 5 add 1/2 counter",
    "well counter is less than 5",
    "while counter is less than 5",
    "add a while loop",
    "well counter is less than 5",
    "wild counter is less than 5",
    "idlewild loop",
    "add a while loop",
    "while counter is less than 5",
    "add 1/2 counter",
    "add one",
    "variable",
    "add one variable counter",
    "add to variable",
    "counter",
    "1",
    "listen for user input",
    "pet",
    "if pet is dog play the dog sound",
    "done",
    "no",
    "if pet is cat play the cat sound",
    "done",
    "done",
    "close the loop",
    "done",
    "done",
    # "run advanced",
    # "run advanced",
    # "run advanced",
    # "an advance",
    # "run the last procedure",
    # "run it",
    # "run advance"
]

client = UserStudyClient("scenario")
sound_pair, inputs = client.inputs["advanced"]["voice-text"]
client.dm = UserStudyAdvancedDialogManager("scenario", inputs, advanced_scenario_check)
dm = client.dm

for m in conversation:
    print(m)
    res = dm.handle_message(m)
    print("==>", res)
