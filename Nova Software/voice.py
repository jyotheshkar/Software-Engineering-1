import pyttsx3

def print_available_voices(engine):
    voices = engine.getProperty('voices')
    print("Available voices:")
    for idx, voice in enumerate(voices):
        print(f" - {idx + 1}: Name: {voice.name}")
    return voices

def set_voice(engine, voice_id):
    try:
        engine.setProperty('voice', voice_id)
    except Exception as e:
        print(f"Error setting voice: {e}")

def speak(engine, text):
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error speaking text: {e}")

def reply(engine, text):
    speak(engine, text)

def main():
    engine = pyttsx3.init()
    
    # Print available voices
    voices = print_available_voices(engine)

    # Set voice 2 as the selected voice
    if len(voices) >= 2:
        selected_voice_id = voices[1].id  # Voice 2 (index 1)
        set_voice(engine, selected_voice_id)
        print("Voice 2 selected:", voices[1].name)
    else:
        print("Voice 2 is not available.")

    # Test the selected voice
    reply(engine, "Hello! I'm here to assist you.")

if __name__ == "__main__":
    main()
