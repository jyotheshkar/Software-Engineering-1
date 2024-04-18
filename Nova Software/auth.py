
import random
import speech_recognition as sr
import time
import spacy
import pyttsx3
import gui  # Importing the GUI module

# Initialize pyttsx3 engine with slower speed
engine = pyttsx3.init()
engine.setProperty('rate', 193)  # Adjust the value as needed, default is 200

# Initialize Spacy NLP model
nlp = spacy.load("en_core_web_sm")

# Activation phrases
activation_phrases = ["hey", "hello", "hey nova", "hello nova", "hey buddy", "buddy", "hi nova"]

# Function to respond based on the current time
def get_greeting():
    current_time = time.localtime()
    if current_time.tm_hour < 12:
        return "Good morning"
    elif 12 <= current_time.tm_hour < 18:
        return "Good afternoon"
    else:
        return "Good evening"

# Function to process user's command
def process_command(command):
    if any(phrase in command.lower() for phrase in activation_phrases):
        greeting = get_greeting()
        return f"{random.choice(['Hello!', 'Hey!', 'Hey there!', 'Greetings!'])} {greeting}. Stand by for Biometric scan."
    elif "are you awake" in command.lower():
        greeting = get_greeting()
        return f"Yes, I am awake. {greeting}. Stand by for Biometric scan."
    elif "camera opened" in command.lower():
        return "Biometrics Authentication successful. Activating desktop autopilot environment."
    else:
        return "I'm sorry, I didn't understand that."

# Function to listen to user's voice command
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio)
        return command
    except sr.UnknownValueError:
        print("Could not understand audio")
        return ""
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        return ""

# Function to speak the response
def speak(response):
    print(response)
    engine.say(response)
    engine.runAndWait()

# Main loop
while True:
    command = listen()
    if command:
        response = process_command(command)
        speak(response)
        if "camera opened" in command.lower():
            gui.open_gui()  # Call the open_gui function from the gui module
