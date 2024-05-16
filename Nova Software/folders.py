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
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)  # Listen for audio input

    try:
        command = recognizer.recognize_google(audio).lower()  # Recognize speech using Google API and convert to lowercase
        print("You said:", command)
        return command  # Return the recognized command
    except sr.UnknownValueError:
        print("Sorry, I didn't understand that.")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

# Function to speak text
def speak(text):
    engine.say(text)  # Queue the text to be spoken
    engine.runAndWait()  # Wait for the speech to be completed

# Function to create a folder on the desktop
def create_folder(folder_name):
    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')  # Get the path to the desktop
    folder_path = os.path.join(desktop_path, folder_name)  # Construct the full path for the new folder
    try:
        os.makedirs(folder_path)  # Create the folder
        speak(f"Folder '{folder_name}' created successfully on the desktop.")
    except FileExistsError:
        speak(f"Folder '{folder_name}' already exists on the desktop.")
    except Exception as e:
        speak(f"Error: {e}")

# Function to delete a folder from the desktop
def delete_folder(folder_name):
    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')  # Get the path to the desktop
    folder_path = os.path.join(desktop_path, folder_name)  # Construct the full path for the folder to be deleted
    try:
        os.rmdir(folder_path)  # Delete the folder
        speak(f"Folder '{folder_name}' deleted successfully from the desktop.")
    except FileNotFoundError:
        speak(f"Folder '{folder_name}' not found on the desktop.")
    except OSError as e:
        speak(f"Error: {e.strerror}")

# Main function
def main():
    while True:
        command = listen_for_commands()  # Listen for a command from the user

        if "create folder" in command:
            speak("What do you want to name the folder?")
            folder_name = listen_for_commands()  # Listen for the folder name
            create_folder(folder_name)  # Create the folder
        elif "delete folder" in command:
            speak("What's the name of the folder you want to delete?")
            folder_name = listen_for_commands()  # Listen for the folder name
            delete_folder(folder_name)  # Delete the folder
        elif "exit" in command:
            speak("Exiting the program.")
            break  # Exit the loop and end the program
        else:
            speak("Invalid command. Please try again.")

# Entry point of the script
if __name__ == "__main__":
    main()  # Run the main function
