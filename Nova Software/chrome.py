import pyttsx3
import speech_recognition as sr
from selenium import webdriver

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def get_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print("You said:", command)
            return command.lower()
        except sr.UnknownValueError:
            print("Could not understand audio")
            return ""
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            return ""

def search_youtube(query):
    try:
        speak("Searching YouTube for " + query)
        query = query.replace(" ", "+")
        url = f"https://www.youtube.com/results?search_query={query}"
        # Use Selenium to open Chrome and navigate to the URL
        driver = webdriver.Chrome()
        driver.get(url)
    except Exception as e:
        print("Error:", e)
        speak("Sorry, I couldn't search YouTube at the moment")
    finally:
        # Close the browser after performing the search
        driver.quit()

speak("How can I help you?")
while True:
    command = get_audio()
    if "play" in command:
        query = command.replace("play", "").strip()
        search_youtube(query)
    elif "exit" in command or "quit" in command:
        speak("Goodbye!")
        break
