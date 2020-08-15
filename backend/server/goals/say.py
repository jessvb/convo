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

class WeatherActionGoal(ActionGoal):
    def __init__(self, context, phrase):
        super().__init__(context)
        self.setattr("city", phrase)
    
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
                self.todos.append(GetInputGoal(self.context, self, "phrase", f"Would you like to check the humidity, temperature or pressure?"))
            return
        if attr == "phrase":
            if value is None or value not in ["humidity", "weather","pressure","temperature"]:
                self.todos.append(GetInputGoal(self.context, self, "phrase", f"I didn't quite catch that. Did you want to check the temperature, humidity or pressure?"))
            else:
                if value == "temperature":
                    self.phrase = value
                    self.todos.append(GetInputGoal(self.context, self, "format", f"Do you want the temperature in Celsius or Fahrenheit?"))
                else:
                    self.phrase = self.check_weather(self.city, value, None)
            return
        if attr == "format":
            if value not in ['celsius', 'fahrenheit']:
                self.todos.append(GetInputGoal(self.context, self, "format", f"I did not catch that. Do you want the temperature in Celsius or Fahrenheit?"))
            else:
                self.phrase = self.check_weather(self.city, self.phrase, value)
            return
        setattr(self, attr, value)
    
    def check_weather(self, phrase, spec, temp):
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
        current_weather= str(data['weather'][0]['description']) # assign weather
        current_local_humidity = str(data['main']['humidity']) +"%" # assgin humidity
        current_local_pressure = str(data['main']['pressure']) + " hPa"# assign pressure text 
        if spec == "temperature":
            if temp == "fahrenheit":
                current_temp = "The temperature in " + self.city +  " is " + str(float(data['main']['temp'])*9/5 + 32) + " Fahrenheit"
                final += current_temp + "\n"
            else:
                final += "The temperature in " + self.city + " is " + str(data['main']['temp']) + " Celsius"
        if spec == "weather":
            final += "The Weather in " + self.city + " is " + str(current_weather)+ "\n"
        if spec == "humidity":
            final += "The humidity in " + self.city + " is " + str(current_local_humidity)+ "\n"
        if spec == "pressure":
            final += "The pressure in " + self.city + " is " + str(current_local_pressure)+ "\n"
        return final

class GetWeatherActionGoal(ActionGoal):
    def __init__(self, context, city, typeOfWeather, form, var_name):
        super().__init__(context)
        self.city = city
        self.typeofWeather = typeOfWeather
        self.temptype = form
        self.var_name = var_name
        if var_name == None:
            self.todos.append(GetInputGoal(self.context, self, "var", f"What variable name do you want to store the value in?"))
        if typeOfWeather == "temperature":
            if form == None:
                self.todos.append(GetInputGoal(self.context, self, "format", f"Do you want the temperature in Celsius or Fahrenheit?"))
            else:
                self.setattr("format", form)
        if typeOfWeather == None or typeOfWeather == "weather":
            logger.debug("Checking Temp")
            self.todos.append(GetInputGoal(self.context, self, "phrase", f"Would you like to check the humidity, temperature or pressure?"))
        else:
            self.setattr("typeOfWeather", typeOfWeather)
        if city == None:
            self.todos.append(GetInputGoal(self.context, self, "city", f"Which city?"))
        else:
            self.setattr("city", city)
        

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
            return
        elif attr == "phrase":
            if value is None or value not in ["humidity", "weather","pressure","temperature"]:
                self.todos.append(GetInputGoal(self.context, self, "phrase", f"I didn't quite catch that. Did you want to check the temperature, humidity or pressure?"))
            else:
                if value == "temperature":
                    self.typeofWeather = value
                else:
                    self.typeofWeather = value
                    self.temptype = None
            return
        elif attr == "format":
            if value not in ['celsius', 'fahrenheit']:
                self.todos.append(GetInputGoal(self.context, self, "format", f"I did not catch that. Do you want the temperature in Celsius or Fahrenheit?"))
            else:
                self.temptype = value
            return
        elif attr == "var":
            self.var_name = value
            self.phrase = "Done"
            return
             
        setattr(self, attr, value)
    
    def check_weather(self, phrase, spec, temp):
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
        current_weather= data['weather'][0]['description'] # assign weather
        current_local_humidity = data['main']['humidity'] # assgin humidity
        current_local_pressure = data['main']['pressure']# assign pressure text 
        if spec == "temperature":
            if temp == "fahrenheit":
                current_temp = float(data['main']['temp'])*9/5 + 32
                final = current_temp
            else:
                final = data['main']['temp']
        if spec == "weather":
            final = current_weather
        if spec == "humidity":
            final = current_local_humidity
        if spec == "pressure":
            final = current_local_pressure
        return final
