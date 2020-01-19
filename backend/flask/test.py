import logging
from models import *
from client import *

logging.basicConfig(level=logging.DEBUG)
client = Client("test")
dm = client.dm
messages = [
    "run",
    "example",
    "my input"
]
for i, message in enumerate(messages):
    dm.handle_message(message)
    
for m in dm.context.conversation:
    print(m)