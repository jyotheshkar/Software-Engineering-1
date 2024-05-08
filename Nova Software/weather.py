# weather.py
import time
import random
import requests
import speech_recognition as sr
import pyttsx3
import spacy

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

# Mapping of country abbreviations to full names
country_mapping = {
    "usa": "United States of America",
    # Add more mappings as needed
    "uk": "United Kingdom"
}

# List of random processing messages
processing_messages = [
    "Working on it...",
    "Processing...",
    "Just a moment...",
    "Let me check that for you...",
    "Hold on, I'm checking...",
    "Just a sec, I'm on it...",
    "I'll get that information for you...",
    "Hang tight, fetching the data...",
    "Almost there, just need a moment...",
    "One moment please, I'm checking...",
    "I'm working on it, please wait...",
    "Let me find that out for you...",
    "Checking now, hold on..."
]

# List of synonyms for weather-related words
weather_synonyms = ["climate", "temperature", "weather"]

# Weather responses
weather_responses = {
    "Clear": "Looks like a great day! Don't forget your sunglasses!",
    "Clouds": "It's a bit cloudy today. Might need a light jacket.",
    "Rain": "Better carry an umbrella, it's raining cats and dogs out there!",
    "Drizzle": "Just a little drizzle today. Don't forget your umbrella!",
    "Thunderstorm": "Thunder and lightning! Stay indoors if you can.",
    "Snow": "Get ready to build a snowman! It's snowing outside!",
    "Mist": "Be cautious, visibility might be low. Drive safe!",
    "Smoke": "Smoke in the air today. Stay indoors if possible.",
    "Haze": "Hazy weather today. Take care if you're heading out.",
    "Dust": "Dusty conditions today. Cover your face if you're outside!",
    "Fog": "Foggy weather ahead. Drive carefully!",
    "Sand": "Sandstorm warning! Stay indoors and keep windows closed.",
    "Ash": "Ashfall warning! Be cautious if you're outside.",
    "Squall": "Squally weather today. Hold onto your hats!",
    "Tornado": "Tornado warning! Seek shelter immediately!",
    "Tornado": "Tornado warning! Seek shelter immediately!",
    "Clear": "Clear skies ahead! Perfect day for a picnic!",
    "Clouds": "Cloudy weather. Don't forget your umbrella just in case!",
    "Drizzle": "A little drizzle won't dampen your spirits, right?",
    "Rain": "Rainy day ahead! Don't forget your raincoat!",
    "Thunderstorm": "Thunder and lightning! Stay indoors and cozy!",
    "Snow": "Snowy weather! Bundle up and enjoy the winter wonderland!",
    "Mist": "Misty weather! Drive safe and keep your headlights on!",
    "Smoke": "Smoky conditions! Stay indoors and keep windows closed!",
    "Haze": "Hazy day ahead! Take care if you have respiratory issues!",
    "Dust": "Dusty conditions! Wear a mask if you're heading out!",
    "Fog": "Foggy weather! Drive carefully and use low beams!",
    "Sand": "Sandstorm warning! Stay indoors and keep windows closed!",
    "Ash": "Ashfall warning! Wear a mask and protect your eyes!",
    "Squall": "Squally weather! Hold onto your hat and stay safe!",
    "Tornado": "Tornado warning! Seek shelter immediately!",
}

def expand_country_name(location_name):
    return country_mapping.get(location_name.lower(), location_name)

def get_weather(location_name, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={location_name}&appid={api_key}"

    response = requests.get(complete_url)
    data = response.json()

    if data["cod"] != "404":
        # Extracting data
        city = data["name"]
        country = data["sys"]["country"]
        weather = data["weather"][0]["main"]
        description = data["weather"][0]["description"]
        temperature_kelvin = data["main"]["temp"]
        temperature_celsius = temperature_kelvin - 273.15

        # Randomly choose a processing message
        processing_message = random.choice(processing_messages)
        
        # Speak the processing message
        engine = pyttsx3.init()
        engine.setProperty('rate', 190)  # Setting the speech rate to 150 words per minute
        engine.say(processing_message)
        engine.runAndWait()

        # Print processing message
        print(processing_message)
        time.sleep(0.5)

        # Print weather information
        print(f"\nWeather in {city}, {country}: {description.capitalize()}.")
        print(f"Temperature: {temperature_celsius:.2f}°C.\n")

        # Speak the weather information
        engine.say(f"The weather in {city}, {country} is {description.lower()}, with a temperature of {temperature_celsius:.2f} degrees Celsius.")
        engine.runAndWait()

        # Check for additional weather response
        if weather in weather_responses:
            response_message = weather_responses[weather]
            print(response_message)
            engine.say(response_message)
            engine.runAndWait()

        # Sarcastic response for temperatures below -2°C
        if temperature_celsius < -2:
            sarcastic_message = "Oh, it's absolutely chilling outside. Get the thermals and jackets on before you leave home alright buddy?"
            print(sarcastic_message)
            engine.say(sarcastic_message)
            engine.runAndWait()
    else:
        print("Location not found.")

def process_input(input_text):
    doc = nlp(input_text)

    # Check if the user is asking about the weather and extract location
    location = None
    for token in doc:
        if token.text.lower() in ["weather", "climate", "temperature"]:
            for ent in doc.ents:
                if ent.label_ == "GPE":  # GPE: Geo-Political Entity (location)
                    location = ent.text
                    break
            break
    return location

if __name__ == "__main__":
    api_key = "42240d393017774c6e0f616dfd7c677b"
    recognizer = sr.Recognizer()

    while True:
        with sr.Microphone() as source:
            
            audio = recognizer.listen(source)

        try:
            user_input = recognizer.recognize_google(audio).lower()
            if user_input == "quit":
                break
            location = process_input(user_input)
            if location:
                location = expand_country_name(location)
                get_weather(location, api_key)
            else:
                print("Sorry, I couldn't understand your query.")
        except sr.UnknownValueError:
            print("Sorry, could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
