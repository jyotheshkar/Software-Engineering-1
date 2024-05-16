# api.py
import datetime
import speech_recognition as sr
import pyttsx3
import spacy
import pyjokes
import weather
import DT

# Load English tokenizer, tagger, parser, NER, and word vectors
nlp = spacy.load("en_core_web_sm")

# Initialize the speech recognizer
recognizer = sr.Recognizer()

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Function to process input text and return a joke
def process_input(text):
    return pyjokes.get_joke()

# Function to analyze the user's intent from the input text
def analyze_intent(text):
    doc = nlp(text)
    for token in doc:
        if token.text.lower() == "joke":
            return True  # Return True if the intent is to hear a joke
    return False  # Return False if the intent is not related to jokes

# Function to get the current date
def get_current_date():
    now = datetime.datetime.now()
    return now.strftime("%m/%d/%Y")

# Function to listen for the user's request using the microphone
def listen_for_request():
    with sr.Microphone() as source:
        print("Listening for request...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)  # Listen for audio input

    try:
        print("Processing request...")
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
def speak(text, male_voice=True):
    voices = engine.getProperty('voices')  # Get available voices
    if male_voice:
        for voice in voices:
            if "David" in voice.name:  # Set male voice
                engine.setProperty('voice', voice.id)
                break
    else:
        for voice in voices:
            if "Zira" in voice.name:  # Set female voice
                engine.setProperty('voice', voice.id)
                break

    engine.setProperty('rate', 190)  # Adjust the speech rate (words per minute)
    engine.say(text)  # Queue the text to be spoken
    engine.runAndWait()  # Wait for the speech to be completed

# Main function to handle the voice assistant's operations
def main():
    while True:
        user_input = listen_for_request()  # Get the user's input
        if user_input:
            if analyze_intent(user_input):  # Check if the user asked for a joke
                joke = process_input("random")
                speak("Here's your joke:", male_voice=True)
                speak(joke, male_voice=True)
            elif any(word in user_input.lower() for word in ['weather', 'climate', 'temperature']):
                # Check if the user asked for weather information
                api_key = "42240d393017774c6e0f616dfd7c677b"  # Your API key for weather service
                recognizer = sr.Recognizer()
                try:
                    location = weather.process_input(user_input)  # Process the user's input for location
                    if location:
                        location = weather.expand_country_name(location)  # Expand country name if necessary
                        weather.get_weather(location, api_key)  # Get weather information for the location
                    else:
                        print("Sorry, I couldn't understand your query.")
                except sr.UnknownValueError:
                    print("Sorry, could not understand the audio.")
                except sr.RequestError as e:
                    print(f"Could not request results; {e}")
            elif "date" in user_input.lower():  # Check if the user asked for the date
                date = get_current_date()
                speak(f"Today's date is {date}.", male_voice=True)
            else:
                # Process the query using the DT module for date/time/location information
                response = DT.process_query(user_input)
                if response:
                    print("Response:", response)
                    speak(response, male_voice=True)
        else:
            continue  # Continue listening if no input was recognized

# Entry point of the script
if __name__ == "__main__":
    main()  # Run the main function
