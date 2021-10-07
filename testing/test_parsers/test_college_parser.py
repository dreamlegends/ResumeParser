import unittest
import pandas as pd
from parsers import college_parser
import os


class TestCollegeParser(unittest.TestCase):
    def setUp(self) -> None:
        os.path.dirname(os.path.abspath(__file__))

        data = pd.read_csv('../../info/universities.csv')

        colleges = list(data.name)  # full list of colleges
        colleges = [college.upper() for college in colleges]

        # some alternative names
        colleges += [college.replace(" AT ", " ") for college in colleges if ' AT ' in college]
        colleges += [college.replace(" AT ", ", ") for college in colleges if ' AT ' in college]
        self.colleges = colleges

    def test_parse(self):
        text = ["something here", "something there", "Boston University", "Massachusetts Institute of Technology", "something here"]

        ground_truth = ["Boston University".upper(), 'Massachusetts Institute of Technology'.upper()]
        hypothesis = college_parser.parse(text, self.colleges)

        self.assertEqual(ground_truth, hypothesis)


if __name__ == '__main__':
    unittest.main()