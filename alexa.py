import sys
from googlesearch import search
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import pyaudio
import time
import math
import requests, json

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    with sr.Microphone() as source:
        print('Listening...')
        engine.say("Hello! How may I help you?")
        engine.runAndWait()
        listener.adjust_for_ambient_noise(source)
        voice = listener.listen(source)

        try:
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '')
                print(command)
        except LookupError:
            print('Could not understand the audio!')
        return command

def run_alexa():
    command = take_command()
    print(command)
    if 'play' in command:
        song = command.replace('play', '')
        talk('playing ' + song)
        pywhatkit.playonyt(song)
    elif 'who is' in command:
        person = command.replace('who is', '')
        info = wikipedia.summary(person, 1)
        print(info)
        talk(info)
    elif 'date' in command:
        #talk('sorry, I have a headache')
        dt = str(datetime.date.today())
        print(dt)
        talk("Today's date is" + dt)
    elif 'are you single' in command:
        talk("yes. I am in a relationship with WiFi.")
    elif 'joke' in command:
        talk(pyjokes.get_joke())
    elif 'weather' in command:
        # enter your API key here.
        api_key = "b49fc337dde81490958f556094103567"

        # base url variable to store url.
        base_url = "http://api.openweathermap.org/data/2.5/weather?"

        # give city name.
        city_name = "thane"

        # variable to store url address. 
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name

        # get method of requests module.
        # return response object.
        response = requests.get(complete_url)

        # python format data.
        x = response.json()

        # city is not found.
        if x["cod"] != "404":
            # store the value of "main".
            # key in the variable 'y'.
            y = x["main"]

            # store the value corresponding.
            # to the temp key of 'x'.
            current_temperature = y["temp"] - 273.15
            vals = math.trunc(current_temperature)
            # print the following values.
            print("The Temperature (In The Celsius Unit) = " + str(vals))
            talk(vals)

        else:
            print('City Not Found.')
            talk('City Not Found.')
    elif 'stop' in command:
        sys.exit()
    else:
        talk('Please repeat the command!')

while True:
# if __name__ == "__main__":
    run_alexa()