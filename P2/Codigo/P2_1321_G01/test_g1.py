import unittest

from src.g1_parser import *

class TestGrammar(unittest.TestCase):
    def _check_analyze(self, input_string, valid):
        try:
            result = parser.parse(input_string)
            assert(result == valid)
        except:
            assert(not valid)

    def test_case_1(self):
        self._check_analyze("aabbccc", True)

    def test_case_2(self):
        self._check_analyze("aabbcc", False)

    # Casos adicionales
    def test_case_3(self):
        self._check_analyze("abbc", False)  # n=1, k=1

    def test_case_4(self):
        self._check_analyze("aaabbbcccc", True)  # n=3, k=4

    def test_case_5(self):
        self._check_analyze("abccccc", True)  # n=1, k=5

    def test_case_6(self):
        self._check_analyze("aaabbcc", False)  # n=3, k=2

    def test_case_7(self):
        self._check_analyze("ab", False)  # n=1, k=0

    def test_case_8(self):
        self._check_analyze("abc", False)  # n=1, k=1


if __name__ == '__main__':
    unittest.main()
