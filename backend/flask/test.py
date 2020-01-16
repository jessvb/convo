from utils import to_snake_case
from models import *

example_procedure = Procedure(name="example", actions=[
    CreateVariableAction("foo", "5"),
    CreateListAction("groceries"),
    SetVariableAction("foo", "10"),
    IncrementVariableAction("foo", "5"),
    SayAction("hello world!"),
    ConditionalAction(
        ComparisonCondition("foo", "greater than", "10"),
        actions=[
            [SayAction("foo is greater than 10"), CreateVariableAction("bar", "4")],
            [SayAction("foo is not greater than 10"), CreateVariableAction("bar", "10")]
        ]
    ),
    LoopAction(
        ComparisonCondition("bar", "less than", "15"),
        actions=[
            SayAction("bar is less than 15"),
            IncrementVariableAction("bar", "1")
        ]
    ),
    AddToListAction("groceries", "\"apples\"")
])

say_func = """def say(phrase):
    print(phrase)
"""

proc_string = say_func + "\n".join(example_procedure.python()) + "\nexample()"
print(proc_string)

print("\nExecuting...\n")
exec(proc_string)
print()

# example_procedure.klass = "klass"
# example_class = Class(
#     name="klass",
#     properties={
#         "prop1": Property(klass="klass", name="prop1", type="number"),
#         "prop2": Property(klass="klass", name="prop2", type="string")
#     },
#     procedures={
#         "example": example_procedure
#     }
# )

# string = "\n".join(example_class.python())
# print(string)
# exec(string)