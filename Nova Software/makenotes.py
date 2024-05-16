# makenotes.py
import os
import datetime
import speech_recognition as sr
import pyautogui
import pyttsx3
import spacy

# Class for making notes using voice commands
class NotesMaker:
    def __init__(self):
        self.recognizer = sr.Recognizer()  # Initialize the speech recognizer
        self.engine = pyttsx3.init()  # Initialize the text-to-speech engine
        self.engine.setProperty('rate', 150)  # Adjust speech rate
        self.nlp = spacy.load("en_core_web_sm")  # Load English NLP model

    # Function to listen for voice commands
    def listen_command(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)  # Adjust for ambient noise
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

    # Function to speak text
    def speak(self, text):
        voices = self.engine.getProperty('voices')  # Get available voices
        # Set voice to Microsoft Zira Desktop
        for voice in voices:
            if "Zira" in voice.name:
                self.engine.setProperty('voice', voice.id)
                break
        self.engine.say(text)  # Queue the text to be spoken
        self.engine.runAndWait()  # Wait for the speech to be completed

    # Function to open Notepad
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

    # Function to create notes
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
            text = self.listen_command()  # Listen for commands
            doc = self.nlp(text)
            if any(word in doc.text for word in ["stop", "cancel", "finish"]):
                # If user says stop, cancel, or finish, ask if they want to save the notes
                self.speak("Do you want to save the notes? Please say 'yes' or 'no'.")
                response = self.listen_command()  # Listen for response
                if "yes" in response:
                    with open(note_file, "w") as f:
                        f.write(heading)  # Write heading
                        f.write(notes_text)  # Write notes
                    self.speak("Notes saved successfully.")
                elif "no" in response:
                    self.speak("Notes not saved.")
                break  # Exit the loop
            else:
                pyautogui.typewrite(text + "\n")  # Append spoken text to notes

# Entry point of the script
if __name__ == "__main__":
    while True:
        notes_maker = NotesMaker()  # Create an instance of NotesMaker
        command = ""
        while "start making notes" not in command:
            command = notes_maker.listen_command()  # Listen for command to start making notes

        notes_maker.create_notes()  # Start creating notes
