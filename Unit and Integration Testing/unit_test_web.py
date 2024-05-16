import unittest
from unittest.mock import patch, MagicMock
import web  # Ensure this matches the actual name of your script file

class TestWebModule(unittest.TestCase):

    @patch('web.requests.get')
    def test_scrape_text(self, mock_get):
        """
        Test the scrape_text function to ensure it scrapes text data from a webpage.
        """
        # Mock the GET request response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """
            <html>
                <body>
                    <h1>Header 1</h1>
                    <p>Paragraph 1</p>
                    <h2>Header 2</h2>
                    <span>Span text</span>
                </body>
            </html>
        """
        mock_get.return_value = mock_response

        # Expected text data
        expected_text = "Header 1\nParagraph 1\nHeader 2\nSpan text\n"

        # Call the function and assert the results
        result = web.scrape_text("http://example.com")
        self.assertEqual(result, expected_text)

        # Check if the GET request was made with the correct URL
        mock_get.assert_called_with("http://example.com")

    @patch('web.sr.Recognizer.listen')
    @patch('web.sr.Recognizer.adjust_for_ambient_noise')
    @patch('web.sr.Microphone')
    @patch('web.sr.Recognizer.recognize_google', return_value="web scraping")
    @patch('web.speak')
    @patch('web.open_gui')
    def test_get_speech_input(self, mock_open_gui, mock_speak, mock_recognize_google, mock_microphone, mock_adjust_noise, mock_listen):
        """
        Test the get_speech_input function to ensure it activates the web scraping environment on command.
        """
        # Mock recognizer instance and audio input
        mock_recognizer_instance = MagicMock()
        mock_listen.return_value = MagicMock()

        with patch('web.sr.Recognizer', return_value=mock_recognizer_instance):
            web.get_speech_input()

        # Assert that the speak function was called
        mock_speak.assert_called_with("Activating web scraping environment.")
        # Assert that the open_gui function was called
        mock_open_gui.assert_called_once()

    @patch('web.tk.Tk')
    def test_open_gui(self, mock_tk):
        """
        Test the open_gui function to ensure it sets up the GUI correctly.
        """
        mock_root = MagicMock()
        mock_tk.return_value = mock_root

        web.open_gui()

        # Check if the Tkinter main loop was started
        mock_root.mainloop.assert_called_once()

    @patch('web.scrape_text', return_value="Scraped text data.")
    @patch('web.speak')
    @patch('web.tk.Text')
    def test_scrape_website(self, mock_text, mock_speak, mock_scrape_text):
        """
        Test the scrape_website function to ensure it handles the GUI button click event correctly.
        """
        mock_text_instance = MagicMock()
        mock_text.return_value = mock_text_instance
        mock_root = MagicMock()

        web.text_output = mock_text_instance
        web.scrape_website("http://example.com", mock_root)

        # Check if the text widget was updated with scraped text
        mock_text_instance.config.assert_any_call(state='normal')
        mock_text_instance.delete.assert_called_with(1.0, web.tk.END)
        mock_text_instance.insert.assert_called_with(web.tk.END, "Scraped text data.")
        mock_text_instance.config.assert_any_call(state='disabled')
        
        # Check if the speak function was called with the success message
        mock_speak.assert_called_with("Web scraping has been successful.")
        
        # Check if the root window was destroyed
        mock_root.destroy.assert_called_once()

    @patch('pyttsx3.init')
    def test_speak(self, mock_init):
        """
        Test the speak function to ensure it converts text to speech.
        """
        mock_engine = MagicMock()
        mock_init.return_value = mock_engine

        web.speak("Hello, world!")
        
        # Check if the TTS engine said the correct text
        mock_engine.say.assert_called_with("Hello, world!")
        # Check if the TTS engine ran and waited
        mock_engine.runAndWait.assert_called_once()

if __name__ == '__main__':
    unittest.main()
