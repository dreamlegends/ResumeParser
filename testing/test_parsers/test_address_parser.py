import unittest
from parsers import address_parser


class TestAddressParser(unittest.TestCase):
    def test_parse(self):
        text = "something here, something there, 1000 skyline Dr., APT #1, Lowell, MA, something here"

        ground_truth = "1000 skyline Dr., APT #1, Lowell, MA"
        hypothesis = address_parser.parse(text).get_full_address()

        self.assertEqual(hypothesis, ground_truth)


if __name__ == '__main__':
    unittest.main()