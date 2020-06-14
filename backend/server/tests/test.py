import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import logging
import time
import copy
from models import *
from client import *
from goals import *
from userstudy import *

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
    "close loop",
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
    "what step am i on",
    "delete step",
    "add step",
    "say hello world",
    "which step am i on",
    "add step",
    "remove step",
    "add step",
    "create a variable",
    "nest",
    "4",
    "where am i",
    "remove step",
    "change step",
    "say",
    "hello world",
    "previous step",
    "done"
]

edit_test3 = [
    "create a procedure called edit test 3",
    "say hello",
    "say bye",
    "done",
    "edit edit test 3",
    "next step",
    "next step",
    "previous step",
    "previous step",
    "delete step",
    "what step am i on",
    "add step",
    "say bye"
]

edit_test4 = [
    "open empty",
    "say hello",
    "add step",
    "say hello",
    "what step",
    "create a variable called var",
    "4",
    "say the value of var",
    "add step",
    "set var to 9",
    "say the value of var",
    "previous step",
    "change step",
    "set var to 10",
    "done",
    "run empty"
]

sound_test = [
    "create a procedure called dog",
    "create a variable called foo and set it to 5",
    "get user input",
    "bar",
    "if bar is equal to dog then play the dog sound",
    "no",
    "play the cat sound",
    "no",
    "done",
    "run dog",
    "cat"
]

sound_test2 = [
    "run",
    "dog or cat",
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
    "5",
    "create a variable",
    "my first variable",
    "5",
    "set my first variable to 5",
    "done",
    "run set test"
]

loop_test = [
    "create a procedure called loop test",
    "create a variable called counter and set it to 5",
    "while asdf add 1 to counter",
    "while counter is less than 10 add 1 to counter",
    "close loop",
    "create a variable called counter 2 and set it to 1",
    "until counter 2 is greater than 15, add 2 to counter 2",
    "close loop",
    "create a variable called counter 3 and set it to 0",
    "add 2 to counter 3 until counter 3 is 20",
    "close loop",
    "done",
    "run loop test"
]

conditional_test = [
    "create a procedure called conditional test",
    "create a variable called counter and set it to 5",
    "if adf is less than 10 add 10 to counter",
    "if counter is less than 10 add 10 to asf",
    "if counter is less than 10 then add 1 to counter",
    "done",
    "done",
    "if counter is less than 10",
    "create a conditional",
    "if counter is less than 10",
    "add 3 to counter",
    "done",
    "no",
    "if counter is 9, say the value of counter",
    "no",
    "say it is not 9",
    "no",
    "done",
    "run conditional test"
]

procedure_test = [
    "rename procedure",
    "hello",
    "rename procedure example to hello",
    "rename procedure dog or cat to dog",
    "run dog",
    "cat",
    "make a procedure called deletion",
    "done",
    "what are my procedures",
    "delete deletion"
]

value_of_test = [
    "create a procedure called adding",
    "create a variable called yes and set it to no",
    "done",
    "edit adding",
    "add step",
    "say the value of yes",
    "create a variable called yes yes and set it to no",
    "if yes is equal to value of yes yes say never",
    "done",
    "nothing",
    "done",
    "run adding"
]

subtraction_test = [
    "create a procedure called fire",
    "create a variable called counter and set it to 10",
    "subtract 2 from counter until counter is less than or equal to 0",
    "say value of counter",
    "close loop",
    "done",
    "run fire"
]

subtraction_test2 = [
    "edit empty",
    "create a variable called counter and set it to negative one",
    "until counter is greater than 10 add 2 to counter",
    "close loop",
    "say the value of counter",
    "until counter is less than -1 subtract 4 from counter",
    "close loop",
    "say the value of counter",
    "done",
    "run empty"
]

negative_test = [
    "create a procedure called negative comparison",
    "create a variable called negative",
    "-1",
    "create a variable called positive and set it to 5",
    "say starting loop",
    "until negative is greater than the value of positive say going up",
    "add 5 to negative",
    "say the value of negative",
    "close loop",
    "done",
    "run negative comparison"
]

infinite_while_loop_test = [
    "create a procedure called while loop",
    "create a variable called bad and set it to 0",
    "while bad is not 1 say bad",
    "close loop",
    "done",
    "run while loop",
    "oh no",
    "why is this happening",
    "stop"
]

conditional_test = [
    "create a procedure called hello world",
    "create a variable called counter and set it to 0",
    "create a while loop",
    "while counter is less than 5",
    "get user input and save it as pet",
    "if pet is dog play the dog sound",
    "done",
    "no",
    "if pet is cat play the cat sound",
    "done",
    "no",
    "add 1 to counter",
    "close loop",
    "done",
]

edit_test_while = [
    "create a procedure called hello world",
    "create a variable called hi and set it to 0",
    "create a while loop",
    "while hi is less than 3",
    "add 1 to hi",
    "close loop",
    "say value of hi",
    "done",
    "run hello world",
    "edit hello world",
    "what step",
    "step into",
    "next step",
    "step into",
    "say hi",
    "go to first step",
    "change step",
    "add 2 to hi",
    "next step",
    "delete step",
    "step into",
    "what step",
    "say value of hi",
    "done",
    "done",
    "run hello world",
    "edit hello world",
    "next step",
    "change step",
    "say hi",
    "done",
    "run hello world"
]

until_stop_test = [
    "create a procedure called loop",
    "until i say stop say hello world",
    "close loop",
    "done",
    "run loop",
    "stop"
]

conditional_test = [
    "create a procedure called conditional",
    "create a variable called count and set it to 0",
    "say the value of count",
    "if count is less than 4, add 4 to count",
    "close",
    "say the value of count",
    "done",
    "run conditional",
    "edit conditional",
    "go to step 3"
]

user_input_test = [
    "create a procedure called inputting",
    "listen for user input",
    "nothing",
    "input1",
    "say the value of input1",
    "listen for user input",
    "give me an input",
    "input2",
    "say the value of input2",
    "done",
    "run inputting",
    "hello",
    "bye"
]

bug_test = [
    "create a procedure called test",
    "say hello",
    "done",
    "run test",
    "create a procedure called test1",
    "say hello",
    "done",
    "run test1"
]

logging.basicConfig(level=logging.DEBUG)
client = Client("test")
dm = client.dm
sleep_time = 0.2
for i, message in enumerate(bug_test):
    logging.info(message)
    res = dm.handle_message(message)
    if res:
        logging.info(res)
        logging.info(dm.context.state)
    if message.startswith("run"):
        time.sleep(2)
    time.sleep(sleep_time)

time.sleep(2)
