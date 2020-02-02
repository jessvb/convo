import logging
from models import *
from goals import *
from client import *
from userstudy import *

practice_test = [
    "run",
    "asdf",
    "create a procedure",
    "blah",
    "create a procedure called hello world",
    "create a variable",
    "adfs",
    "run",
    "say",
    "asdfsdf",
    "create a procedure",
    "done",
    "say",
    "hello world",
    "done",
    "run hello"
]

novice_test = [
    "create procedure",
    "pet sounds",
    "get user input",
    "input",
    "if dune is dog play the bark sound",
    "if input is dog play the bark sound",
    "dafsdf",
    "done",
    "no",
    "if input is dog play the bark sound",
    "while input is dog play sound",
    "if input is dog play the sound",
    "bark",
    "if input is cat play sound",
    "bark",
    "if input is cat play sound",
    "meow",
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

logging.basicConfig(level=logging.INFO)
client = Client("scenario")
dm = UserStudyDialogManager("scenario", "novice", novice_scenario)
client.dm = dm

for i, message in enumerate(novice_test):
    print("===========================")
    logging.info(f"Message: {message}")
    logging.info(f"State: {dm.context.state}")
    logging.info(f"Goal: {dm.context.current_goal}")
    logging.info(f"Step: {dm.step}")
    logging.info(f"Backup State: {dm.backup_context.state}")
    logging.info(f"Backup Goal: {dm.backup_context.current_goal}")
    res = dm.handle_message(message)
    if res:
        print("---------------------------------")
        logging.info(f"Response: {res}")
        logging.info(f"State: {dm.context.state}")
        logging.info(f"Goal: {dm.context.current_goal}")
        logging.info(f"Step: {dm.step}")
        logging.info(f"Backup State: {dm.backup_context.state}")
        logging.info(f"Backup Goal: {dm.backup_context.current_goal}")
