import unittest
from unittest.mock import patch, MagicMock
import pyttsx3
import voice  

class TestVoiceModule(unittest.TestCase):

    @patch('pyttsx3.init')
    def test_print_available_voices(self, mock_init):
        """
        Test the print_available_voices function to ensure it prints the available voices.
        """
        mock_engine = MagicMock()
        mock_init.return_value = mock_engine
        mock_voices = [MagicMock(name='Voice 1'), MagicMock(name='Voice 2')]
        mock_engine.getProperty.return_value = mock_voices

        voices = voice.print_available_voices(mock_engine)
        
        # Check if the voices were retrieved and printed correctly
        mock_engine.getProperty.assert_called_with('voices')
        self.assertEqual(voices, mock_voices)

    @patch('pyttsx3.init')
    def test_set_voice(self, mock_init):
        """
        Test the set_voice function to ensure it sets the voice correctly.
        """
        mock_engine = MagicMock()
        mock_init.return_value = mock_engine

        voice.set_voice(mock_engine, 'test_voice_id')
        
        # Check if the voice was set correctly
        mock_engine.setProperty.assert_called_with('voice', 'test_voice_id')

    @patch('pyttsx3.init')
    def test_speak(self, mock_init):
        """
        Test the speak function to ensure it speaks the given text.
        """
        mock_engine = MagicMock()
        mock_init.return_value = mock_engine

        voice.speak(mock_engine, "Hello, world!")
        
        # Check if the engine said the correct text
        mock_engine.say.assert_called_with("Hello, world!")
        # Check if the engine ran and waited
        mock_engine.runAndWait.assert_called_once()

    @patch('voice.speak')
    @patch('pyttsx3.init')
    def test_reply(self, mock_init, mock_speak):
        """
        Test the reply function to ensure it speaks the given text.
        """
        mock_engine = MagicMock()
        mock_init.return_value = mock_engine

        voice.reply(mock_engine, "Hello!")
        
        # Check if the speak function was called with the correct text
        mock_speak.assert_called_with(mock_engine, "Hello!")

    @patch('voice.print_available_voices')
    @patch('voice.set_voice')
    @patch('voice.reply')
    @patch('pyttsx3.init')
    def test_main(self, mock_init, mock_reply, mock_set_voice, mock_print_available_voices):
        """
        Test the main function to ensure it initializes the TTS engine, sets the voice, and tests the selected voice.
        """
        mock_engine = MagicMock()
        mock_init.return_value = mock_engine
        mock_voices = [MagicMock(id='voice_1_id', name='Voice 1'), MagicMock(id='voice_2_id', name='Voice 2')]
        mock_print_available_voices.return_value = mock_voices

        with patch('builtins.print'):
            voice.main()
        
        # Check if the engine was initialized
        mock_init.assert_called_once()
        # Check if the available voices were printed
        mock_print_available_voices.assert_called_with(mock_engine)
        # Check if the second voice was set and selected
        mock_set_voice.assert_called_with(mock_engine, 'voice_2_id')
        # Check if the reply function was called with the test text
        mock_reply.assert_called_with(mock_engine, "Hello! I'm here to assist you.")

if __name__ == '__main__':
    unittest.main()
