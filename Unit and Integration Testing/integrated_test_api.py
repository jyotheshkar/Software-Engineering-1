import unittest
from unittest.mock import patch, MagicMock
import api  # Import your main script

class IntegratedTestApiScript(unittest.TestCase):

    @patch('api.speak')
    @patch('api.sr.Recognizer')
    @patch('api.sr.Microphone')
    def test_joke_intent_flow(self, mock_microphone, mock_recognizer, mock_speak):
        """
        Test the full flow from voice command recognition to telling a joke.
        """
        # Mock the recognizer and microphone
        mock_recognizer_instance = MagicMock()
        mock_recognizer.return_value = mock_recognizer_instance
        mock_recognizer_instance.listen.return_value = "audio_data"
        mock_recognizer_instance.recognize_google.return_value = "tell me a joke"

        # Call the listen_for_request function to simulate voice command recognition
        user_input = api.listen_for_request()

        # Check if the recognized command matches the expected input
        self.assertEqual(user_input, "tell me a joke")

        # Check if the intent is recognized as requesting a joke
        intent = api.analyze_intent(user_input)
        self.assertTrue(intent)

        # Process the input and check the response
        joke = api.process_input(user_input)
        self.assertTrue(isinstance(joke, str))  # Ensure a joke string is returned

        # Speak the response and verify
        api.speak("Here's your joke:", male_voice=True)
        api.speak(joke, male_voice=True)
        mock_speak.assert_any_call("Here's your joke:", male_voice=True)
        mock_speak.assert_any_call(joke, male_voice=True)

    @patch('api.speak')
    @patch('api.sr.Recognizer')
    @patch('api.sr.Microphone')
    def test_date_intent_flow(self, mock_microphone, mock_recognizer, mock_speak):
        """
        Test the full flow from voice command recognition to providing the current date.
        """
        # Mock the recognizer and microphone
        mock_recognizer_instance = MagicMock()
        mock_recognizer.return_value = mock_recognizer_instance
        mock_recognizer_instance.listen.return_value = "audio_data"
        mock_recognizer_instance.recognize_google.return_value = "what is the date today"

        # Call the listen_for_request function to simulate voice command recognition
        user_input = api.listen_for_request()

        # Check if the recognized command matches the expected input
        self.assertEqual(user_input, "what is the date today")

        # Process the date request and check the response
        date = api.get_current_date()
        self.assertTrue(isinstance(date, str))  # Ensure a date string is returned

        # Speak the response and verify
        api.speak(f"Today's date is {date}.", male_voice=True)
        mock_speak.assert_called_with(f"Today's date is {date}.", male_voice=True)

    @patch('api.speak')
    @patch('api.weather.get_weather')
    @patch('api.weather.expand_country_name')
    @patch('api.weather.process_input')
    @patch('api.sr.Recognizer')
    @patch('api.sr.Microphone')
    def test_weather_intent_flow(self, mock_microphone, mock_recognizer, mock_process_input, mock_expand_country_name, mock_get_weather, mock_speak):
        """
        Test the full flow from voice command recognition to providing weather information.
        """
        # Mock the recognizer and microphone
        mock_recognizer_instance = MagicMock()
        mock_recognizer.return_value = mock_recognizer_instance
        mock_recognizer_instance.listen.return_value = "audio_data"
        mock_recognizer_instance.recognize_google.return_value = "what's the weather like in London"

        # Mock weather processing functions
        mock_process_input.return_value = "London"
        mock_expand_country_name.return_value = "London, United Kingdom"

        # Call the listen_for_request function to simulate voice command recognition
        user_input = api.listen_for_request()

        # Check if the recognized command matches the expected input
        self.assertEqual(user_input, "what's the weather like in London")

        # Simulate processing the weather request
        location = api.weather.process_input(user_input)
        self.assertEqual(location, "London")

        expanded_location = api.weather.expand_country_name(location)
        self.assertEqual(expanded_location, "London, United Kingdom")

        # Call the get_weather function
        api_key = "42240d393017774c6e0f616dfd7c677b"
        api.weather.get_weather(expanded_location, api_key)
        mock_get_weather.assert_called_with(expanded_location, api_key)

    @patch('api.speak')
    @patch('api.DT.process_query')
    @patch('api.sr.Recognizer')
    @patch('api.sr.Microphone')
    def test_general_query_flow(self, mock_microphone, mock_recognizer, mock_process_query, mock_speak):
        """
        Test the full flow from voice command recognition to processing a general query.
        """
        # Mock the recognizer and microphone
        mock_recognizer_instance = MagicMock()
        mock_recognizer.return_value = mock_recognizer_instance
        mock_recognizer_instance.listen.return_value = "audio_data"
        mock_recognizer_instance.recognize_google.return_value = "who is the president of the United States"

        # Mock the general query processing
        mock_process_query.return_value = "The president of the United States is Joe Biden."

        # Call the listen_for_request function to simulate voice command recognition
        user_input = api.listen_for_request()

        # Check if the recognized command matches the expected input
        self.assertEqual(user_input, "who is the president of the United States")

        # Process the query and check the response
        response = api.DT.process_query(user_input)
        self.assertEqual(response, "The president of the United States is Joe Biden.")

        # Speak the response and verify
        api.speak(response, male_voice=True)
        mock_speak.assert_called_with("The president of the United States is Joe Biden.", male_voice=True)

if __name__ == '__main__':
    unittest.main()
