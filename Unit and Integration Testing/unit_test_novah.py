import unittest
from unittest.mock import patch, MagicMock
import datetime
import voice_assistant  

class TestVoiceAssistantModule(unittest.TestCase):

    @patch('pyttsx3.init')
    def test_speak(self, mock_init):
        """
        Test the speak function to ensure it initializes the TTS engine and speaks the given text.
        """
        mock_engine = MagicMock()
        mock_init.return_value = mock_engine
        assistant = voice_assistant.VoiceAssistant(mock_engine)

        assistant.speak("Hello, world!")
        
        # Check if the TTS engine was initialized
        mock_init.assert_called_once()
        # Check if the engine said the correct text
        mock_engine.say.assert_called_with("Hello, world!")
        # Check if the engine ran and waited
        mock_engine.runAndWait.assert_called_once()

    @patch('voice_assistant.sr.Microphone')
    @patch('voice_assistant.sr.Recognizer')
    def test_listen_command(self, mock_recognizer, mock_microphone):
        """
        Test the listen_command function to ensure it listens for commands and returns the recognized text.
        """
        mock_recognizer_instance = MagicMock()
        mock_recognizer.return_value = mock_recognizer_instance
        mock_recognizer_instance.recognize_google.return_value = "test command"

        assistant = voice_assistant.VoiceAssistant(mock_recognizer_instance)
        result = assistant.listen_command()
        
        # Check if the recognized command is returned correctly
        self.assertEqual(result, "test command")

    def test_get_time_of_day(self):
        """
        Test the get_time_of_day function to ensure it returns the correct part of the day.
        """
        assistant = voice_assistant.Novah(None)

        with patch('datetime.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime.datetime(2021, 1, 1, 8, 0, 0)
            self.assertEqual(assistant.get_time_of_day(), "morning")
            mock_datetime.now.return_value = datetime.datetime(2021, 1, 1, 13, 0, 0)
            self.assertEqual(assistant.get_time_of_day(), "afternoon")
            mock_datetime.now.return_value = datetime.datetime(2021, 1, 1, 19, 0, 0)
            self.assertEqual(assistant.get_time_of_day(), "evening")
            mock_datetime.now.return_value = datetime.datetime(2021, 1, 1, 23, 0, 0)
            self.assertEqual(assistant.get_time_of_day(), "night")

    def test_get_funny_response(self):
        """
        Test the get_funny_response function to ensure it returns the correct response for each time of day.
        """
        assistant = voice_assistant.Novah(None)
        self.assertEqual(assistant.get_funny_response("morning"), "Good morning! Let's make this day special. How can I help?")
        self.assertEqual(assistant.get_funny_response("afternoon"), "Good afternoon! Hope you're having a splendid day!")
        self.assertEqual(assistant.get_funny_response("evening"), "Good evening! Time to unwind and relax!")
        self.assertEqual(assistant.get_funny_response("night"), "Good night! Sweet dreams and see you tomorrow!")

    @patch('voice_assistant.VoiceAssistant.speak')
    def test_authenticate(self, mock_speak):
        """
        Test the authenticate function to ensure it correctly identifies wake and greeting words.
        """
        assistant = voice_assistant.Novah(None)
        
        assistant.authenticate("hey novah")
        self.assertTrue(assistant.is_awake)
        mock_speak.assert_called_with("Yes, I am here.")
        
        assistant.authenticate("nova are you awake")
        self.assertTrue(assistant.is_awake)
        mock_speak.assert_called_with("For you, sir, always.")
        
        assistant.authenticate("random command")
        self.assertFalse(assistant.is_awake)

    @patch('voice_assistant.VoiceAssistant.listen_command')
    @patch('voice_assistant.VoiceAssistant.speak')
    def test_prompt_request(self, mock_speak, mock_listen_command):
        """
        Test the prompt_request function to ensure it processes commands and provides appropriate responses.
        """
        mock_listen_command.side_effect = ["hello novah", "stop listening"]
        assistant = voice_assistant.Novah(None)
        
        with patch.object(assistant, 'get_time_of_day', return_value="morning"):
            with patch.object(assistant, 'get_funny_response', return_value="Good morning! Let's make this day special. How can I help?"):
                assistant.prompt_request()
        
        mock_speak.assert_any_call("Hello, Good morning! Let's make this day special. How can I help?")

if __name__ == '__main__':
    unittest.main()
