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
        self.first_sets = {symbol: set() for symbol in terminals | non_terminals}
        self.follow_sets = {symbol: set() for symbol in terminals | non_terminals}

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
        Calcula el conjunto First.

        Args:
            sentence: Secuencia de símbolos para la que se calculará el conjunto First.

        Returns:
            Conjunto First de la secuencia.
        """
        work_stack = [sentence]  # Pila para procesar las sentences
        computed_first = set()   # Conjunto First calculado para la sentence actual
        
        while work_stack:
            current_sentence = work_stack.pop()
            temp_first = set()

            for symbol in current_sentence:
                if symbol in self.terminals:
                    temp_first.add(symbol)
                    break  # Un terminal define el First y se detiene aquí
                elif symbol in self.non_terminals:
                    # Calculamos si el First del no terminal aún no está calculado
                    if not self.first_sets[symbol]:
                        # Agregamos todas sus producciones al stack para calcularlas iterativamente
                        for production in self.productions[symbol]:
                            work_stack.append(production)
                    temp_first.update(self.first_sets[symbol] - {""})

                    if "" not in self.first_sets[symbol]:
                        break  # No hay epsilon, se detiene aquí
                else:
                    raise ValueError(f"Símbolo no válido en la sentence: {symbol}")
            else:
                # Si llegamos aquí, significa que todos los símbolos tienen ε en su First
                temp_first.add("")

            # Guardamos el conjunto temporal calculado
            computed_first.update(temp_first)
            
            # Actualizamos el First almacenado para la sentence si cambia
            if sentence not in self.first_sets or self.first_sets[sentence] != computed_first:
                self.first_sets[sentence] = computed_first

        return computed_first

	# TODO: Complete this method for exercise 2...


    def compute_follow(self, symbol: str) -> AbstractSet[str]:
        """
        Method to compute the follow set of a non-terminal symbol.

        Args:
            symbol: non-terminal whose follow set is to be computed.

        Returns:
            Follow set of symbol.
        """
        #NOTE:Status = Implemented. Test = Not tested 
        if symbol not in self.non_terminals:
                raise ValueError(f"El simbolo {symbol} no pertenece al conjunto de simbolos no terminales de la gramatica")
        
        abs_set1 = {}
        abs_set2 = {}
        flag = True
        while flag:
            for key in self.productions.keys():
                production = self.productions[key]
                len_prod = len(production)
                for i in range(len_prod):
                    if production[i] == symbol:
                        if (i == (len_prod - 1)) or ('λ' in self.compute_first(production[i+1])): #No tiene mas elementos detras suya
                            abs_set2.add(self.compute_follow(key))
                        else:
                            elem = self.compute_first(production[i+1])
                            elem.remove('λ')
                            abs_set2.add(elem)
            if(abs_set1 != abs_set2):
                abs_set1 = abs_set2.copy()

        return abs_set2   
        
        

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
        for elem in input_string:
            if elem not in self.terminals:
                raise SyntaxError("La cadena a analizar contiene terminales que no estan en la tabla LL1")
        stack = []
        end = ParseTree('$')
        stack.append(end)
        tree = ParseTree(start)
        stack.append(tree)
        len_string = len(input_string)

        while stack and i <len_string:
            element = stack.pop()
            if element.root in self.non_terminals:
                next = self.cells[element.root][input_string[i]]
                if next is not None:
                    cld = []
                    if next != '': #El simbolo de la tabla es distinto de la cadena vacia
                        for e in next[::-1]: #Por cada simbolo se aniade a la pila y se crea un parse tree
                            n_aux = ParseTree(e)
                            stack.append(n_aux)
                            cld.append(n_aux)
                    else: #El simbolo de la tabla es la cadena vacia
                        cld.append(ParseTree('λ')) #Se crea un parse tree con la cadena vacia, sin meter en la pila
                    element.add_children(cld[::-1]) #Se aniaden los hijos al elemento actual del arbol (simbolos o la cadena vacia)
                else:
                    raise SyntaxError(f"No se ha encontrado entrada en la tabla para {element.root}, {input_string[i]}")

            elif element.root in self.terminals:
                if element.root != input_string[i]:
                    raise SyntaxError("El elemento terminal de la pila no coincide con el elemento del string")
                i += 1
                
                if element.root == '$':
                    if i < len(input_string):
                        raise SyntaxError("Hay elementos detras del simbolo \"$\" en la cadena")
                    return tree
            else:
                raise SyntaxError(f"{element.root} no pertenece ni a la lista de simbolos terminales ni a la de no terminales")
        raise SyntaxError("Se ha terminado de recorrer el string y la pila no esta vacía")
    
    
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
