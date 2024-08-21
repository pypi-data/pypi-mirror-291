import unittest
import re
from unittest.mock import patch, mock_open
from doc_insights.link_validation import gather_all_filenames, extract_links_from_app_dirs

class TestLinkValidation(unittest.TestCase):

    @patch('os.walk')
    def test_gather_all_filenames(self, mock_walk):
        # Mock directory walk
        mock_walk.return_value = [
            ('/root', ('subdir',), ('file1.c3doc.md', 'file2.c3typ', 'image.png')),
            ('/root/subdir', (), ('file3.md', 'file4.c3typ')),
        ]

        # Run the function
        filenames = gather_all_filenames(['/root'], ['.c3doc.md', '.c3typ'])

        # Test assertions
        self.assertIn('file1.c3doc.md', filenames)
        self.assertIn('file2.c3typ', filenames)
        self.assertIn('image.png', filenames)
        self.assertNotIn('file3.md', filenames)

    @patch('os.walk')
    def test_extract_links_from_app_dirs(self, mock_walk):
        # Mock directory walk
        mock_walk.return_value = [
            ('/root', (), ('file1.c3doc.md',)),
        ]
        with patch('builtins.open', mock_open(read_data='[link](doc.c3doc.md)\n{@link MyType}')):
            links_data = extract_links_from_app_dirs(['/root'], {
                'doc': re.compile(r'\[.*?\]\((.*?\.c3doc\.md)\)'),
                'type': re.compile(r'\{@link ([\w.]+)'),
                'image': re.compile(r'!\[.*?\]\((.*?)\)')
            })

        # Test assertions
        self.assertEqual(len(links_data['doc_links']), 1)
        self.assertEqual(len(links_data['type_links']), 1)
        self.assertEqual(links_data['doc_links'][0]['Links'][0], 'doc.c3doc.md')
        self.assertEqual(links_data['type_links'][0]['Links'][0], 'MyType.c3typ')  # Update expected value

if __name__ == '__main__':
    unittest.main()
