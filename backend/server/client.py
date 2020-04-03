from dialog import DialogManager
from userstudy import *

class Client(object):
    """Represent a client with a dialog manager connected to the server"""

    def __init__(self, sid):
        self.id = sid
        self.dm = DialogManager(sid)

class UserStudyClient(Client):
    """Special client for user study containing generated scenarios for all stages and parts"""

    def __init__(self, sid):
        super().__init__(sid)
        self.inputs = {
            "practice": create_practice_scenarios(),
            "novice": create_novice_scenarios(),
            "advanced": create_advanced_scenarios()
        }
