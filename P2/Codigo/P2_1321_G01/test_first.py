import unittest
from typing import AbstractSet

from src.grammar import Grammar
from src.utils import GrammarFormat


class TestFirst(unittest.TestCase):
    def _check_first(
        self,
        grammar: Grammar,
        input_string: str,
        first_set: AbstractSet[str],
    ) -> None:
        with self.subTest(
            string=f"First({input_string}), expected {first_set}",
        ):
            computed_first = grammar.compute_first(input_string)
            self.assertEqual(computed_first, first_set)

    def test_case1(self) -> None:
        """Test Case 1."""
        grammar_str = """
        E -> TX
        X -> +E
        X ->
        T -> iY
        T -> (E)
        Y -> *T
        Y ->
        """

        grammar = GrammarFormat.read(grammar_str)
        self._check_first(grammar, "E", {'(', 'i'})
        self._check_first(grammar, "T", {'(', 'i'})
        self._check_first(grammar, "X", {'', '+'})
        self._check_first(grammar, "Y", {'', '*'})
        self._check_first(grammar, "", {''})
        self._check_first(grammar, "Y+i", {'+', '*'})
        self._check_first(grammar, "YX", {'+', '*', ''})
        self._check_first(grammar, "YXT", {'+', '*', 'i', '('})
    
    def test_case2(self) -> None:
        """Test Case 2."""
        grammar_str = """
        S -> aBC
        B -> b
        B -> 
        C -> cD
        C -> 
        D -> d
        D -> 
        """

        grammar = GrammarFormat.read(grammar_str)
        self._check_first(grammar, "S", {'a'})
        self._check_first(grammar, "B", {'b', ''})
        self._check_first(grammar, "C", {'c', ''})
        self._check_first(grammar, "D", {'d', ''})
        self._check_first(grammar, "BC", {'b', 'c', ''})
        self._check_first(grammar, "aBC", {'a'})
        self._check_first(grammar, "BCD", {'b', 'c', 'd', ''})
    
    def test_case3(self) -> None:
        """Test Case 3."""
        grammar_str = """
        S -> AB
        A -> aA
        A -> 
        B -> b
        B -> c
        """

        grammar = GrammarFormat.read(grammar_str)
        self._check_first(grammar, "S", {'a', 'b', 'c'})
        self._check_first(grammar, "A", {'a', ''})
        self._check_first(grammar, "B", {'b', 'c'})
        self._check_first(grammar, "AB", {'a', 'b', 'c'})
        self._check_first(grammar, "aB", {'a'})
        self._check_first(grammar, "Ab", {'a', 'b'})
    
    def test_case4(self) -> None:
        grammar_str = """
        S -> aS
        S -> bA
        A -> cA
        A -> d
        """

        grammar = GrammarFormat.read(grammar_str)
        self._check_first(grammar, "S", {'a', 'b'})
        self._check_first(grammar, "A", {'c', 'd'})
        self._check_first(grammar, "aS", {'a'})
        self._check_first(grammar, "bA", {'b'})
        self._check_first(grammar, "cA", {'c'})
        self._check_first(grammar, "d", {'d'})
    
    def test_case5(self) -> None:
        grammar_str = """
        S -> Aa
        S -> b
        A -> Ac
        A -> d
        """

        grammar = GrammarFormat.read(grammar_str)
        self._check_first(grammar, "S", {'d', 'b'})
        self._check_first(grammar, "A", {'d'})
        self._check_first(grammar, "Aa", {'d'})
        self._check_first(grammar, "b", {'b'})
        self._check_first(grammar, "Ac", {'d'})
        self._check_first(grammar, "d", {'d'})







if __name__ == '__main__':
    unittest.main()
