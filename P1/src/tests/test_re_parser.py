"""Test evaluation of regex parser."""
import unittest

from automaton import FiniteAutomaton
from re_parser import REParser
from utils import write_dot


class TestREParser(unittest.TestCase):
    """Tests for regex parser."""

    def _create_evaluator(self, regex):
        automaton = REParser().create_automaton(regex)
        with open('automata.dot', 'w') as fdot:
            fdot.write(write_dot(automaton))
        return automaton

    def _check_accept(self, evaluator, string, should_accept = True):
        with self.subTest(string=string):
            accepted = evaluator.accepts(string)
            self.assertEqual(accepted, should_accept)

    def test_fixed(self):
        """Test fixed regex."""
        evaluator = self._create_evaluator("H.e.l.l.o")

        self._check_accept(evaluator, "Hello", should_accept=True)
        self._check_accept(evaluator, "Helloo", should_accept=False)
        self._check_accept(evaluator, "Hell", should_accept=False)
        self._check_accept(evaluator, "llH", should_accept=False)
        self._check_accept(evaluator, "", should_accept=False)

    def test_star(self):
        """Test Kleene star."""
        evaluator = self._create_evaluator("a*.b*")

        self._check_accept(evaluator, "", should_accept=True)
        self._check_accept(evaluator, "a", should_accept=True)
        self._check_accept(evaluator, "b", should_accept=True)
        self._check_accept(evaluator, "aa", should_accept=True)
        self._check_accept(evaluator, "bb", should_accept=True)
        self._check_accept(evaluator, "ab", should_accept=True)
        self._check_accept(evaluator, "ba", should_accept=False)
        self._check_accept(evaluator, "aab", should_accept=True)
        self._check_accept(evaluator, "abb", should_accept=True)
        self._check_accept(evaluator, "aba", should_accept=False)
        self._check_accept(evaluator, "bab", should_accept=False)

    def test_or(self):
        """Test Kleene star."""
        evaluator = self._create_evaluator("(a+b)*")

        self._check_accept(evaluator, "", should_accept=True)
        self._check_accept(evaluator, "a", should_accept=True)
        self._check_accept(evaluator, "b", should_accept=True)
        self._check_accept(evaluator, "aa", should_accept=True)
        self._check_accept(evaluator, "bb", should_accept=True)
        self._check_accept(evaluator, "ab", should_accept=True)
        self._check_accept(evaluator, "ba", should_accept=True)
        self._check_accept(evaluator, "aab", should_accept=True)
        self._check_accept(evaluator, "abb", should_accept=True)
        self._check_accept(evaluator, "aba", should_accept=True)
        self._check_accept(evaluator, "bab", should_accept=True)

    def test_number(self):
        """Test number expression."""
        num = "(0+1+2+3+4+5+6+7+8+9)"
        evaluator = self._create_evaluator(
            f"({num}.{num}*.,.{num}*)+{num}*",
        )

        self._check_accept(evaluator, ",", should_accept=False)
        self._check_accept(evaluator, "1,7", should_accept=True)
        self._check_accept(evaluator, "25,73", should_accept=True)
        self._check_accept(evaluator, "5027", should_accept=True)
        self._check_accept(evaluator, ",13", should_accept=False)
        self._check_accept(evaluator, "13,", should_accept=True)
        self._check_accept(evaluator, "3,7,12", should_accept=False)


if __name__ == "__main__":
    unittest.main()
