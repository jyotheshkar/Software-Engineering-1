
# makenotes.py
import os
import datetime
import speech_recognition as sr
import pyautogui
import pyttsx3
import spacy

class NotesMaker:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)  # Adjust speech rate
        self.nlp = spacy.load("en_core_web_sm")

    def listen_command(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)  # Adjust for ambient noise
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
        voices = self.engine.getProperty('voices')
        # Set voice to Microsoft Zira Desktop
        for voice in voices:
            if "Zira" in voice.name:
                self.engine.setProperty('voice', voice.id)
                break
        self.engine.say(text)
        self.engine.runAndWait()

    def open_notepad(self):
        # Press Windows key
        pyautogui.press("win")
        pyautogui.sleep(1)

        # Search for Notepad
        pyautogui.write("notepad")
        pyautogui.sleep(1)
        pyautogui.press("enter")
        pyautogui.sleep(2)  # Wait for Notepad to open

        # Press Ctrl+N to open a new window
        pyautogui.hotkey("ctrl", "n")
        pyautogui.sleep(1)

    def create_notes(self):
        # Get today's date and time
        today_datetime = datetime.datetime.now().strftime("%A, %B %d, %Y %I:%M %p")
        # Set the note file name
        note_file = os.path.join(os.path.expanduser("~"), "Desktop", f"Todays_notes.txt")

        # Open a new Notepad file
        self.open_notepad()

        # Type the heading with today's date and time in Notepad
        heading = f"Notes for {today_datetime}:\n\n"
        pyautogui.typewrite(heading)

        # Speak instructions to start making notes
        self.speak("You can start making notes now.")

        notes_text = ""  # Variable to store notes

        while True:
            text = self.listen_command()
            doc = self.nlp(text)
            if any(word in doc.text for word in ["stop", "cancel", "finish"]):
                self.speak("Do you want to save the notes? Please say 'yes' or 'no'.")
                response = self.listen_command()
                if "yes" in response:
                    with open(note_file, "w") as f:
                        f.write(heading)  # Write heading
                        f.write(notes_text)  # Write notes
                    self.speak("Notes saved successfully.")
                elif "no" in response:
                    self.speak("Notes not saved.")
                break
            else:
                pyautogui.typewrite(text + "\n")  # Append spoken text to notes

if __name__ == "__main__":
    while True:
        notes_maker = NotesMaker()
        command = ""
        while "start making notes" not in command:
            command = notes_maker.listen_command()

        notes_maker.create_notes()
