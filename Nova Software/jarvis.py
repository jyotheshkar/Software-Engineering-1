# novah.py
import speech_recognition as sr
import pyttsx3
import datetime

class VoiceAssistant:
    def __init__(self, engine):
        self.recognizer = sr.Recognizer()
        self.engine = engine

    def listen_command(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            print("Listening...")
            audio = self.recognizer.listen(source)

        try:
            print("Recognizing...")
            command = self.recognizer.recognize_google(audio).lower()
            print("You said:", command)
            return command
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand what you said.")
            return ""
        except sr.RequestError:
            print("Sorry, there was an issue with the speech recognition service.")
            return ""

    def speak(self, text):
        print(f"Speaking: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

class Jarvis(VoiceAssistant):
    def __init__(self, engine):
        super().__init__(engine)
        self.is_awake = False

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

    def get_funny_response(self, time_of_day):
        if time_of_day == "morning":
            return "Good morning! Let's make this day special. How can I help?"
        elif time_of_day == "afternoon":
            return "Good afternoon! Hope you're having a splendid day!"
        elif time_of_day == "evening":
            return "Good evening! Time to unwind and relax!"
        else:
            return "Good night! Sweet dreams and see you tomorrow!"

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

    def prompt_request(self):
        while True:
            command = self.listen_command()
            self.authenticate(command)
            if self.is_awake:
                time_of_day = self.get_time_of_day()
                funny_response = self.get_funny_response(time_of_day)
                self.speak("Hello, " + funny_response)
                break

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

    jarvis = Jarvis(engine)
    jarvis.prompt_request()
