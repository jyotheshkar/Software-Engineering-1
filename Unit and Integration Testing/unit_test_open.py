import unittest
from unittest.mock import patch, MagicMock, call
import open  # Import the main script

class TestOpenScript(unittest.TestCase):

    # Test the listen function
    @patch('open.speak')
    @patch('open.sr.Recognizer')
    @patch('open.sr.Microphone')
    def test_listen(self, mock_microphone, mock_recognizer, mock_speak):
        # Mock the recognizer and microphone
        mock_recognizer_instance = MagicMock()
        mock_recognizer.return_value = mock_recognizer_instance
        mock_recognizer_instance.listen.return_value = "audio_data"
        mock_recognizer_instance.recognize_google.return_value = "open instagram"
        
        # Call the listen function
        result = open.listen()
        
        # Check if the result is as expected
        self.assertEqual(result, "open instagram")

    # Test the open_application function
    @patch('open.speak')
    @patch('pyautogui.press')
    @patch('pyautogui.write')
    @patch('pyautogui.click')
    @patch('time.sleep')
    @patch('ctypes.windll.user32.GetForegroundWindow')
    @patch('ctypes.windll.user32.ShowWindow')
    def test_open_application(self, mock_show_window, mock_get_foreground_window, mock_sleep, mock_click, mock_write, mock_press, mock_speak):
        # Mock window handle
        mock_get_foreground_window.return_value = 1234
        
        # Call the open_application function with "instagram"
        open.open_application("instagram")
        
        # Check if speak was called
        mock_speak.assert_called()
        
        # Check if the correct keys were pressed
        expected_calls = [
            call('win'),
            call('enter')
        ]
        mock_press.assert_has_calls(expected_calls, any_order=False)
        
        # Check if the correct text was written
        mock_write.assert_called_with("instagram")
        
        # Check if the window was maximized
        mock_get_foreground_window.assert_called()
        mock_show_window.assert_called_with(1234, 3)
    
    # Test the open_webpage function
    @patch('open.speak')
    @patch('webbrowser.open')
    def test_open_webpage(self, mock_web_open, mock_speak):
        # Call the open_webpage function with a test URL
        open.open_webpage("http://example.com")
        
        # Check if speak was called
        mock_speak.assert_called()
        
        # Check if the web browser was opened with the correct URL
        mock_web_open.assert_called_with("http://example.com")

    # Test the scroll_up function
    @patch('open.speak')
    @patch('pyautogui.scroll')
    def test_scroll_up(self, mock_scroll, mock_speak):
        # Call the scroll_up function
        open.scroll_up()
        
        # Check if the page was scrolled up
        mock_scroll.assert_called_with(900)
        
        # Check if speak was called
        mock_speak.assert_called_with("Scrolled up.")

    # Test the scroll_down function
    @patch('open.speak')
    @patch('pyautogui.scroll')
    def test_scroll_down(self, mock_scroll, mock_speak):
        # Call the scroll_down function
        open.scroll_down()
        
        # Check if the page was scrolled down
        mock_scroll.assert_called_with(-900)
        
        # Check if speak was called
        mock_speak.assert_called_with("Scrolled down.")

    # Test the close_application function
    @patch('open.speak')
    @patch('pyautogui.getWindowsWithTitle')
    def test_close_application(self, mock_get_windows_with_title, mock_speak):
        # Mock a window object
        mock_window = MagicMock()
        mock_get_windows_with_title.return_value = [mock_window]

        # Call the close_application function with "instagram"
        open.close_application("instagram")
        
        # Check if the window was closed
        mock_window.close.assert_called()
        
        # Check if speak was called
        mock_speak.assert_called_with("The instagram application has been closed.")

    # Test the process_command function
    def test_process_command(self):
        # Call the process_command function with a test command
        command = "open instagram"
        verb, obj = open.process_command(command)
        
        # Check if the verb and object were correctly extracted
        self.assertEqual(verb, "open")
        self.assertEqual(obj, "instagram")

if __name__ == '__main__':
    unittest.main()
