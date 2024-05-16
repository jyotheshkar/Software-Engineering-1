# joke.py
import speech_recognition as sr
import pyttsx3
import pyjokes
import spacy

# Load English tokenizer, tagger, parser, NER, and word vectors
nlp = spacy.load("en_core_web_sm")

# Initialize the speech recognizer
recognizer = sr.Recognizer()

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Function to get a joke from pyjokes
def process_input(text):
    return pyjokes.get_joke()

# Function to analyze the user's intent and check if they want to hear a joke
def analyze_intent(text):
    doc = nlp(text)  # Process the input text with spaCy
    for token in doc:
        if token.text.lower() == "joke":
            return True  # Return True if the intent is to hear a joke
    return False  # Return False if the intent is not related to jokes

# Function to listen for a joke request using the microphone
def listen_for_joke_request():
    with sr.Microphone() as source:  # Use the microphone as the audio source
        # print("Listening for joke request...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)  # Listen for audio input

    try:
        print("Processing joke request...")
        text = recognizer.recognize_google(audio)  # Recognize speech using Google API
        print("User said:", text)
        return text  # Return the recognized text
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")
        return None  # Return None if the speech was not understood
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return None  # Return None if there was an error with the request

# Function to convert text to speech and adjust voice properties
def speak(text):
    voices = engine.getProperty('voices')  # Get available voices
    # Set voice to Microsoft Zira Desktop if available
    selected_voice_id = None
    for voice in voices:
        if "Zira" in voice.name:
            selected_voice_id = voice.id
            break
    if selected_voice_id:
        engine.setProperty('voice', selected_voice_id)
        engine.setProperty('rate', 170)  # Adjust the speech rate (words per minute)
    engine.say(text)  # Queue the text to be spoken
    engine.runAndWait()  # Wait for the speech to be completed

# Continuous listening for joke requests
while True:
    user_input = listen_for_joke_request()  # Listen for a joke request
    if user_input:
        if analyze_intent(user_input):  # Check if the user asked for a joke
            joke = process_input("random")  # Get a random joke
            speak("Here's your joke:")  # Announce the joke
            speak(joke)  # Speak the joke
        else:
            speak("I'm sorry, I didn't catch that. Can you repeat?")  # Ask the user to repeat if the intent was not understood
    else:
        continue  # Continue listening if no input was recognized
