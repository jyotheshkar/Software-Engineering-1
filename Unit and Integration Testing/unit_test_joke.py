import unittest
from unittest.mock import patch, MagicMock
import joke  # Ensure this matches the actual name of your script file

class TestJokeModule(unittest.TestCase):

    @patch('pyttsx3.init')
    def test_speak(self, mock_init):
        """
        Test the speak function to ensure it initializes the TTS engine and speaks the given text.
        """
        mock_engine = MagicMock()
        mock_init.return_value = mock_engine

        joke.speak("Hello, world!")
        
        # Check if the TTS engine was initialized
        mock_init.assert_called_once()
        # Check if the engine properties were set correctly
        mock_engine.setProperty.assert_any_call('voice', mock_engine.getProperty.return_value[1].id)
        mock_engine.setProperty.assert_any_call('rate', 170)
        # Check if the engine said the correct text
        mock_engine.say.assert_called_with("Hello, world!")
        # Check if the engine ran and waited
        mock_engine.runAndWait.assert_called_once()

    @patch('joke.sr.Microphone')
    @patch('joke.sr.Recognizer')
    def test_listen_for_joke_request(self, mock_recognizer, mock_microphone):
        """
        Test the listen_for_joke_request function to ensure it listens for requests and returns the recognized text.
        """
        mock_recognizer_instance = MagicMock()
        mock_recognizer.return_value = mock_recognizer_instance
        mock_recognizer_instance.recognize_google.return_value = "tell me a joke"

        result = joke.listen_for_joke_request()
        
        # Check if the recognized text is returned correctly
        self.assertEqual(result, "tell me a joke")

    @patch('pyjokes.get_joke', return_value="Why don't scientists trust atoms? Because they make up everything.")
    def test_process_input(self, mock_get_joke):
        """
        Test the process_input function to ensure it returns a joke.
        """
        result = joke.process_input("random")
        
        # Check if the correct joke is returned
        self.assertEqual(result, "Why don't scientists trust atoms? Because they make up everything.")
        # Check if the pyjokes.get_joke function was called
        mock_get_joke.assert_called_once_with()

    @patch('spacy.load')
    def test_analyze_intent(self, mock_spacy_load):
        """
        Test the analyze_intent function to ensure it correctly identifies the intent to tell a joke.
        """
        mock_nlp = MagicMock()
        mock_doc = MagicMock()
        mock_spacy_load.return_value = mock_nlp
        mock_nlp.return_value = mock_doc
        mock_doc.__iter__.return_value = [MagicMock(text='joke', text_with_ws='joke')]

        result = joke.analyze_intent("Tell me a joke.")
        
        # Check if the intent to tell a joke is correctly identified
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
