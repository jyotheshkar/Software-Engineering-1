# DT.py
import speech_recognition as sr
import pyttsx3
import spacy
import requests
from datetime import datetime

# Function to convert text to speech
def speak(text):
    engine = pyttsx3.init()  # Initialize the text-to-speech engine
    engine.say(text)  # Queue the text to be spoken
    engine.runAndWait()  # Wait for the speech to be completed

# Function to capture audio input and recognize speech
def get_audio():
    recognizer = sr.Recognizer()  # Initialize the speech recognizer
    with sr.Microphone() as source:  # Use the microphone as the audio source
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)  # Listen for audio input
        said = ""  # Initialize the variable to store recognized text
        try:
            said = recognizer.recognize_google(audio)  # Use Google Speech Recognition to convert audio to text
        except Exception as e:
            print("Exception:", str(e))  # Print any recognition errors
    return said  # Return the recognized text

# Function to get the current time for a given location using OpenWeatherMap API
def get_time_for_location(location):
    api_key = '42240d393017774c6e0f616dfd7c677b'  # Your API key for OpenWeatherMap
    base_url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}'
    
    try:
        response = requests.get(base_url)  # Make a request to the API
        data = response.json()  # Parse the response JSON
        
        if response.status_code == 200:
            timezone_offset = data['timezone']  # Get the timezone offset for the location
            current_time = datetime.utcfromtimestamp(data['dt'] + timezone_offset).strftime('%I:%M %p')
            return current_time  # Return the formatted current time
        else:
            print("Failed to fetch time for", location)
            return None
    except Exception as ex:
        print("Exception:", str(ex))
        return None

# Function to process the user's query and determine the appropriate response
def process_query(query):
    nlp = spacy.load('en_core_web_sm')  # Load the small English NLP model from spaCy
    doc = nlp(query)  # Process the query with spaCy
    location = None  # Initialize the location variable
    
    # Extract location entity from the query
    for ent in doc.ents:
        if ent.label_ == 'GPE':  # GPE (Geopolitical Entity) corresponds to locations like cities, countries, etc.
            location = ent.text
            break
    
    # Determine the response based on the query content
    for token in doc:
        if token.text.lower() == 'date':  # If the query asks for the date
            if location:
                return datetime.now().strftime('%A, %d/%m/%Y') + " in " + location
            else:
                return datetime.now().strftime('%A, %d/%m/%Y')
        elif token.text.lower() == 'time':  # If the query asks for the time
            if location:
                return get_time_for_location(location)
            else:
                return datetime.now().strftime('%I:%M %p')  # Default to current local time
    
    # If only location is mentioned, return the current time for that location
    if location:
        return get_time_for_location(location)
    
    return None  # Return None if the query doesn't match any criteria

# Main function to run the voice assistant
if __name__ == "__main__":
    while True:
        query = get_audio().lower()  # Get the audio input from the user and convert to lowercase
        print("You said:", query)
        
        if "quit" in query:  # If the user says "quit", exit the program
            speak("Goodbye!")
            print("Exiting...")
            break
        
        response = process_query(query)  # Process the user's query
        if response:
            print("Response:", response)
            speak(response)  # Speak the response to the user
