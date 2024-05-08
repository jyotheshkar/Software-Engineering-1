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


def process_input(text):
    return pyjokes.get_joke()


def analyze_intent(text):
    doc = nlp(text)
    for token in doc:
        if token.text.lower() == "joke":
            return True
    return False


def get_current_date():
    now = datetime.datetime.now()
    return now.strftime("%m/%d/%Y")


def listen_for_request():
    with sr.Microphone() as source:
        print("Listening for request...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Processing request...")
        text = recognizer.recognize_google(audio)
        print("User said:", text)
        return text
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")
        return None
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return None


def speak(text, male_voice=True):
    voices = engine.getProperty('voices')
    if male_voice:
        for voice in voices:
            if "David" in voice.name:
                engine.setProperty('voice', voice.id)
                break
    else:
        for voice in voices:
            if "Zira" in voice.name:
                engine.setProperty('voice', voice.id)
                break

    engine.setProperty('rate', 190)  # Adjust the rate (words per minute)
    engine.say(text)
    engine.runAndWait()


def main():
    while True:
        user_input = listen_for_request()
        if user_input:
            if analyze_intent(user_input):
                joke = process_input("random")
                speak("Here's your joke:", male_voice=True)
                speak(joke, male_voice=True)
            elif any(word in user_input.lower() for word in ['weather', 'climate', 'temperature']):
                api_key = "42240d393017774c6e0f616dfd7c677b"
                recognizer = sr.Recognizer()
                try:
                    location = weather.process_input(user_input)
                    if location:
                        location = weather.expand_country_name(location)
                        weather.get_weather(location, api_key)
                    else:
                        print("Sorry, I couldn't understand your query.")
                except sr.UnknownValueError:
                    print("Sorry, could not understand the audio.")
                except sr.RequestError as e:
                    print(f"Could not request results; {e}")
            elif "date" in user_input.lower():
                date = get_current_date()
                speak(f"Today's date is {date}.", male_voice=True)
            else:
                response = DT.process_query(user_input)
                if response:
                    print("Response:", response)
                    speak(response, male_voice=True)
        else:
            continue


if __name__ == "__main__":
    main()
