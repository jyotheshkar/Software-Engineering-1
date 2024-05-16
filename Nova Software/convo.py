# convo.py
import random
import wikipedia
import speech_recognition as sr
import pyttsx3

# Function to get a summary from Wikipedia for a given topic
def get_wikipedia_info(topic):
    try:
        # Fetch information from Wikipedia
        summary = wikipedia.summary(topic, sentences=2)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        # Handle cases where the search term is ambiguous
        return "Ambiguous search term. Please be more specific."
    except wikipedia.exceptions.PageError as e:
        # Handle cases where the page is not found
        return "Page not found. Please try a different search term."

# Function to get a random response from a predefined list
def get_random_response():
    responses = [
        "Activating ultra search mode! What topic would you like information about?",
        "Activating ultra search mode! Let's dive deep! What topic are you interested in?",
        "Activating ultra search mode! Get ready for a deep dive into knowledge! What topic do you want to learn about?",
        "Activating ultra search mode! Ready to explore! What topic are you curious about?",
        "Activating ultra search mode! Let's find some hidden gems! What topic are we exploring?"
    ]
    return random.choice(responses)

# Function to convert text to speech
def speak(text):
    engine = pyttsx3.init()  # Initialize the text-to-speech engine
    voices = engine.getProperty('voices')  # Get available voices
    selected_voice_id = None
    # Set voice to Microsoft Zira Desktop if available
    for voice in voices:
        if "Zira" in voice.name:
            selected_voice_id = voice.id
            break
    if selected_voice_id:
        engine.setProperty('voice', selected_voice_id)
        engine.setProperty('rate', 180)  # Adjust the speech rate (words per minute)
    engine.say(text)  # Queue the text to be spoken
    engine.runAndWait()  # Wait for the speech to be completed

# Function to listen for audio input and recognize speech
def listen():
    recognizer = sr.Recognizer()  # Initialize the speech recognizer
    with sr.Microphone() as source:  # Use the microphone as the audio source
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        print("Listening...")
        audio = recognizer.listen(source)  # Listen for audio input

    try:
        query = recognizer.recognize_google(audio)  # Use Google Speech Recognition to convert audio to text
        print("You said:", query)
        return query.lower()  # Return the recognized text in lowercase
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")
        return ""  # Return an empty string if the speech was not understood
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return ""  # Return an empty string if there was an error with the request

# Main function to handle the conversation
def main():
    while True:
        query = listen()  # Listen for the user's input
        if "information" in query or "details" in query:
            # If the user asks for information or details
            speak(get_random_response())  # Speak a random response
            topic = listen()  # Listen for the topic
            if topic:
                if topic == 'quit':  # If the user wants to quit
                    speak("Exiting...")
                    break
                else:
                    # Get and speak the Wikipedia summary for the topic
                    summary = get_wikipedia_info(topic)
                    speak("Summary: " + summary)
        else:
            print("Sorry, I didn't catch that. Please say 'information' or 'details' to activate.")

# Entry point of the script
if __name__ == "__main__":
    main()  # Run the main function
