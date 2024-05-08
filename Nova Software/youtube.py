# youtube.py
import webbrowser
import speech_recognition as sr
import pyttsx3
import spacy
import time
import pyautogui

# Load English language model in SpaCy
nlp = spacy.load("en_core_web_sm")

# Function to authenticate the user
def authenticate():
    # Your authentication code here
    authenticated = True  # Assume authenticated for now
    return authenticated

# Function to check if the query contains keywords related to listening to music
def contains_listen_music_keywords(query):
    # Process the query using SpaCy
    doc = nlp(query)
    # Check for tokens containing 'listen' or 'music'
    for token in doc:
        if token.text.lower() in ['listen', 'music']:
            return True
    return False

# Function to pause or play the video
def toggle_play_pause():
    # Press the space key to toggle play/pause
    pyautogui.press('space')

# Function to stop music and close the browser tab
def stop_music():
    # Close the browser tab
    pyautogui.hotkey('ctrl', 'w')

# Function to control the volume
def control_volume(action):
    # Simulate pressing the volume up or down key based on the action
    if action == "increase":
        pyautogui.press('volumeup')
    elif action == "decrease":
        pyautogui.press('volumedown')

# Main function
def main():
    # Authenticate the user
    authenticated = authenticate()
    if not authenticated:
        print("Authentication failed. Exiting.")
        return

    # Initialize speech recognizer
    recognizer = sr.Recognizer()

    # Initialize the microphone
    mic = sr.Microphone()

    while True:
        # Listen for the activation phrase
        with mic as source:
            print("Listening for activation phrase...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            print("Recognizing...")
            # Use the recognizer to convert speech to text
            activation_phrase = recognizer.recognize_google(audio)
            print("Activation phrase:", activation_phrase)

            # Check if the activation phrase contains keywords related to listening to music
            if contains_listen_music_keywords(activation_phrase):
                print("Activation phrase detected. Activating music search...")

                # Prompt user for song or artist
                engine = pyttsx3.init()
                engine.say("What artist or song would you like to listen to?")
                engine.runAndWait()

                # Listen for user input
                with mic as source:
                    print("Listening for song or artist...")
                    recognizer.adjust_for_ambient_noise(source)
                    audio = recognizer.listen(source)

                print("Recognizing...")
                query = recognizer.recognize_google(audio)
                print("User query:", query)

                # Construct the YouTube search URL with the user's query
                search_url = f"https://www.youtube.com/results?search_query={query}"

                # Open the search URL in the default web browser
                webbrowser.open(search_url)

                # Wait for the page to load
                time.sleep(5)

                # Click on the first video
                pyautogui.click(x=430, y=305)

                # Wait for the video to start
                time.sleep(5)

                # Listen for further commands
                while True:
                    with mic as source:
                        print("Listening for commands...")
                        recognizer.adjust_for_ambient_noise(source)
                        audio = recognizer.listen(source)

                    try:
                        print("Recognizing command...")
                        command = recognizer.recognize_google(audio)
                        print("User command:", command)

                        if "pause" in command or "play" in command:
                            toggle_play_pause()
                        elif "increase volume" in command:
                            control_volume("increase")
                        elif "decrease volume" in command:
                            control_volume("decrease")
                        elif "stop music" in command or "quit music" in command or "done" in command or "stop" in command or "quit" in command:
                            stop_music()
                            break  # Exit the loop and wait for the activation phrase again

                    except sr.UnknownValueError:
                        print("Sorry, I could not understand the command.")
                    except sr.RequestError as e:
                        print("Could not request results from Google Speech Recognition service; {0}".format(e))

            else:
                print("Activation phrase does not contain keywords related to listening to music.")

        except sr.UnknownValueError:
            print("Sorry, I could not understand the activation phrase.")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

if __name__ == "__main__":
    main()

