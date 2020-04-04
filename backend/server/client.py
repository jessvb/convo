from dialog import DialogManager
from userstudy import *

class Client(object):
    """Represent a client with a dialog manager connected to the server"""

    def __init__(self, id):
        self.id = id
        self.dm = DialogManager(id)

class UserStudyClient(Client):
    """Special client for user study containing generated scenarios for all stages and parts"""

    def __init__(self, id):
        super().__init__(id)
        self.inputs = {
            "practice": create_practice_scenarios(),
            "novice": create_novice_scenarios(),
            "advanced": create_advanced_scenarios()
        }
