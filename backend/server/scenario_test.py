import logging
from models import *
from goals import *
from client import *
from userstudy import *

practice_test = [
    "asdf",
    "create a procedure",
    "blah",
    "create a variable",
    "adfs",
    "run",
    "say",
    "asdfsdf",
    "create a procedure",
    "done",
    "say",
    "hello world",
    "done"
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
    "done"
]

logging.basicConfig(level=logging.INFO)
client = Client("scenario")
dm = UserStudyDialogManager("scenario", novice_scenario)
client.dm = dm

for i, message in enumerate(novice_test):
    logging.debug(message)
    res = dm.handle_message(message)
    if res:
        logging.debug(res)
