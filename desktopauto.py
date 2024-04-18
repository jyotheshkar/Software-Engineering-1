# import random
# import speech_recognition as sr
# import pyautogui
# import time
# import spacy
# import pyttsx3
# import ctypes
# import pygetwindow as gw
# import webbrowser

# # Load the English NLP model
# nlp = spacy.load("en_core_web_sm")

# # Initialize the Text-to-Speech engine
# engine = pyttsx3.init()

# # Possible phrases for starting the process
# start_phrases = ["Processing...", "On it...", "Just a second...", "Opening it up..."]

# def speak(text):
#     engine.say(text)
#     engine.runAndWait()

# def listen():
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Listening...")
#         recognizer.adjust_for_ambient_noise(source)
#         audio = recognizer.listen(source)
    
#     try:
#         print("Recognizing...")
#         command = recognizer.recognize_google(audio)
#         print("You said:", command)
#         return command.lower()
#     except sr.UnknownValueError:
#         print("Sorry, I didn't understand that.")
#         return ""
#     except sr.RequestError as e:
#         print("Could not request results; {0}".format(e))
#         return ""

# def open_application(app_name):
#     speak(random.choice(start_phrases))
#     if app_name is None:
#         speak("Application name not recognized.")
#         return
#     # Simulate pressing the Windows key to open the Start menu
#     pyautogui.press('win')
#     time.sleep(1)  # Wait for the Start menu to open
#     # Search for the application
#     pyautogui.write(app_name)
#     time.sleep(1)  # Wait for search results to appear
#     # Press Enter to open the first search result
#     pyautogui.press('enter')
#     time.sleep(2)  # Wait for the application to open
    
#     # Get the handle of the active window
#     hwnd = ctypes.windll.user32.GetForegroundWindow()
#     # Set the window to fullscreen mode
#     ctypes.windll.user32.ShowWindow(hwnd, 3)  # 3 represents SW_MAXIMIZE
    
#     speak(f"{app_name} opened in fullscreen mode.")

# def open_webpage(url):
#     speak(random.choice(start_phrases))
#     webbrowser.open(url)
#     speak(f"Opening {url}")

# def google_search(query):
#     search_url = f"https://www.google.com/search?q={query}"
#     open_webpage(search_url)

# def process_command(command):
#     doc = nlp(command)
#     # Extract verb and object from the command
#     verb = None
#     obj = None
#     for token in doc:
#         if token.pos_ == "VERB" or token.pos_ == "AUX":
#             verb = token.lemma_  # Use lemma for verbs (e.g., "watch" instead of "watching")
#         if token.pos_ == "NOUN":
#             if obj is None:
#                 obj = token.text
#             else:
#                 obj += " " + token.text  # Handle multi-word object
#     return verb, obj


# def close_application(app_name):
#     if app_name is None:
#         speak("Application name not recognized.")
#         return

#     # Use pyautogui to locate the window title
#     window = pyautogui.getWindowsWithTitle(app_name)

#     if window:
#         # Close the window
#         window[0].close()
#         print(f"The {app_name} application has been closed.")
#         speak(f"The {app_name} application has been closed.")
#     else:
#         # If the window with the specified title is not found
#         print(f"No {app_name} application found.")
#         speak(f"No {app_name} application found.")

#     return  # Return after closing the application

# def scroll_up():
#     pyautogui.scroll(900)  # Scroll up by 900 pixels
#     speak("Scrolled up.")

# def scroll_down():
#     pyautogui.scroll(-900)  # Scroll down by 900 pixels
#     speak("Scrolled down.")

# if __name__ == "__main__":
#     while True:
#         command = listen()
#         verb, obj = process_command(command)
#         if verb == "open":
#             if obj.startswith("http://") or obj.startswith("https://"):
#                 open_webpage(obj)
#             else:
#                 open_application(obj)
#         elif verb == "exit" or verb == "close":
#             close_application(obj)
#         elif "scroll up" in command or "scroll it up" in command:
#             scroll_up()
#         elif "scroll down" in command or "scroll it down" in command:
#             scroll_down()
#         elif "google search" in command:
#             search_query = command.replace("google search", "").strip()
#             google_search(search_query)
