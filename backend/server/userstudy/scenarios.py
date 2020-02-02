from goals import *

practice_scenario = [
    ("create a procedure called hello world", CreateProcedureGoal),
    ("say hello world", SayActionGoal),
    ("done", None),
    ("run hello world", ExecuteGoal)
]

novice_scenario = [
    ("create a procedure called pet sounds", CreateProcedureGoal),
    ("get user input and save it as pet", GetUserInputActionGoal),
    ("if pet is dog play the bark sound", ConditionalActionGoal),
    ("done", None),
    ("no", None),
    ("if pet is cat, play the meow sound", ConditionalActionGoal),
    ("done", None),
    ("no", None),
    ("done", None),
    ("run pet sounds", ExecuteGoal)
]

userstudy_scenarios = {
    "practice": practice_scenario,
    "novice": novice_scenario
}
