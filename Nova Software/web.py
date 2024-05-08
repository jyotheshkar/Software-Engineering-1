# web.py
import tkinter as tk
import speech_recognition as sr
from bs4 import BeautifulSoup
import requests
import pyttsx3
import re

# Function to scrape text data from a webpage
def scrape_text(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the webpage using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find and extract text data from specific HTML elements
        text_data = ''
        for element in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span']):
            text_data += element.get_text() + '\n'
        
        return text_data
    else:
        return None

# Function to handle speech input
def get_speech_input():
    recognizer = sr.Recognizer()
    while True:  # Continuous listening
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            print("Recognizing...")
            query = recognizer.recognize_google(audio)
            print("You said:", query)

            # Check if query contains both "web" and "scrapping"
            if re.search(r'\bweb\b', query, re.IGNORECASE) and re.search(r'\bscrap(?:ping)?\b', query, re.IGNORECASE):
                speak("Activating web scraping environment.")
                open_gui()
                return None

        except sr.UnknownValueError:
            print("Sorry, I couldn't understand what you said.")
        except sr.RequestError:
            print("Sorry, I'm having trouble accessing the speech recognition service.")

# Function to open GUI with requested message
def open_gui():
    global text_output  # Use the global text_output variable
    root = tk.Tk()
    root.title("Web Scraping with Speech Interface")
    root.configure(bg='black')  # Set background color to black

    # Label for message
    message_label = tk.Label(root, text="Please copy paste the link here.", fg="red", bg="black")
    message_label.pack()

    # Entry for website URL
    url_entry = tk.Entry(root, width=50, fg="red", bg="black", insertbackground="red", highlightcolor="red", highlightbackground="red")
    url_entry.pack()

    # Button to trigger scraping
    scrape_button = tk.Button(root, text="Scrape", command=lambda: scrape_website(url_entry.get(), root), fg="red", bg="black", activeforeground="red", activebackground="black", highlightcolor="red", highlightbackground="red")
    scrape_button.pack()

    # Text widget to display scraped text
    text_output = tk.Text(root, height=20, width=80, wrap=tk.WORD, fg="red", bg="black")
    text_output.pack()

    root.mainloop()

# Function to handle GUI button click event
def scrape_website(url, root):
    global text_output  # Use the global text_output variable
    if url:
        scraped_text = scrape_text(url)
        if scraped_text:
            text_output.config(state='normal')
            text_output.delete(1.0, tk.END)
            text_output.insert(tk.END, scraped_text)
            text_output.config(state='disabled')
            speak("Web scraping has been successful.")
        else:
            text_output.config(state='normal')
            text_output.delete(1.0, tk.END)
            text_output.insert(tk.END, "Failed to scrape text data from the website.")
            text_output.config(state='disabled')
            speak("Failed to scrape text data from the website.")
    else:
        text_output.config(state='normal')
        text_output.delete(1.0, tk.END)
        text_output.insert(tk.END, "Please enter a website URL.")
        text_output.config(state='disabled')
        speak("Please enter a website URL.")

    root.destroy()  # Close the GUI after scraping

# Function to convert text to speech
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Call the function to start listening for speech input
get_speech_input()
