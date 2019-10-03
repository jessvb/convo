# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/

from typing import Dict, Text, Any, List, Union, Optional

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction

class ActionStoryTime(Action):
    def name(self):
        return "action_story_time"

    def run(self, dispatcher, tracker, domain):
        time = tracker.get_slot("time")
        print(time);
        if time is None:
            dispatcher.utter_template("utter_ask_time", tracker)
        elif time == "bedtime":
            dispatcher.utter_message(f"When is {time}?")
        else:
            dispatcher.utter_template("utter_read_story", tracker)

        return [SlotSet("time", None)]
