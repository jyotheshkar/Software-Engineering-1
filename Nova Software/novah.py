import speech_recognition as sr
import pyttsx3
import datetime

# Base class for the voice assistant
class VoiceAssistant:
    def __init__(self, engine):
        self.recognizer = sr.Recognizer()  # Initialize the speech recognizer
        self.engine = engine  # Initialize the text-to-speech engine

    # Function to listen for voice commands
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

    # Function to convert text to speech
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
            self.speak("For you, sir, always.")
            self.is_awake = True
        elif any(word in command for word in greeting_words):
            self.speak("Yes, I am here.")
            self.is_awake = True
        else:
            self.is_awake = False

    # Function to prompt the user for a request and process it
    def prompt_request(self):
        while True:
            command = self.listen_command()  # Listen for a command from the user
            self.authenticate(command)  # Authenticate based on the command
            if self.is_awake:
                time_of_day = self.get_time_of_day()  # Get the current time of day
                funny_response = self.get_funny_response(time_of_day)  # Get a funny response based on the time of day
                self.speak("Hello, " + funny_response)  # Speak the funny response
                break  # Exit the loop if the assistant is awake

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
    novah.prompt_request()  # Start the assistant
