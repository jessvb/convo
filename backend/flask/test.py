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
    "if copy is greater than three then add ten to variable copy",
    "done",
    "no",
    "say getting input two",
    "get user input and save it as input two",
    "say got user input two",
    "create a variable called copy two",
    "the value of variable input",
    "add two to variable input",
    "say the value of copy",
    "set the variable copy two to the value of input",
    "add two to variable copy two until copy two is greater than twelve",
    "done",
    "create a variable called copy three and set it to the value of input two",
    "done",
    "run test",
    "five",
    "10"
]
messages2 = [
    "create a procedure",
    "text",
    "say hello world",
    "create a variable",
    "input",
    "5",
    "say the value of imports",
    "say the value of input",
    "done",
    "run test",
    "run test",
    "run text"
]
messages3 = [
    "create a procedure called fire",
    "create a variable called foo",
    "5",
    "set the variable bar",
    "create a variable called foo",
    "set the variable foo",
    "10"
]
edit_test = [
    "edit blah",
    "edit example",
    "previous step",
    "next step",
    "next step",
    "next",
    "next step",
    "continue",
    "next",
    "continue",
    "next",
    "next step",
    "continue",
    "previous step",
    "previous",
    "go back",
    "done"
]

for i, message in enumerate(edit_test):
    logging.info(message)
    res = dm.handle_message(message)
    if res:
        logging.info(res)
