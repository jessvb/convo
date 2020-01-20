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
    "say the value of copy",
    "if copy is greater than 3 then add 10 to variable copy",
    "done",
    "no",
    "say getting input two",
    "get user input and save it as input two",
    "say got user input two",
    "create a variable called copy two",
    "the value of variable input",
    "add 2 to variable input",
    "say the value of copy",
    "set the variable copy two to the value of input",
    "add 2 to variable copy two until copy two is greater than 12",
    "done",
    "create a variable called copy three and set it to the value of input two",
    "done",
    "run test",
    "5",
    "10"
]
messages2 = [
    "run example",
    "hi"
]

for i, message in enumerate(messages2):
    logging.info(message)
    res = dm.handle_message(message)
    if res:
        logging.info(res)
