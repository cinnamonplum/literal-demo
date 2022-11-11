import os
import unittest
from unittest.mock import mock_open, patch

from integrations.utils.file_writers import write_to_txt, write_to_csv


class FileWritersTestCase(unittest.TestCase):
    def test_write_to_txt(self):
        mock_filename = "test_write_to_txt.txt"
        m = mock_open()
        with patch("__main__.open", m, create=True):
            write_to_txt(mock_filename, "hello", "world", "from", "remote")

            with open(mock_filename) as h:
                result = h.read()

        self.assertTrue("world" in result)
        self.assertFalse("global" in result)

        file_exists = os.path.exists(mock_filename)
        self.assertTrue(file_exists)

        if file_exists:
            os.remove(mock_filename)

    def test_write_to_csv(self):
        mock_filename = "test_write_to_csv.csv"
        mock_content = {"param1": "first", "param2": "second", "param3": "third"}
        mock_fieldnames = ["param1", "param2", "param3"]
        m = mock_open()
        with patch("__main__.open", m):
            write_to_csv(mock_filename, mock_fieldnames, mock_content)
            with open(mock_filename) as h:
                result = h.read()

        self.assertTrue("second" in result)
        self.assertFalse("fourth" in result)

        file_exists = os.path.exists(mock_filename)
        self.assertTrue(file_exists)

        if file_exists:
            os.remove(mock_filename)
