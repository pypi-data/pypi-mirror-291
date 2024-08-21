import unittest
from unittest.mock import patch, mock_open
from doc_insights.logging_utils import log_message

class TestLoggingUtils(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open)
    @patch('builtins.print')
    def test_log_message(self, mock_print, mock_open):
        # Run the function
        log_message('Test message', 'mock_log.txt')

        # Test assertions
        mock_open.assert_called_once_with('mock_log.txt', 'a')
        mock_print.assert_called_once_with('Test message')
        mock_open().write.assert_called_once_with('Test message\n')

if __name__ == '__main__':
    unittest.main()
