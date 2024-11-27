from __future__ import annotations

from collections import deque
from typing import AbstractSet, Collection, MutableSet, Optional, Dict, List, Optional

class RepeatedCellError(Exception):
    """Exception for repeated cells in LL(1) tables."""


class SyntaxError(Exception):
    """Exception for parsing errors."""
    pass

class Grammar:
    """
    Class that represents a grammar.

    Args:
        terminals: Terminal symbols of the grammar.
        non_terminals: Non terminal symbols of the grammar.
        productions: Dictionary with the production rules for each non terminal
          symbol of the grammar.
        axiom: Axiom of the grammar.

    """

    def __init__(
        self,
        terminals: AbstractSet[str],
        non_terminals: AbstractSet[str],
        productions: Dict[str, List[str]],
        axiom: str,
    ) -> None:
        if terminals & non_terminals:
            raise ValueError(
                "Intersection between terminals and non terminals "
                "must be empty.",
            )

        if axiom not in non_terminals:
            raise ValueError(
                "Axiom must be included in the set of non terminals.",
            )

        if non_terminals != set(productions.keys()):
            raise ValueError(
                f"Set of non-terminals and productions keys should be equal."
            )
        
        for nt, rhs in productions.items():
            if not rhs:
                raise ValueError(
                    f"No production rules for non terminal symbol {nt} "
                )
            for r in rhs:
                for s in r:
                    if (
                        s not in non_terminals
                        and s not in terminals
                    ):
                        raise ValueError(
                            f"Invalid symbol {s}.",
                        )

        self.terminals = terminals
        self.non_terminals = non_terminals
        self.productions = productions
        self.axiom = axiom

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}("
            f"terminals={self.terminals!r}, "
            f"non_terminals={self.non_terminals!r}, "
            f"axiom={self.axiom!r}, "
            f"productions={self.productions!r})"
        )


    def compute_first(self, sentence: str) -> AbstractSet[str]:
        """
        Method to compute the first set of a string.

        Args:
            str: string whose first set is to be computed.

        Returns:
            First set of str.
        """

	# TODO: Complete this method for exercise 2...


    def compute_follow(self, symbol: str) -> AbstractSet[str]:
        """
        Method to compute the follow set of a non-terminal symbol.

        Args:
            symbol: non-terminal whose follow set is to be computed.

        Returns:
            Follow set of symbol.
        """

	# TO-DO: Complete this method for exercise 3...


    def get_ll1_table(self) -> Optional[LL1Table]:
        """
        Method to compute the LL(1) table.

        Returns:
            LL(1) table for the grammar, or None if the grammar is not LL(1).
        """

	# TO-DO: Complete this method for exercise 4...


    def is_ll1(self) -> bool:
        return self.get_ll1_table() is not None


