
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

def process_input(text):
    return pyjokes.get_joke()

def analyze_intent(text):
    doc = nlp(text)
    for token in doc:
        if token.text.lower() == "joke":
            return True
    return False

def listen_for_joke_request():
    with sr.Microphone() as source:
        # print("Listening for joke request...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Processing joke request...")
        text = recognizer.recognize_google(audio)
        print("User said:", text)
        return text
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")
        return None
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return None

def speak(text):
    voices = engine.getProperty('voices')
    # Set voice 2 (Microsoft Zira Desktop)
    selected_voice_id = None
    for voice in voices:
        if "Zira" in voice.name:
            selected_voice_id = voice.id
            break
    if selected_voice_id:
        engine.setProperty('voice', selected_voice_id)
        engine.setProperty('rate', 170)  # Adjust the rate (words per minute)
    engine.say(text)
    engine.runAndWait()

# Continuous listening for joke requests
while True:
    user_input = listen_for_joke_request()
    if user_input:
        if analyze_intent(user_input):
            joke = process_input("random")
            speak("Here's your joke:")
            speak(joke)
        else:
            speak("I'm sorry, I didn't catch that. Can you repeat?")
    else:
        continue


