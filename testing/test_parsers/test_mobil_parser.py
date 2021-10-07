import unittest
from parsers import mobil_parser


class TestMobilParser(unittest.TestCase):
    def test_parse(self):
        text = "something here, something there, +1(978)-204-2357, MA, something here"

        ground_truth = "+19782042357"
        hypothesis = mobil_parser.parse(text)

        self.assertEqual(hypothesis, ground_truth)


if __name__ == '__main__':
    unittest.main()