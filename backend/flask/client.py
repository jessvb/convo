from dialog import DialogManager

class Client(object):
    def __init__(self, id):
        self.id = id
        self.dm = DialogManager(id)
