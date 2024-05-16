# main.py
import speech_recognition as sr
import pyttsx3
import datetime
import spacy
import pyjokes
import weather
import DT
import random
import pyautogui
import ctypes
import time

# Load English tokenizer, tagger, parser, NER, and word vectors
nlp = spacy.load("en_core_web_sm")

# Base class for the voice assistant
class VoiceAssistant:
    def __init__(self, engine):
        self.recognizer = sr.Recognizer()  # Initialize the speech recognizer
        self.engine = engine  # Initialize the text-to-speech engine

    def listen_command(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
            print("Listening...")
            audio = self.recognizer.listen(source)  # Listen for audio input

        try:
            print("Recognizing...")
            command = self.recognizer.recognize_google(audio).lower()  # Recognize speech using Google API
            print("You said:", command)
            return command  # Return the recognized command
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand what you said.")
            return ""  # Return empty string if the speech was not understood
        except sr.RequestError:
            print("Sorry, there was an issue with the speech recognition service.")
            return ""  # Return empty string if there was an error with the request

    def speak(self, text):
        print(f"Speaking: {text}")
        self.engine.say(text)  # Queue the text to be spoken
        self.engine.runAndWait()  # Wait for the speech to be completed

# Derived class for the specific assistant Novah
class Novah(VoiceAssistant):
    def __init__(self, engine):
        super().__init__(engine)
        self.is_awake = False  # Initialize the awake state

    # Function to get the current time of day
    def get_time_of_day(self):
        current_time = datetime.datetime.now(datetime.timezone.utc).astimezone(datetime.timezone(datetime.timedelta(hours=1)))
        hour = current_time.hour
        if 6 <= hour < 12:
            return "morning"
        elif 12 <= hour < 18:
            return "afternoon"
        elif 18 <= hour < 22:
            return "evening"
        else:
            return "night"

    # Function to get a funny response based on the time of day
    def get_funny_response(self, time_of_day):
        if time_of_day == "morning":
            return "Good morning! Let's make this day special. How can I help?"
        elif time_of_day == "afternoon":
            return "Good afternoon! Hope you're having a splendid day!"
        elif time_of_day == "evening":
            return "Good evening! Time to unwind and relax!"
        else:
            return "Good night! Sweet dreams and see you tomorrow!"

    # Function to authenticate the assistant based on wake words
    def authenticate(self, command):
        wake_words = ["hey are you awake", "novah are you awake", "nova are you awake"]
        greeting_words = ["hey novah", "hello novah", "hi novah", "hey nova", "hello nova", "hi nova"]

        if any(word in command for word in wake_words):
            self.speak("For you sir, always.")
            self.is_awake = True
        elif any(word in command for word in greeting_words):
            self.speak("Yes, I am here.")
            self.is_awake = True
        else:
            self.is_awake = False

    # Function to open an application
    def open_application(self, app_name):
        phrases = ["Processing...", "On it...", "Just a second...", "Opening it up..."]
        self.speak(random.choice(phrases))
        if not app_name:
            self.speak("Application name not recognized.")
            return

        pyautogui.press('win')  # Press the Windows key
        time.sleep(1)
        pyautogui.write(app_name)  # Type the application name
        time.sleep(1)
        pyautogui.press('enter')  # Press Enter to open the application
        time.sleep(2)
        hwnd = ctypes.windll.user32.GetForegroundWindow()  # Get the handle of the currently active window
        ctypes.windll.user32.ShowWindow(hwnd, 3)  # Maximize the window
        self.speak(f"{app_name} opened in fullscreen mode.")

    # Function to close an application
    def close_application(self, app_name):
        if not app_name:
            self.speak("Application name not recognized.")
            return

        windows = pyautogui.getWindowsWithTitle(app_name)  # Get the windows with the given title
        if windows:
            windows[0].close()  # Close the first window found
            self.speak(f"The {app_name} application has been closed.")
        else:
            self.speak(f"No {app_name} application found.")

    # Function to scroll up
    def scroll_up(self):
        pyautogui.scroll(900)
        self.speak("Scrolled up.")

    # Function to scroll down
    def scroll_down(self):
        pyautogui.scroll(-900)
        self.speak("Scrolled down.")

    # Function to process a command using NLP
    def process_command(self, command):
        doc = nlp(command)
        verb = None
        obj = None
        for token in doc:
            if token.pos_ in ["VERB", "AUX"]:
                verb = token.lemma_
            if token.pos_ == "NOUN":
                obj = token.text if obj is None else f"{obj} {token.text}"

        return verb, obj

    # Function to listen for commands and process them
    def listen_and_process(self):
        while True:
            command = self.listen_command()
            if command:
                verb, obj = self.process_command(command)
                if verb == "open":
                    self.open_application(obj)
                elif verb in ["exit", "close"]:
                    self.close_application(obj)
                elif "scroll up" in command or "scroll it up" in command:
                    self.scroll_up()
                elif "scroll down" in command or "scroll it down" in command:
                    self.scroll_down()
                elif "joke" in command:
                    joke = pyjokes.get_joke()
                    self.speak("Here's your joke:")
                    self.speak(joke)
                elif any(word in command for word in ['weather', 'climate', 'temperature']):
                    api_key = "42240d393017774c6e0f616dfd7c677b"
                    location = weather.process_input(command)
                    if location:
                        location = weather.expand_country_name(location)
                        weather.get_weather(location, api_key)
                    else:
                        self.speak("Sorry, I couldn't understand your query.")
                elif "date" in command:
                    now = datetime.datetime.now()
                    self.speak(f"Today's date is {now.strftime('%m/%d/%Y')}.")
                else:
                    response = DT.process_query(command)
                    if response:
                        self.speak(response)

    # Function to prompt the user and start processing commands
    def prompt_and_process(self):
        while True:
            command = self.listen_command()
            self.authenticate(command)
            if self.is_awake:
                time_of_day = self.get_time_of_day()
                funny_response = self.get_funny_response(time_of_day)
                self.speak("Hello, " + funny_response)
                self.listen_and_process()
                break

# Entry point of the script
if __name__ == "__main__":
    # Initialize the TTS engine
    engine = pyttsx3.init()

    # Set the speech rate to 190 words per minute
    engine.setProperty('rate', 190)

    # Find and select a male voice
    voices = engine.getProperty('voices')
    male_voice = next((voice for voice in voices if "male" in voice.name.lower()), None)
    if male_voice:
        engine.setProperty('voice', male_voice.id)

    novah = Novah(engine)  # Create an instance of Novah
    novah.prompt_and_process()  # Start the assistant
