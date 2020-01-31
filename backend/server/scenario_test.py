from models import *
from goals import *
from client import *

def check_goal_state(goal, state):
    return lambda c: (isinstance(c.current_goal, goal) if goal else True) and c.state == state

def check_actions(actions):
    return lambda c: context.current and context.current.actions and context.current.actions == actions


# practice = [
#     [ check_goal_state(CreateProcedureGoal, "creating") ],
#     [
#         check_goal_state(CreateProcedureGoal, "creating"),
#         check_actions([SayAction("hello world")])
#     ],
#     [ check_goal_state(None, "home") ]
# ]

# novice = [
#     [ check_goal_state(CreateProcedureGoal, "creating") ],
#     [  ]
# ]

practice1 = [
    "I want to create a procedure",
    "hello world",
    "say hello world",
    "done",
    "run hello world"
]

practice2 = [
    "I want to create a procedure called hello world",
    "say",
    "hello world",
    "done",
    "run hello world"
]

novice1 = [
    "I want to create a procedure called pet sounds",
    "get user input",
    "input",
    "if input is dog play the bark sound",
    "done",
    "no",
    "if input is cat, play the meow sound",
    "done",
    "no",
    "done",
    "run pet sounds"
]

novice2 = [
    "I want to create a procedure",
    "pet sounds",
    "get user input",
    "input",
    "if input is dog play sound",
    "bark",
    "done",
    "no",
    "if input is cat, play the meow sound",
    "done",
    "no",
    "done",
    "run",
    "pet sounds"
]

logging.basicConfig(level=logging.INFO)
goals = []
for messages in [novice1, novice2]:
    goals.append([])
    client = Client("scenario")
    dm = client.dm
    j = 0
    for i, message in enumerate(messages):
        # logging.info(message)
        res = dm.handle_message(message)
        # if res:
        #     logging.info(res)
        goal = (j, str(dm.current_goal()), dm.current_immediate_goal(), dm.context.state)
        goals[-1].append(goal)
        time.sleep(0.5)
        if not goal[1].endswith("get_input"):
            j += 1

    logging.info("Sleeping for 3 seconds...")
    time.sleep(3)

# print(goals)

goals_input_removed1 = [(goal[0], goal[1]) for goal in goals[0] if not goal[1].endswith("get_input")]
goals_input_removed2 = [(goal[0], goal[1]) for goal in goals[1] if not goal[1].endswith("get_input")]
print(goals_input_removed1)
print(goals_input_removed2)
print(goals_input_removed1 == goals_input_removed2)

actions_input_removed1 = [(goal[0], goal[2].actions) for goal in goals[0] if str(goal[2]).endswith("_actions")]
actions_input_removed2 = [(goal[0], goal[2].actions) for goal in goals[1] if str(goal[2]).endswith("_actions")]
print(actions_input_removed1)
print(actions_input_removed2)
print(actions_input_removed1 == actions_input_removed2)

states1 = [(goal[0], goal[3]) for goal in goals[0] if str(goal[2]).endswith("None")]
states2 = [(goal[0], goal[3]) for goal in goals[1] if str(goal[2]).endswith("None")]
print(states1)
print(states2)
print(states1 == states2)