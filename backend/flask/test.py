from utils import to_snake_case
from models import *
from client import *
import subprocess

client = Client("test")
dm = client.dm
messages = [
    "run example procedure"
]
for i, message in enumerate(messages):
    print("Message:", message)
    dm.handle_message(message)
    print(dm.context.conversation)
    print(str(dm.current_goal()))