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
    "done",
    "run hello world",
    "create a procedure called hi"
]

client = Client("scenario")
dm = UserStudyDialogManager("scenario", "practice", practice_scenario)
client.dm = dm

for i, message in enumerate(practice_test):
    print("===========================")
    print(f"Message: {message}")
    print(f"State: {dm.context.state}")
    print(f"Goal: {dm.context.current_goal}")
    print(f"Step: {dm.step}")
    print(f"Backup State: {dm.backup_context.state}")
    print(f"Backup Goal: {dm.backup_context.current_goal}")
    res = dm.handle_message(message)
    if res:
        print("---------------------------------")
        print(f"Response: {res}")
        print(f"State: {dm.context.state}")
        print(f"Goal: {dm.context.current_goal}")
        print(f"Step: {dm.step}")
        print(f"Backup State: {dm.backup_context.state}")
        print(f"Backup Goal: {dm.backup_context.current_goal}")
    time.sleep(1)

time.sleep(3)
