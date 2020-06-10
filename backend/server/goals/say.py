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
class SayActionGoal(ActionGoal):
    """Goal for adding a say action"""
    def __init__(self, context, phrase=None):
        super().__init__(context)
        self.setattr("phrase", phrase)

    def complete(self):
        assert hasattr(self, "actions")
        self.actions.append(SayAction(self.phrase))
        return super().complete()

    def setattr(self, attr, value):
        if attr == "phrase":
            if value is None:
                self.todos.append(GetInputGoal(self.context, self, attr, f"What do you want me to say?"))
            elif isinstance(value, ValueOf):
                if value.variable not in self.variables:
                    self.error = f"Variable, {value.variable}, hasn't been created. Try using an existing variable if you want to try again."
                    return
                self.phrase = value
            else:
                self.phrase = value
            return
        setattr(self, attr, value)

class GreetWelcomeActionGoal(ActionGoal):
    """Adding a welcome action"""
    def __init__(self, context, phrase = "Welcome to Programming"):
        super().__init__(context)
        self.setattr("phrase", phrase)
    
    def complete(self):
        assert hasattr(self, "actions")
        self.actions.append(GreetWelcomeAction(self.phrase))
        return super().complete()
    
    def setattr(self, attr, value):
        if attr == "phrase":
            if value is None:
                self.phrase = "Welcome to Programming"
            else:
                self.phrase = value
            return
        setattr(self, attr, value)

class WeatherActionGoal(ActionGoal):
    def __init__(self, context, phrase):
        super().__init__(context)
        self.setattr("city", self.check_weather(phrase, None))
    
    def complete(self):
        assert hasattr(self, "actions")
        self.actions.append(WeatherAction(self.phrase))
        return super().complete()
    
    def setattr(self, attr, value):
        if attr == "city":
            if value is None:
                self.todos.append(GetInputGoal(self.context, self, attr, f"Which city?"))
            else:
                self.city = value
                self.todos.append(GetInputGoal(self.context, self, "phrase", f"Choose a value [Humidity, Temperature, Date, Pressure]"))
            return
        if attr == "phrase":
            logger.debug("Reached")
            if value is None or value not in ["humidity","date", "weather","pressure","temperature"]:
                self.todos.append(GetInputGoal(self.context, self, "phrase", f"Wrong value make sure the value is one of the following [Humidity, Temperature, Date, Pressure]"))
            else:
                self.phrase = self.check_weather(self.city, value)
            return
        setattr(self, attr, value)
    
    def check_weather(self, phrase, spec):
        if phrase == None:
            return None
        api_key = "ae0dc43f65cd3e7408eee9948d09ea7f"#api key
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=ae0dc43f65cd3e7408eee9948d09ea7f&units=metric'.format(phrase)
        res = requests.get(url)
        final = ""
        data = res.json()
        date_time_str = str(datetime.fromtimestamp(data['dt']))
        date_time_str = date_time_str.split("+")[0]
        new_date = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
        if new_date.hour > 12:
            new_date = new_date.replace(hour = new_date.hour-12)
            text = " PM"
        if new_date.hour == 12:
            text = " PM"
        else:
            text = " AM"
        x = str(new_date).split(" ")
        current_temp = "The temperature is " + str(data['main']['temp']) + " Celsius" # get current temp
        current_time = x[1]
        count = 0
        final_time = "The time is "
        for part in current_time.split(":"):
            if count == 0:
                final_time += part
                final_time += ":"
            if count == 1:
                final_time += part
            count += 1
        final_time += text
        current_time = final_time #assign final time
        current_date = "The date is " + x[0]
        current_weather= "The weather is looking like " + str(data['weather'][0]['description']) # assign weather
        current_local_humidity = "The humidity is " + str(data['main']['humidity']) +"%" # assgin humidity
        current_local_pressure = "The pressure is " + str(data['main']['pressure']) + " hPa"# assign pressure text 
        if spec == "temperature": 
            final += "Current Temperature: " + str(current_temp) + "\n"
        # final += "Current Time: " + str(current_time) + "\n"
        if spec == "date": 
            final += "Current Date: " + str(current_date)+ "\n"
        if spec == "weather":
            final += "Current Weather: " + str(current_weather)+ "\n"
        if spec == "humidity":
            final += "Current Local Humidity: "+ str(current_local_humidity)+ "\n"
        if spec == "pressure":
            final += "Current Local Pressure: "+ str(current_local_pressure)+ "\n"
        return final
