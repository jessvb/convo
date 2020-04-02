import logging
from models import *
from goals import *
from client import *
from userstudy import *
from dialog import *
from models import *

novice_test = [
    "create procedure",
    "pet sounds",
    "get user input",
    "pet",
    "if dune is dog play the dog sound",
    "if pet is dog play the dog sound",
    "dafsdf",
    "done",
    "no",
    "if pet is dog play the dog sound",
    "while pet is dog play sound",
    "if pet is dog play the sound",
    "dog",
    "if pet is cat play sound",
    "dog",
    "if pet is cat play sound",
    "cat",
    "asdf",
    "dafsdf",
    "done",
    "no",
    "create a procedure called hi",
    "hi",
    "done",
    "run",
    "adf",
    "run pet sounds"
]

novice_test2 = [
    "create a procedure called pet sounds",
    "get user input and save it as pet",
    "if pet is dog play the dog sound",
    "done",
    "no",
    "if pet is cat, play the cat sound",
    "done",
    "no",
    "done",
    "run pet sounds",
    "dog"
]

practice_test = [
    "create a procedure called hello world",
    "say hello world",
    "reset",
    # "done",
    # "run hello world",
    "create a procedure called hi",
    "create a procedure called hello world"
]

client = UserStudyClient("scenario")
sounds, scenario = client.inputs["novice"]["voice-text"]

print(sounds)
print([s[0] for s in scenario])
novice_test3 = [
    "create a procedure called pet sounds",
    "get user input",
    "pat",
    "get user input",
    "pet",
    f"if the value of pat is {sounds[0]} play the sound",
    f"{sounds[0]}",
    f"if the value of pet is {sounds[0]} play the sound",
    f"{sounds[0]}",
    "done",
    "no"
]

dm = UserStudyDialogManager("scenario", "novice", scenario)
client.dm = dm

for i, message in enumerate(novice_test3):
    print("===========================")
    print(f"Message: {message}")
    # print(f"State: {dm.context.state}")
    # print(f"Goal: {dm.context.current_goal}")
    print(f"Step: {dm.step}")
    # print(f"Backup State: {dm.backup_context.state}")
    # print(f"Backup Goal: {dm.backup_context.current_goal}")
    res = dm.handle_message(message)
    if res:
        print("---------------------------------")
        print(f"Response: {res}")
        # print(f"State: {dm.context.state}")
        # print(f"Goal: {dm.context.current_goal}")
        print(f"Step: {dm.step}")
        # print(f"Backup State: {dm.backup_context.state}")
        # print(f"Backup Goal: {dm.backup_context.current_goal}")
    time.sleep(0.5)

time.sleep(2)
