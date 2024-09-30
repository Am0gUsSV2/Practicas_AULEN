#!/usr/bin/env python

import re
import unittest

from regular_expressions import RE0, RE1, RE2, RE3, RE4, RE5


class TestP0(unittest.TestCase):
    """Tests of assignment 0."""

    def check_expression(self, expr: str, string: str, expected: bool) -> None:
        with self.subTest(string=string):
            match = re.fullmatch(expr, string)
            self.assertEqual(bool(match), expected)




    def test_exercise_2(self) -> None:
        self.check_expression(RE2, "-.45", True)
        self.check_expression(RE2, "-0", False)
        self.check_expression(RE2, "0", True)
        self.check_expression(RE2, "0.", True)
        self.check_expression(RE2, ".0", True)
        self.check_expression(RE2, "011", False)
        self.check_expression(RE2, "-11", True)
        self.check_expression(RE2, "0.1", True)
        self.check_expression(RE2, ".1", True)
        self.check_expression(RE2, "-0.1", True)
        self.check_expression(RE2, "0.1", True)
        self.check_expression(RE2, "01.1", False)

    def test_exercise_4(self) -> None:
        self.check_expression(RE4, "0+0", False)
        self.check_expression(RE4, "1+1", True)
        self.check_expression(RE4, "01-02", False)
        self.check_expression(RE4, "20=30", False)
        self.check_expression(RE4, "2=33/44", False)
        self.check_expression(RE4, "2+33/44", True)
        self.check_expression(RE4, "4324324/234432/2+33/44", True)
        self.check_expression(RE4, "0/234432/2+33/44", False)



if __name__ == '__main__':
    unittest.main()
