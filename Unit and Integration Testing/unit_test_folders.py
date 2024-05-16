import unittest
from unittest.mock import patch, MagicMock
import os
import folders  

class TestFoldersModule(unittest.TestCase):

    @patch('pyttsx3.init')
    def test_speak(self, mock_init):
        """
        Test the speak function to ensure it initializes the TTS engine and speaks the given text.
        """
        mock_engine = MagicMock()
        mock_init.return_value = mock_engine

        folders.speak("Hello, world!")
        
        # Check if the TTS engine was initialized
        mock_init.assert_called_once()
        # Check if the engine said the correct text
        mock_engine.say.assert_called_with("Hello, world!")
        # Check if the engine ran and waited
        mock_engine.runAndWait.assert_called_once()

    @patch('folders.sr.Microphone')
    @patch('folders.sr.Recognizer')
    def test_listen_for_commands(self, mock_recognizer, mock_microphone):
        """
        Test the listen_for_commands function to ensure it listens for commands and returns the recognized text.
        """
        mock_recognizer_instance = MagicMock()
        mock_recognizer.return_value = mock_recognizer_instance
        mock_recognizer_instance.recognize_google.return_value = "test command"

        result = folders.listen_for_commands()
        
        # Check if the recognized command is returned correctly
        self.assertEqual(result, "test command")

    @patch('folders.speak')
    @patch('os.makedirs')
    @patch('os.path.join', return_value='mock_desktop_path')
    def test_create_folder(self, mock_path_join, mock_makedirs, mock_speak):
        """
        Test the create_folder function to ensure it creates a folder on the desktop.
        """
        folders.create_folder("TestFolder")
        
        # Check if the folder path was correctly generated
        mock_path_join.assert_called()
        # Check if the folder was created
        mock_makedirs.assert_called_with('mock_desktop_path')
        # Check if the speak function was called with the success message
        mock_speak.assert_called_with("Folder 'TestFolder' created successfully on the desktop.")

    @patch('folders.speak')
    @patch('os.rmdir')
    @patch('os.path.join', return_value='mock_desktop_path')
    def test_delete_folder(self, mock_path_join, mock_rmdir, mock_speak):
        """
        Test the delete_folder function to ensure it deletes a folder from the desktop.
        """
        folders.delete_folder("TestFolder")
        
        # Check if the folder path was correctly generated
        mock_path_join.assert_called()
        # Check if the folder was deleted
        mock_rmdir.assert_called_with('mock_desktop_path')
        # Check if the speak function was called with the success message
        mock_speak.assert_called_with("Folder 'TestFolder' deleted successfully from the desktop.")

    @patch('folders.speak')
    @patch('folders.listen_for_commands')
    @patch('folders.create_folder')
    @patch('folders.delete_folder')
    def test_main(self, mock_delete_folder, mock_create_folder, mock_listen_for_commands, mock_speak):
        """
        Test the main function to ensure it handles commands for creating and deleting folders.
        """
        # Simulate a sequence of voice commands
        mock_listen_for_commands.side_effect = [
            "create folder", "NewFolder",  # Create a new folder
            "delete folder", "NewFolder",  # Delete the created folder
            "exit"  # Exit the program
        ]

        with patch('builtins.input', return_value='exit'):
            folders.main()
        
        # Check if the create folder process was called
        mock_speak.assert_any_call("What do you want to name the folder?")
        mock_create_folder.assert_called_with("NewFolder")
        # Check if the delete folder process was called
        mock_speak.assert_any_call("What's the name of the folder you want to delete?")
        mock_delete_folder.assert_called_with("NewFolder")
        # Check if the program exit message was called
        mock_speak.assert_any_call("Exiting the program.")

if __name__ == '__main__':
    unittest.main()
