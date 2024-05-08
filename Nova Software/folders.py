# folders.py
import os
import speech_recognition as sr
import pyttsx3

# Initialize the speech recognizer
recognizer = sr.Recognizer()

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Function to listen to voice commands
def listen_for_commands():
    with sr.Microphone() as source:
        print("Listening for commands...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower()
        print("You said:", command)
        return command
    except sr.UnknownValueError:
        print("Sorry, I didn't understand that.")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to create a folder on the desktop
def create_folder(folder_name):
    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    folder_path = os.path.join(desktop_path, folder_name)
    try:
        os.makedirs(folder_path)
        speak(f"Folder '{folder_name}' created successfully on the desktop.")
    except FileExistsError:
        speak(f"Folder '{folder_name}' already exists on the desktop.")
    except Exception as e:
        speak(f"Error: {e}")

# Function to delete a folder from the desktop
def delete_folder(folder_name):
    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    folder_path = os.path.join(desktop_path, folder_name)
    try:
        os.rmdir(folder_path)
        speak(f"Folder '{folder_name}' deleted successfully from the desktop.")
    except FileNotFoundError:
        speak(f"Folder '{folder_name}' not found on the desktop.")
    except OSError as e:
        speak(f"Error: {e.strerror}")

# Main function
def main():
    while True:
        command = listen_for_commands()

        if "create folder" in command:
            speak("What do you want to name the folder?")
            folder_name = listen_for_commands()
            create_folder(folder_name)
        elif "delete folder" in command:
            speak("What's the name of the folder you want to delete?")
            folder_name = listen_for_commands()
            delete_folder(folder_name)
        elif "exit" in command:
            speak("Exiting the program.")
            break
        else:
            speak("Invalid command. Please try again.")

if __name__ == "__main__":
    main()
