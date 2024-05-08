
# convo.py
import random
import wikipedia
import speech_recognition as sr
import pyttsx3

def get_wikipedia_info(topic):
    try:
        # Fetch information from Wikipedia
        summary = wikipedia.summary(topic, sentences=2)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return "Ambiguous search term. Please be more specific."
    except wikipedia.exceptions.PageError as e:
        return "Page not found. Please try a different search term."

def get_random_response():
    responses = [
        "Activating ultra search mode! What topic would you like information about?",
        "Activating ultra search mode! Let's dive deep! What topic are you interested in?",
        "Activating ultra search mode! Get ready for a deep dive into knowledge! What topic do you want to learn about?",
        "Activating ultra search mode! Ready to explore! What topic are you curious about?",
        "Activating ultra search mode! Let's find some hidden gems! What topic are we exploring?"
    ]
    return random.choice(responses)

def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    # Set voice 2 (Microsoft Zira Desktop)
    selected_voice_id = None
    for voice in voices:
        if "Zira" in voice.name:
            selected_voice_id = voice.id
            break
    if selected_voice_id:
        engine.setProperty('voice', selected_voice_id)
        engine.setProperty('rate', 180)  # Adjust the rate (words per minute)
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        query = recognizer.recognize_google(audio)
        print("You said:", query)
        return query.lower()
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")
        return ""
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return ""

def main():
    
    while True:
        query = listen()
        if "information" in query or "details" in query:
            speak(get_random_response())
            topic = listen()
            if topic:
                if topic == 'quit':
                    speak("Exiting...")
                    break
                else:
                    summary = get_wikipedia_info(topic)
                    speak("Summary: " + summary)
        else:
            print("Sorry, I didn't catch that. Please say 'information' or 'details' to activate.")

if __name__ == "__main__":
    main()
