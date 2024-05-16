import pyttsx3

# Function to print available voices
def print_available_voices(engine):
    voices = engine.getProperty('voices')  # Get the list of available voices
    print("Available voices:")
    for idx, voice in enumerate(voices):
        print(f" - {idx + 1}: Name: {voice.name}")  # Print the name of each voice
    return voices  # Return the list of voices

# Function to set the voice
def set_voice(engine, voice_id):
    try:
        engine.setProperty('voice', voice_id)  # Set the voice property to the selected voice
    except Exception as e:
        print(f"Error setting voice: {e}")  # Print error if setting voice fails

# Function to speak text
def speak(engine, text):
    try:
        engine.say(text)  # Queue the text to be spoken
        engine.runAndWait()  # Wait for the speech to be completed
    except Exception as e:
        print(f"Error speaking text: {e}")  # Print error if speaking text fails

# Function to reply with a given text
def reply(engine, text):
    speak(engine, text)  # Use speak function to say the text

# Main function to run the script
def main():
    engine = pyttsx3.init()  # Initialize the text-to-speech engine
    
    # Print available voices
    voices = print_available_voices(engine)

    # Set voice 2 as the selected voice
    if len(voices) >= 2:
        selected_voice_id = voices[1].id  # Voice 2 (index 1)
        set_voice(engine, selected_voice_id)  # Set the selected voice
        print("Voice 2 selected:", voices[1].name)  # Print the name of the selected voice
    else:
        print("Voice 2 is not available.")  # Print message if voice 2 is not available

    # Test the selected voice
    reply(engine, "Hello! I'm here to assist you.")  # Speak a test message

# Entry point of the script
if __name__ == "__main__":
    main()  # Run the main function
