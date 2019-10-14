from transitions import Machine
from editor import ProgramEditor
from utils import *

class Agent(object):
    def __init__(self):
        self.lines = []
        self.current_state = "ask_for_input"

    def parse_message(message):
        