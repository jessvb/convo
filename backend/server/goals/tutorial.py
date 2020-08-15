from models import *
from goals import *
from helpers import *
from app import logger
import requests
from datetime import datetime
import sqlite3
import math
import pprint
import random

class ChooseTutorialGoal(TutorialGoal):
    def __init__(self, context, phrase=None):
        super().__init__(context)
        self.tutorial = Tutorial(phrase)
        self.context.current = self.tutorial
        self.setattr("phrase", phrase)

    def complete(self):
        assert hasattr(self, "actions")
        self.context.transition(self)
        self.context.current = self.tutorial
        return super().complete()
    
    def setattr(self, attr, value):
        if (attr == "phrase"):
            if value is None:
                self.todos.append(GetInputGoal(self.context, self, attr, "Which tutorial do you want to initiate?"))
            else:
                self.tutorial = Tutorial(value)
            return
        setattr(self, attr, value)