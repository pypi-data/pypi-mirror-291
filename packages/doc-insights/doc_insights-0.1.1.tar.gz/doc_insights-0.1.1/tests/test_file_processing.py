import unittest
from unittest.mock import patch, MagicMock
from collections import defaultdict
from doc_insights.file_processing import count_files_in_single_directory

class TestFileProcessing(unittest.TestCase):

    @patch('os.scandir')
    @patch('doc_insights.file_processing.extract_metadata')
    def test_count_files_in_single_directory(self, mock_extract_metadata, mock_scandir):
        # Mock a file entry
        mock_file = MagicMock()
        mock_file.is_file.return_value = True
        mock_file.name = 'test.c3doc.md'

        # Create a mock scandir that supports the context manager and only returns the file
        mock_scandir_obj = MagicMock()
        mock_scandir_obj.__enter__.return_value = [mock_file]
        mock_scandir_obj.__exit__.return_value = None
        mock_scandir.return_value = mock_scandir_obj

        mock_extract_metadata.return_value = {'Title': 'Test Title', 'Abstract': 'Test Abstract'}

        # Run the function
        scan_cache = {}
        count, metadata = count_files_in_single_directory(
            directory='mock_directory',
            extensions=['.c3doc.md', '.c3typ'],
            scan_cache=scan_cache,
            subdirs_to_ignore=[],  # No subdirs to ignore since we aren't mocking them here
            log_file_path='mock_log.txt'
        )

        # Test assertions
        self.assertEqual(count['.c3doc.md'], 1)
        self.assertEqual(len(metadata), 1)
        self.assertEqual(metadata[0]['Title'], 'Test Title')
        self.assertEqual(metadata[0]['Abstract'], 'Test Abstract')

    @patch('os.scandir')
    def test_permission_error(self, mock_scandir):
        # Mock scandir to raise a PermissionError
        mock_scandir.side_effect = PermissionError

        # Run the function
        scan_cache = {}
        count, metadata = count_files_in_single_directory(
            directory='mock_directory',
            extensions=['.c3doc.md', '.c3typ'],
            scan_cache=scan_cache,
            subdirs_to_ignore=[],
            log_file_path='mock_log.txt'
        )

        # Test assertions
        self.assertEqual(count, defaultdict(int))
        self.assertEqual(metadata, [])

    @patch('os.scandir')
    def test_generic_error(self, mock_scandir):
        # Mock scandir to raise a generic Exception
        mock_scandir.side_effect = Exception('Generic error')

        # Run the function
        scan_cache = {}
        count, metadata = count_files_in_single_directory(
            directory='mock_directory',
            extensions=['.c3doc.md', '.c3typ'],
            scan_cache=scan_cache,
            subdirs_to_ignore=[],
            log_file_path='mock_log.txt'
        )

        # Test assertions
        self.assertEqual(count, defaultdict(int))
        self.assertEqual(metadata, [])

if __name__ == '__main__':
    unittest.main()
