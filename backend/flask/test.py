import logging
from models import *
from client import *
from goals import *

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
    "edit",
    "blah",
    "edit example",
    "previous step",
    "next step",
    "go to previous step",
    "continue",
    "next",
    "go to next step",
    "continue",
    "previous step",
    "previous",
    "go back",
    "go to step 5",
    "go to step 100",
    "go to first step",
    "go to the last step",
    "done"
]
edit_test2 = [
    "edit example",
    "next step",
    "delete step",
    "add step",
    "say hello world",
    "add step",
    "remove step",
    "add step",
    "create a variable",
    "nest",
    "4",
    "remove step",
    "change step",
    "say",
    "hello world",
    "previous step",
    "done"
]
edit_test3 = [
    "edit example",
    "delete step",
    "done",
    "run example",
    "5"
]
sound_test = [
    "create a procedure called bark",
    "create a variable called foo and set it to 5",
    "get user input",
    "bar",
    "if bar is equal to dog then play the bark sound",
    "no",
    "play the meow sound",
    "no",
    "done",
    "run bark",
    "cat"
]
sound_test2 = [
    "run dog or cat",
    "cat",
    "run dog or cat",
    "dog"
]

set_test = [
    "create a procedure called set test",
    "create a variable called setting and set it to 5",
    "set variable setting to 6",
    "change setting to 5",
    "change variable to 5",
    "setting",
    "change step",
    "change step to 5",
    "change variable step to 5",
    "change setting",
    "5"
]

create_procedure_test = [
    "create a procedure",
    "my first procedure",
    "create a variable"
]

for i, message in enumerate(set_test):
    logging.info(message)
    res = dm.handle_message(message)
    if res:
        logging.info(res)
