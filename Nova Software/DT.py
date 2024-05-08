
# DT.py
import speech_recognition as sr
import pyttsx3
import spacy
import requests
from datetime import datetime

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def get_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        said = ""
        try:
            said = recognizer.recognize_google(audio)
        except Exception as e:
            print("Exception:", str(e))
    return said

def get_time_for_location(location):
    api_key = '42240d393017774c6e0f616dfd7c677b'  # Replace 'YOUR_API_KEY' with your actual API key
    base_url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}'
    
    try:
        response = requests.get(base_url)
        data = response.json()
        
        if response.status_code == 200:
            timezone_offset = data['timezone']
            current_time = datetime.utcfromtimestamp(data['dt'] + timezone_offset).strftime('%I:%M %p')
            return current_time
        else:
            print("Failed to fetch time for", location)
            return None
    except Exception as ex:
        print("Exception:", str(ex))
        return None

def process_query(query):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(query)
    location = None
    
    for ent in doc.ents:
        if ent.label_ == 'GPE':
            location = ent.text
            break
    
    for token in doc:
        if token.text.lower() == 'date':
            if location:
                return datetime.now().strftime('%A, %d/%m/%Y') + " in " + location
            else:
                return datetime.now().strftime('%A, %d/%m/%Y')
        elif token.text.lower() == 'time':
            if location:
                return get_time_for_location(location)
            else:
                return datetime.now().strftime('%I:%M %p')  # Default to UK time
    
    if location:
        return get_time_for_location(location)
    
    return None

if __name__ == "__main__":
   
    
    while True:
        
        query = get_audio().lower()
        print("You said:", query)
        
        if "quit" in query:
            speak("Goodbye!")
            print("Exiting...")
            break
        
        response = process_query(query)
        if response:
            print("Response:", response)
            speak(response)
        
