import logging
from models import *
from client import *

logging.basicConfig(level=logging.DEBUG)
client = Client("test")
dm = client.dm
messages = [
    "make a procedure called test",
    "say getting user input",
    "get user input and save it as input",
    "say got user input",
    "create a variable called copy",
    "the value of variable input",
    "create a variable called copy two",
    "the value of variable input",
    "add 2 to variable input",
    "say the value of copy",
    "set the variable copy two to the value of input",
    "done",
    "run test",
    "5"
]

for i, message in enumerate(messages):
    logging.info(message)
    res = dm.handle_message(message)
    if res:
        logging.info(res)
