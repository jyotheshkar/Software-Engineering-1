import unittest
from unittest.mock import patch, MagicMock
import datetime
import nova 

class TestNovaModule(unittest.TestCase):

    @patch('pyttsx3.init')
    def test_speak(self, mock_init):
        """
        Test the speak function to ensure it initializes the TTS engine and speaks the given text.
        """
        mock_engine = MagicMock()
        mock_init.return_value = mock_engine
        assistant = nova.VoiceAssistant(mock_engine)

        assistant.speak("Hello, world!")
        
        # Check if the TTS engine was initialized
        mock_init.assert_called_once()
        # Check if the engine said the correct text
        mock_engine.say.assert_called_with("Hello, world!")
        # Check if the engine ran and waited
        mock_engine.runAndWait.assert_called_once()

    @patch('nova.sr.Microphone')
    @patch('nova.sr.Recognizer')
    def test_listen_command(self, mock_recognizer, mock_microphone):
        """
        Test the listen_command function to ensure it listens for commands and returns the recognized text.
        """
        mock_recognizer_instance = MagicMock()
        mock_recognizer.return_value = mock_recognizer_instance
        mock_recognizer_instance.recognize_google.return_value = "test command"

        assistant = nova.VoiceAssistant(mock_recognizer_instance)
        result = assistant.listen_command()
        
        # Check if the recognized command is returned correctly
        self.assertEqual(result, "test command")

    def test_get_time_of_day(self):
        """
        Test the get_time_of_day function to ensure it returns the correct part of the day.
        """
        assistant = nova.Jarvis(None)

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
        assistant = nova.Jarvis(None)
        self.assertEqual(assistant.get_funny_response("morning"), "Good morning! Let's make this day special. How can I help?")
        self.assertEqual(assistant.get_funny_response("afternoon"), "Good afternoon! Hope you're having a splendid day!")
        self.assertEqual(assistant.get_funny_response("evening"), "Good evening! Time to unwind and relax!")
        self.assertEqual(assistant.get_funny_response("night"), "Good night! Sweet dreams and see you tomorrow!")

    @patch('nova.pyautogui.press')
    @patch('nova.time.sleep')
    @patch('nova.ctypes.windll.user32.GetForegroundWindow')
    @patch('nova.ctypes.windll.user32.ShowWindow')
    @patch('nova.pyautogui.write')
    @patch('nova.random.choice', return_value="On it...")
    def test_open_application(self, mock_random_choice, mock_write, mock_show_window, mock_get_foreground_window, mock_sleep, mock_press):
        """
        Test the open_application function to ensure it opens the specified application.
        """
        mock_engine = MagicMock()
        assistant = nova.Jarvis(mock_engine)

        assistant.open_application("notepad")
        
        # Check if the speak function was called with the correct phrase
        mock_engine.say.assert_any_call("On it...")
        mock_engine.say.assert_any_call("notepad opened in fullscreen mode.")
        # Check if the correct sequence of actions was performed to open the application
        mock_press.assert_called_with('win')
        mock_write.assert_called_with("notepad")
        mock_press.assert_called_with('enter')
        mock_get_foreground_window.assert_called_once()
        mock_show_window.assert_called_with(mock_get_foreground_window.return_value, 3)

    @patch('nova.pyautogui.getWindowsWithTitle')
    @patch('nova.pyautogui.click')
    @patch('nova.speak')
    def test_close_application(self, mock_speak, mock_get_windows_with_title, mock_click):
        """
        Test the close_application function to ensure it closes the specified application.
        """
        mock_window = MagicMock()
        mock_get_windows_with_title.return_value = [mock_window]
        mock_engine = MagicMock()
        assistant = nova.Jarvis(mock_engine)

        assistant.close_application("notepad")
        
        # Check if the window was closed
        mock_window.close.assert_called_once()
        # Check if the speak function was called with the correct message
        mock_engine.say.assert_called_with("The notepad application has been closed.")

    @patch('nova.speak')
    @patch('nova.pyautogui.scroll')
    def test_scroll_up(self, mock_scroll, mock_speak):
        """
        Test the scroll_up function to ensure it scrolls up and speaks the action.
        """
        mock_engine = MagicMock()
        assistant = nova.Jarvis(mock_engine)

        assistant.scroll_up()
        
        # Check if the page was scrolled up
        mock_scroll.assert_called_with(900)
        # Check if the speak function was called with the correct message
        mock_engine.say.assert_called_with("Scrolled up.")

    @patch('nova.speak')
    @patch('nova.pyautogui.scroll')
    def test_scroll_down(self, mock_scroll, mock_speak):
        """
        Test the scroll_down function to ensure it scrolls down and speaks the action.
        """
        mock_engine = MagicMock()
        assistant = nova.Jarvis(mock_engine)

        assistant.scroll_down()
        
        # Check if the page was scrolled down
        mock_scroll.assert_called_with(-900)
        # Check if the speak function was called with the correct message
        mock_engine.say.assert_called_with("Scrolled down.")

    @patch('spacy.load')
    def test_process_command(self, mock_spacy_load):
        """
        Test the process_command function to ensure it processes the command and extracts the verb and noun.
        """
        mock_nlp = MagicMock()
        mock_doc = MagicMock()
        mock_spacy_load.return_value = mock_nlp
        mock_nlp.return_value = mock_doc
        mock_doc.__iter__.return_value = [MagicMock(pos_='VERB', lemma_='open'), MagicMock(pos_='NOUN', text='notepad')]

        assistant = nova.Jarvis(None)
        verb, obj = assistant.process_command("open notepad")
        
        # Check if the verb and object were extracted correctly
        self.assertEqual(verb, "open")
        self.assertEqual(obj, "notepad")

if __name__ == '__main__':
    unittest.main()
