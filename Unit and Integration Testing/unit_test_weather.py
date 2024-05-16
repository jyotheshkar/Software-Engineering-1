import unittest
from unittest.mock import patch, MagicMock
import weather  # Ensure this matches the actual name of your script file

class TestWeatherModule(unittest.TestCase):

    @patch('pyttsx3.init')
    def test_expand_country_name(self, mock_init):
        """
        Test the expand_country_name function to ensure it correctly expands country abbreviations.
        """
        self.assertEqual(weather.expand_country_name("usa"), "United States of America")
        self.assertEqual(weather.expand_country_name("uk"), "United Kingdom")
        self.assertEqual(weather.expand_country_name("canada"), "canada")  # No expansion needed

    @patch('requests.get')
    @patch('pyttsx3.init')
    @patch('time.sleep')
    def test_get_weather(self, mock_sleep, mock_init, mock_get):
        """
        Test the get_weather function to ensure it retrieves and displays weather information correctly.
        """
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "cod": 200,
            "name": "London",
            "sys": {"country": "GB"},
            "weather": [{"main": "Clear", "description": "clear sky"}],
            "main": {"temp": 280.32}
        }
        mock_get.return_value = mock_response
        mock_engine = MagicMock()
        mock_init.return_value = mock_engine

        weather.get_weather("London", "dummy_api_key")
        
        # Check if the correct URL was used to make the API call
        mock_get.assert_called_with("http://api.openweathermap.org/data/2.5/weather?q=London&appid=dummy_api_key")
        
        # Check if the TTS engine was initialized
        mock_init.assert_called_once()
        
        # Check if the processing message and weather information were spoken
        mock_engine.say.assert_any_call("Processing...")
        mock_engine.say.assert_any_call("The weather in London, GB is clear sky, with a temperature of 7.17 degrees Celsius.")
        mock_engine.runAndWait.assert_called()

    @patch('spacy.load')
    def test_process_input(self, mock_spacy_load):
        """
        Test the process_input function to ensure it correctly processes input text and extracts location.
        """
        mock_nlp = MagicMock()
        mock_doc = MagicMock()
        mock_spacy_load.return_value = mock_nlp
        mock_nlp.return_value = mock_doc
        
        # Mock the input text and entities
        mock_doc.ents = [MagicMock(label_='GPE', text='London')]
        mock_doc.__iter__.return_value = [
            MagicMock(text='What', text_with_ws='What '),
            MagicMock(text='is', text_with_ws='is '),
            MagicMock(text='the', text_with_ws='the '),
            MagicMock(text='weather', text_with_ws='weather '),
            MagicMock(text='in', text_with_ws='in '),
            MagicMock(text='London', text_with_ws='London?')
        ]

        location = weather.process_input("What is the weather in London?")
        
        # Check if the location was extracted correctly
        self.assertEqual(location, "London")

if __name__ == '__main__':
    unittest.main()
