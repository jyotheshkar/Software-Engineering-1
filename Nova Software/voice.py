# voice.py
import pyttsx3

def print_available_voices():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    print("Available voices:")
    for idx, voice in enumerate(voices):
        print(f" - {idx + 1}: Name: {voice.name}")

def set_voice(voice_id):
    engine = pyttsx3.init()
    engine.setProperty('voice', voice_id)

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def reply(text):
    speak(text)

# Print available voices
print_available_voices()

# Set voice 2 as the selected voice
selected_voice_id = None
engine = pyttsx3.init()
voices = engine.getProperty('voices')
if len(voices) >= 2:
    selected_voice_id = voices[1].id  # Voice 2 (index 1)
    set_voice(selected_voice_id)
    print("Voice 2 selected:", voices[1].name)
else:
    print("Voice 2 is not available.")

# Test the selected voice
reply("Hello! I'm here to assist you.")
