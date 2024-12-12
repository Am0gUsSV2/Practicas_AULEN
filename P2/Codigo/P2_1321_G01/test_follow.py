import unittest
from typing import AbstractSet

from src.grammar import Grammar
from src.utils import GrammarFormat


class TestFollow(unittest.TestCase):
    def _check_follow(
        self,
        grammar: Grammar,
        symbol: str,
        follow_set: AbstractSet[str],
    ) -> None:
        with self.subTest(string=f"Follow({symbol}), expected {follow_set}"):
            computed_follow = grammar.compute_follow(symbol)
            self.assertEqual(computed_follow, follow_set)

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
        self._check_follow(grammar, "E", {'$', ')'})
        self._check_follow(grammar, "T", {'$', ')', '+'})
        self._check_follow(grammar, "X", {'$', ')'})
        self._check_follow(grammar, "Y", {'$', ')', '+'})

    def test_case2(self) -> None:

        """Test Case 2: Follow sets for a different grammar."""
        grammar_str = """
        S -> AB
        A -> aA
        A ->
        B -> bB
        B -> c
        """
        
        grammar = GrammarFormat.read(grammar_str)
        
        # Follow de S es {'$', 'b', 'c'}, ya que es el axioma y el Follow de S debe contener '$'.
        self._check_follow(grammar, "S", {'$'})
        
        # Follow de A es {'b', 'c'}, porque A está seguido por B en la producción S -> AB.
        self._check_follow(grammar, "A", {'b', 'c'})
        
        # Follow de B es {'$', 'c'}, ya que B está al final de la producción S -> AB, y Follow(S) incluye '$'.
        self._check_follow(grammar, "B", {'$'})
    
    def test_case_3(self) -> None:
        """Test Case with Recursions."""
        grammar_str = """
        S -> aS
        S -> bA
        A -> cA
        A -> d
        """

        grammar = GrammarFormat.read(grammar_str)
        self._check_follow(grammar, "S", {'$'})  # Follow(S) incluye '$' porque S es el axioma, y 'c' o 'd' pueden venir de A.
        self._check_follow(grammar, "A", {'$'})  # Follow(A) incluye Follow(S) porque A aparece en S -> bA.

    def test_case_4(self) -> None:
        grammar_str = """
        S -> AB
        A -> aA
        A ->
        B -> bB
        B ->
        """
        
        grammar = GrammarFormat.read(grammar_str)
        self._check_follow(grammar, "S", {'$'})
        self._check_follow(grammar, "A", {'b', '$'})
        self._check_follow(grammar, "B", {'$'})
        

if __name__ == '__main__':
    unittest.main()
