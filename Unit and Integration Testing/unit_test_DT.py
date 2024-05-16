import unittest
from unittest.mock import patch, MagicMock
import DT  
from datetime import datetime

class TestDTModule(unittest.TestCase):

    @patch('pyttsx3.init')
    def test_speak(self, mock_init):
        """
        Test the speak function to ensure it initializes the TTS engine and speaks the given text.
        """
        mock_engine = MagicMock()
        mock_init.return_value = mock_engine

        DT.speak("Hello, world!")
        
        # Check if the TTS engine was initialized
        mock_init.assert_called_once()
        # Check if the engine said the correct text
        mock_engine.say.assert_called_with("Hello, world!")
        # Check if the engine ran and waited
        mock_engine.runAndWait.assert_called_once()

    @patch('DT.sr.Microphone')
    @patch('DT.sr.Recognizer')
    def test_get_audio(self, mock_recognizer, mock_microphone):
        """
        Test the get_audio function to ensure it listens for audio and returns the recognized text.
        """
        mock_recognizer_instance = MagicMock()
        mock_recognizer.return_value = mock_recognizer_instance
        mock_recognizer_instance.recognize_google.return_value = "test audio"

        result = DT.get_audio()
        
        # Check if the recognized audio is returned correctly
        self.assertEqual(result, "test audio")

    @patch('requests.get')
    def test_get_time_for_location(self, mock_get):
        """
        Test the get_time_for_location function to ensure it fetches and returns the correct time for a given location.
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'timezone': 3600,
            'dt': 1609459200  # January 1, 2021 00:00:00 UTC
        }
        mock_get.return_value = mock_response

        result = DT.get_time_for_location("London")
        
        # Check if the time returned is correct
        self.assertEqual(result, "01:00 AM")
        
        # Check if the requests.get was called with the correct URL
        mock_get.assert_called_with('http://api.openweathermap.org/data/2.5/weather?q=London&appid=42240d393017774c6e0f616dfd7c677b')

    @patch('DT.get_time_for_location')
    @patch('spacy.load')
    def test_process_query(self, mock_spacy_load, mock_get_time_for_location):
        """
        Test the process_query function to ensure it processes the query and returns the correct response.
        """
        mock_nlp = MagicMock()
        mock_doc = MagicMock()
        mock_spacy_load.return_value = mock_nlp
        mock_nlp.return_value = mock_doc
        
        # Test date query without location
        mock_doc.ents = []
        mock_doc.__iter__.return_value = [MagicMock(text='date', text_with_ws='date')]
        result = DT.process_query("What is the date today?")
        self.assertEqual(result, datetime.now().strftime('%A, %d/%m/%Y'))

        # Test time query with location
        mock_doc.ents = [MagicMock(label_='GPE', text='London')]
        mock_doc.__iter__.return_value = [MagicMock(text='time', text_with_ws='time')]
        mock_get_time_for_location.return_value = "01:00 AM"
        result = DT.process_query("What is the time in London?")
        self.assertEqual(result, "01:00 AM")
        mock_get_time_for_location.assert_called_with("London")

        # Test general query with location
        mock_doc.ents = [MagicMock(label_='GPE', text='New York')]
        mock_doc.__iter__.return_value = [MagicMock(text='time', text_with_ws='time')]
        mock_get_time_for_location.return_value = "08:00 PM"
        result = DT.process_query("What time is it in New York?")
        self.assertEqual(result, "08:00 PM")
        mock_get_time_for_location.assert_called_with("New York")

if __name__ == '__main__':
    unittest.main()