class LL1Table:
    """
    LL1 table. Initially all cells are set to None (empty). Table cells
    must be filled by calling the method add_cell.

    Args:
        non_terminals: Set of non terminal symbols.
        terminals: Set of terminal symbols.

    """

    def __init__(
        self,
        non_terminals: AbstractSet[str],
        terminals: AbstractSet[str],
    ) -> None:

        if terminals & non_terminals:
            raise ValueError(
                "Intersection between terminals and non terminals "
                "must be empty.",
            )

        self.terminals: AbstractSet[str] = terminals
        self.non_terminals: AbstractSet[str] = non_terminals
        self.cells: Dict[str, Dict[str, Optional[str]]] = {nt: {t: None for t in terminals} for nt in non_terminals}

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}("
            f"terminals={self.terminals!r}, "
            f"non_terminals={self.non_terminals!r}, "
            f"cells={self.cells!r})"
        )

    def add_cell(self, non_terminal: str, terminal: str, cell_body: str) -> None:
        """
        Adds a cell to an LL(1) table.

        Args:
            non_terminal: Non termial symbol (row)
            terminal: Terminal symbol (column)
            cell_body: content of the cell 

        Raises:
            RepeatedCellError: if trying to add a cell already filled.
        """
        if non_terminal not in self.non_terminals:
            raise ValueError(
                "Trying to add cell for non terminal symbol not included "
                "in table.",
            )
        if terminal not in self.terminals:
            raise ValueError(
                "Trying to add cell for terminal symbol not included "
                "in table.",
            )
        if not all(x in self.terminals | self.non_terminals for x in cell_body):
            raise ValueError(
                "Trying to add cell whose body contains elements that are "
                "not either terminals nor non terminals.",
            )            
        if self.cells[non_terminal][terminal] is not None:
            raise RepeatedCellError(
                f"Repeated cell ({non_terminal}, {terminal}).")
        else:
            self.cells[non_terminal][terminal] = cell_body

    def analyze(self, input_string: str, start: str) -> ParseTree:
        """
        Method to analyze a string using the LL(1) table.

        Args:
            input_string: string to analyze.
            start: initial symbol.

        Returns:
            ParseTree object with either the parse tree (if the elective exercise is solved)
            or an empty tree (if the elective exercise is not considered).

        Raises:
            SyntaxError: if the input string is not syntactically correct.
        """

        """
        En este ejercicio se implementará el algoritmo e análisis sintáctico descendente
        LL(1) a partir de una tabla de análisis dada. Para ello es necesario completar el código
        del método analyze de la clase LL1Table en el fichero grammar.py. El método
        recibe la cadena a analizar, input_string, y el axioma o símbolo inicial, start.
        Debe devolver un árbol de derivación si la cadena es sintácticamente correcta de
        acuerdo con la tabla de análisis, o generar una excepción de tipo SyntaxError si
        no lo es.
        En el fichero test_analyze.py se facilitan algunos tests. Recordad no obstante
        que es vuestra responsabilidad realizar tests adicionales para comprobar que el
        código funciona de manera correcta.
        """
        i = 0
        # TODO: Complete this method for exercise 1...
        for elem in input_string:
            if elem not in self.terminals:
                raise SyntaxError("La cadena a analizar contiene terminales que no estan en la tabla LL1")
        stack = deque()
        end = ParseTree('$')
        stack.appendleft(end)
        tree = ParseTree(start)
        stack.appendleft(tree)

        while stack:
            element = stack.popleft()
            if element.root in self.non_terminals:
                print(f"Elemento popeado = {element.root}")
                print(f"Elemento del string = {input_string[i]}")
                next = self.cells[element.root][input_string[i]]
                print(f"Elemento de la tabla LL1 = {next}")
                if next is not None:
                    cld = []
                    if next != '': #El simbolo de la tabla es distinto de la cadena vacia
                        print(f"Se mete en pila {next}")
                        for e in next[::-1]: #Por cada simbolo se aniade a la pila y se crea un parse tree
                            
                            n_aux = ParseTree(e)
                            stack.appendleft(n_aux)
                            cld.append(n_aux)
                        print(f"Estado pila tras push = {stack}")
                    else: #El simbolo de la tabla es la cadena vacia
                        cld.append(ParseTree(next)) #Se crea un parse tree con la cadena vacia, sin meter en la pila
                    element.add_children(cld) #Se aniaden los hijos al elemento actual del arbol (simbolos o la cadena vacia)
                else:
                    print(f"No se ha encontrado entrada en la tabla para {element.root}, {input_string[i]}")

            elif element.root in self.terminals:
                if element.root != input_string[i]:
                    print(f"Elemento del string: {input_string[i]}")
                    print(f"Elemento de la pila: {element.root}")
                    print(f"Indice del string {i}")
                    print("ERROR: El elemento de la pila no coincide con el de la cadena")
                    print(f"Arbol fallido {tree}")
                    raise SyntaxError("xd") #NOTE: No se si esto funciona asi, revisar
                print(f"Elemento del string: {input_string[i]}")
                print(f"Elemento de la pila: {element.root}")
                print(f"TERMINAL: {input_string[i]}")
                i += 1
                
                if element.root == '$':
                    if i < len(input_string):
                        print("Error, hay elementos detras del simbolo \"$\" en la cadena")
                        #NOTE: Aqui debe salir excepcion ???
                        raise SyntaxError("xd") #NOTE: No se si esto funciona asi, revisar
                    print(f"Arbol final = {tree}")
                    return tree
            else:
                raise SyntaxError("xd")
    
class ParseTree():
    """
    Parse Tree.

    Args:
        root: root node of the tree.
        children: list of children, which are also ParseTree objects.
    """
    def __init__(self, root: str, children: Collection[ParseTree] = []) -> None:
        self.root = root
        self.children = children

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}({self.root!r}: {self.children})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return (
            self.root == other.root
            and len(self.children) == len(other.children)
            and all([x.__eq__(y) for x, y in zip(self.children, other.children)])
        )

    def add_children(self, children: Collection[ParseTree]) -> None:
        self.children = children
