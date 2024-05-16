import unittest
from unittest.mock import patch, MagicMock, call
import youtube  

class TestYouTubeModule(unittest.TestCase):

    @patch('youtube.nlp')
    def test_contains_listen_music_keywords(self, mock_nlp):
        """
        Test the contains_listen_music_keywords function to ensure it detects keywords related to listening to music.
        """
        mock_doc = MagicMock()
        mock_nlp.return_value = mock_doc

        # Test case with keywords
        mock_doc.__iter__.return_value = [MagicMock(text='listen'), MagicMock(text='to'), MagicMock(text='music')]
        result = youtube.contains_listen_music_keywords("listen to music")
        self.assertTrue(result)

        # Test case without keywords
        mock_doc.__iter__.return_value = [MagicMock(text='play'), MagicMock(text='a'), MagicMock(text='game')]
        result = youtube.contains_listen_music_keywords("play a game")
        self.assertFalse(result)

    @patch('youtube.pyautogui.press')
    def test_toggle_play_pause(self, mock_press):
        """
        Test the toggle_play_pause function to ensure it presses the space key to toggle play/pause.
        """
        youtube.toggle_play_pause()
        mock_press.assert_called_with('space')

    @patch('youtube.pyautogui.hotkey')
    def test_stop_music(self, mock_hotkey):
        """
        Test the stop_music function to ensure it closes the browser tab.
        """
        youtube.stop_music()
        mock_hotkey.assert_called_with('ctrl', 'w')

    @patch('youtube.pyautogui.press')
    def test_control_volume(self, mock_press):
        """
        Test the control_volume function to ensure it controls the volume based on the action.
        """
        # Test case for increasing volume
        youtube.control_volume("increase")
        mock_press.assert_called_with('volumeup')

        # Test case for decreasing volume
        youtube.control_volume("decrease")
        mock_press.assert_called_with('volumedown')

    @patch('youtube.authenticate', return_value=True)
    @patch('youtube.sr.Recognizer')
    @patch('youtube.sr.Microphone')
    @patch('youtube.contains_listen_music_keywords', return_value=True)
    @patch('youtube.webbrowser.open')
    @patch('youtube.pyttsx3.init')
    @patch('youtube.time.sleep')
    @patch('youtube.pyautogui.click')
    def test_main(self, mock_click, mock_sleep, mock_pyttsx3_init, mock_webbrowser_open, mock_contains_listen_music_keywords, mock_Microphone, mock_Recognizer, mock_authenticate):
        """
        Test the main function to ensure it processes commands and performs the correct actions.
        """
        # Mock recognizer instance and audio input
        mock_recognizer_instance = MagicMock()
        mock_Recognizer.return_value = mock_recognizer_instance
        mock_recognizer_instance.listen.return_value = MagicMock()
        mock_recognizer_instance.recognize_google.side_effect = ["listen to music", "some song", "stop music"]

        mock_mic_instance = MagicMock()
        mock_Microphone.return_value = mock_mic_instance

        mock_engine = MagicMock()
        mock_pyttsx3_init.return_value = mock_engine

        # Run the main function
        with patch('builtins.print'):
            youtube.main()

        # Check if authentication was called
        mock_authenticate.assert_called_once()

        # Check if the web browser opened the correct search URL
        mock_webbrowser_open.assert_called_with("https://www.youtube.com/results?search_query=some+song")

        # Check if the video was clicked
        mock_sleep.assert_called()
        mock_click.assert_called_with(x=430, y=305)

        # Check if the TTS engine was initialized and used
        mock_engine.say.assert_any_call("What artist or song would you like to listen to?")
        mock_engine.runAndWait.assert_any_call()
        mock_engine.say.assert_any_call("Web scraping has been successful.")

if __name__ == '__main__':
    unittest.main()
