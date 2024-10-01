#!/usr/bin/env python

import re
import unittest

from regular_expressions import RE1, RE2, RE3, RE4, RE5


class TestP0(unittest.TestCase):
    """Tests of assignment 0."""

    def check_expression(self, expr: str, string: str, expected: bool) -> None:
        with self.subTest(string=string):
            match = re.fullmatch(expr, string)
            self.assertEqual(bool(match), expected)


    def test_exercise_1(self) -> None:
        self.check_expression(RE1, "a", False)
        self.check_expression(RE1, "ab", True)
        self.check_expression(RE1, "aab", True)

        self.check_expression(RE1, "bc", False)
        self.check_expression(RE1, "abccc", True)

        self.check_expression(RE1, "aaac", False)
        self.check_expression(RE1, "abbcca", True)

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

    def test_exercise_3(self) -> None:
        self.check_expression(RE3, "", False)
        self.check_expression(RE3, "www.uam.es", True)

        self.check_expression(RE3, "www.uam.es/pepito/", True)
        self.check_expression(RE3, "moodle.uam.es/pepito", True)

        self.check_expression(RE3, "www.uam.es//pepito/", False)
        self.check_expression(RE3, "@gmail.pepito/", False)
        self.check_expression(RE3, "moodle.uam.es/pep/it/o", True)
        self.check_expression(RE3, "www.uam.es/pepito//", False)

    def test_exercise_4(self) -> None:
        self.check_expression(RE4, "0+0", False)
        self.check_expression(RE4, "1+1", True)
        self.check_expression(RE4, "01-02", False)
        self.check_expression(RE4, "20=30", False)
        self.check_expression(RE4, "2=33/44", False)
        self.check_expression(RE4, "2+33/44", True)
        self.check_expression(RE4, "4324324/234432/2+33/44", True)
        self.check_expression(RE4, "0/234432/2+33/44", False)

    def test_exercise_5(self) -> None:
        self.check_expression(RE5, "10*(11+12)", True)
        self.check_expression(RE5, "1+2", True)
        self.check_expression(RE5, "5*(6+7)-8/9", True)

        self.check_expression(RE5, "10*(11+12)10", False)
        self.check_expression(RE5, "0+1", False)
        self.check_expression(RE5, "((1+2))", False)



if __name__ == '__main__':
    unittest.main()
