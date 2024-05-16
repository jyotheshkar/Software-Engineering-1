import unittest
from unittest.mock import patch, MagicMock, call
import makenotes  

class TestNotesMakerModule(unittest.TestCase):

    @patch('pyttsx3.init')
    def test_speak(self, mock_init):
        """
        Test the speak function to ensure it initializes the TTS engine and speaks the given text.
        """
        mock_engine = MagicMock()
        mock_init.return_value = mock_engine
        notes_maker = makenotes.NotesMaker()

        notes_maker.speak("Hello, world!")
        
        # Check if the TTS engine was initialized
        mock_init.assert_called_once()
        # Check if the engine said the correct text
        mock_engine.say.assert_called_with("Hello, world!")
        # Check if the engine ran and waited
        mock_engine.runAndWait.assert_called_once()

    @patch('makenotes.sr.Microphone')
    @patch('makenotes.sr.Recognizer')
    def test_listen_command(self, mock_recognizer, mock_microphone):
        """
        Test the listen_command function to ensure it listens for commands and returns the recognized text.
        """
        mock_recognizer_instance = MagicMock()
        mock_recognizer.return_value = mock_recognizer_instance
        mock_recognizer_instance.recognize_google.return_value = "test command"

        notes_maker = makenotes.NotesMaker()
        result = notes_maker.listen_command()
        
        # Check if the recognized command is returned correctly
        self.assertEqual(result, "test command")

    @patch('pyautogui.press')
    @patch('pyautogui.write')
    @patch('pyautogui.sleep')
    @patch('pyautogui.hotkey')
    def test_open_notepad(self, mock_hotkey, mock_sleep, mock_write, mock_press):
        """
        Test the open_notepad function to ensure it opens Notepad and creates a new window.
        """
        notes_maker = makenotes.NotesMaker()

        notes_maker.open_notepad()
        
        # Check if the correct sequence of actions was performed to open Notepad
        mock_press.assert_called_with("win")
        mock_sleep.assert_any_call(1)
        mock_write.assert_called_with("notepad")
        mock_press.assert_called_with("enter")
        mock_sleep.assert_any_call(2)
        mock_hotkey.assert_called_with("ctrl", "n")

    @patch('os.path.expanduser', return_value='mock_user_home')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch('makenotes.NotesMaker.listen_command', side_effect=["note 1", "note 2", "stop"])
    @patch('makenotes.NotesMaker.speak')
    @patch('pyautogui.typewrite')
    def test_create_notes(self, mock_typewrite, mock_speak, mock_listen_command, mock_open, mock_expanduser):
        """
        Test the create_notes function to ensure it creates notes and saves them correctly.
        """
        notes_maker = makenotes.NotesMaker()
        note_file = 'mock_user_home/Desktop/Todays_notes.txt'

        with patch('makenotes.NotesMaker.open_notepad') as mock_open_notepad:
            notes_maker.create_notes()
        
        # Check if Notepad was opened
        mock_open_notepad.assert_called_once()
        # Check if the initial heading was typed in Notepad
        today_datetime = datetime.datetime.now().strftime("%A, %B %d, %Y %I:%M %p")
        heading = f"Notes for {today_datetime}:\n\n"
        mock_typewrite.assert_any_call(heading)
        # Check if notes were typed in Notepad
        mock_typewrite.assert_any_call("note 1\n")
        mock_typewrite.assert_any_call("note 2\n")
        # Check if the save prompt was spoken
        mock_speak.assert_any_call("Do you want to save the notes? Please say 'yes' or 'no'.")
        # Check if the notes were saved to the correct file
        mock_open.assert_called_with(note_file, "w")
        mock_open().write.assert_any_call(heading)
        mock_open().write.assert_any_call("note 1\nnote 2\n")
        # Check if the confirmation was spoken
        mock_speak.assert_any_call("Notes saved successfully.")

if __name__ == '__main__':
    unittest.main()
