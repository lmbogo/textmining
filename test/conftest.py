from unittest.mock import patch
import unittest
import sys
import os
from app.find_keywords import retrieve_file_keywords

x=484
class make_tests(unittest.TestCase):
    def test_find_keyword(self):
        keywords=['Henry', 'Kitchen']
        wd=os.getcwd()
        path=f"{wd}/test/"
        print('HEY', path)
        ind_file=["test_files"]
        return_file=f"{path}return_data/return_info.xlsx"
        get_files=retrieve_file_keywords(path, keywords,ind_file, return_file)
        get_files.run()
        self.assertFalse