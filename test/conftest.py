from unittest.mock import patch
import unittest
import sys
from app.find_keywords import retrieve_file_keywords

x=484
class make_tests(unittest.TestCase):
    def test_find_keyword(self):
        keywords=['Henry', 'Kitchen']
        path="test_files/"
        ind_file=["test_file.txt"]
        return_file="return_data/return_info.xlsx"
        get_files=retrieve_file_keywords(path, keywords,ind_file, return_file)
        get_files.run()
        self.assertFalse