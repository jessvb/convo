from dialog import DialogManager
from userstudy import *

class Client(object):
    def __init__(self, sid):
        self.id = id
        self.dm = DialogManager(sid)

class UserStudyClient(Client):
    def __init__(self, sid):
        super().__init__(sid)
        self.inputs = {
            "practice": create_practice_scenarios(),
            "novice": create_novice_scenarios(),
            "advanced": create_advanced_scenarios()
        }
