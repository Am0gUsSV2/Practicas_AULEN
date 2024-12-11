from __future__ import annotations

from collections import deque
from typing import AbstractSet, Collection, MutableSet, Optional, Dict, List, Optional
from pprint import pprint

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
        self.first_sets = {symbol: set() for symbol in non_terminals}
        self.follow_sets = {symbol: set() for symbol in non_terminals}
        self.first_sets_calculated = False

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}("
            f"terminals={self.terminals!r}, "
            f"non_terminals={self.non_terminals!r}, "
            f"axiom={self.axiom!r}, "
            f"productions={self.productions!r})"
        )

    def compute_all_first_sets(self):
        """
        Calcula todos los conjuntos First para los no terminales de la gramática de manera iterativa.

        Este método asegura que cada conjunto First se actualiza adecuadamente hasta que no haya más cambios.
        """
        changes = True

        while changes:
            changes = False
            for non_terminal in self.non_terminals:
                current_first_set = self.first_sets[non_terminal].copy()

                # Iteramos sobre las producciones del no terminal
                for production in self.productions[non_terminal]:
                    empty_production = True  # Se asume inicialmente que la producción puede derivar en ""

                    for symbol in production:
                        if symbol in self.terminals:
                            # Si el símbolo es terminal, lo añadimos al conjunto First
                            self.first_sets[non_terminal].add(symbol)
                            empty_production = False  # La producción no puede ser vacía
                            break  # Dejamos de procesar esta producción
                        elif symbol in self.non_terminals:
                            # Si el símbolo es un no terminal, actualizamos el conjunto First
                            self.first_sets[non_terminal].update(self.first_sets[symbol] - {""})
                            # Si el no terminal puede derivar en "", seguimos evaluando el siguiente símbolo
                            if "" not in self.first_sets[symbol]:
                                empty_production = False
                                break
                        else:
                            raise ValueError(f"Símbolo no válido en producción: {symbol}")

                    # Si la producción tiene solo no terminales que pueden derivar en "", añadimos ""
                    if empty_production:
                        self.first_sets[non_terminal].add("")

                # Si hubo un cambio en el conjunto First del no terminal, repetimos el proceso
                if self.first_sets[non_terminal] != current_first_set:
                    changes = True

        # Marcamos como calculados los conjuntos First
        self.first_sets_calculated = True

    def compute_first(self, sentence: str) -> set[str]:
        """
        Método para calcular el conjunto First de una cadena específica.

        Args:
            sentence: Cadena cuya conjunto First se va a calcular.

        Returns:
            Conjunto First de la cadena.
        """
        # Calculamos todos los conjuntos First si no están calculados
        if not self.first_sets_calculated:
            self.compute_all_first_sets()

        first_set = set()

        # Procesamos la cadena símbolo por símbolo
        for symbol in sentence:
            if symbol in self.terminals:
                # Si el símbolo es terminal, lo añadimos al conjunto First
                first_set.add(symbol)
                break  # Una vez que añadimos el terminal, no necesitamos más símbolos
            elif symbol in self.non_terminals:
                # Si el símbolo es un no terminal, actualizamos el conjunto First con los de ese no terminal
                first_set.update(self.first_sets[symbol] - {""})

                # Si el conjunto First de este no terminal no contiene "", dejamos de procesar
                if "" not in self.first_sets[symbol]:
                    break
            else:
                raise ValueError(f"Símbolo no válido en producción: {symbol}")

        # Si llegamos al final de la cadena y no hemos encontrado ningún terminal ni no terminal
        # que termine el conjunto (es decir, toda la cadena puede derivar en lambda),
        # añadimos el conjunto lambda al conjunto First.
        if all(symbol in self.non_terminals and "" in self.first_sets[symbol] for symbol in sentence):
            first_set.add("")

        return first_set




	# TODO: Complete this method for exercise 2...


    def compute_follow(self, symbol: str) -> AbstractSet[str]:
        """
        Computes the follow set of a specific non-terminal symbol iteratively.

        Args:
            symbol: Non-terminal whose follow set is to be computed.

        Returns:
            Follow set of the symbol.
        """
        if symbol not in self.non_terminals:
            raise ValueError(f"Symbol '{symbol}' must be a non-terminal.")

        # Inicializar los conjuntos Follow de todos los no terminales
        for non_terminal in self.non_terminals:
            if non_terminal not in self.follow_sets:
                self.follow_sets[non_terminal] = set()

        # Regla 1: Follow del axioma incluye "$"
        self.follow_sets[self.axiom].add("$")

        changed = True
        while changed:
            changed = False

            # Iterar sobre cada producción
            for head, productions in self.productions.items():
                for production in productions:
                    # Propagar Follow(head)
                    follow_to_propagate = self.follow_sets[head]

                    for i in range(len(production)):
                        sym = production[i]

                        if sym in self.non_terminals:  # Sólo no terminales tienen Follow
                            # Regla 2: Añadir First(B) - {λ} a Follow(sym)
                            if i + 1 < len(production):
                                next_symbol = production[i + 1:]
                                first_of_next = self.compute_first(next_symbol)

                                before = len(self.follow_sets[sym])
                                self.follow_sets[sym].update(first_of_next - {""})
                                after = len(self.follow_sets[sym])
                                if after > before:
                                    changed = True

                            # Regla 3: Propagar Follow(head) si es el último símbolo
                            # o si First(B) contiene λ
                            if i + 1 == len(production) or "" in self.compute_first(production[i + 1:]):
                                before = len(self.follow_sets[sym])
                                self.follow_sets[sym].update(follow_to_propagate)
                                after = len(self.follow_sets[sym])
                                if after > before:
                                    changed = True

        return self.follow_sets[symbol]



	# TO-DO: Complete this method for exercise 3...


    def get_ll1_table(self) -> Optional[LL1Table]:
        """
        Método para calcular la tabla LL(1).

        Returns:
            La tabla LL(1) de la gramática, o None si la gramática no es LL(1).
        """
        table = LL1Table(self.non_terminals, self.terminals | {'$'})
        
        # Recorremos todas las producciones para construir la tabla LL(1)
        for non_terminal, productions in self.productions.items():
            for production in productions:
                # Calculamos el conjunto First de la producción
                first_set = self.compute_first(production)
                
                for terminal in first_set - {""}:
                    if terminal != "":  # Terminal válido
                        if table.cells[non_terminal][terminal] is None:
                            table.add_cell(non_terminal, terminal, production)
                        else:
                            # Conflicto: la gramática no es LL(1)
                            return None
                
                # Si la producción puede derivar a vacío, añadimos Follow
                if "" in first_set:
                    follow_set = self.compute_follow(non_terminal)
                    for terminal in follow_set:
                        if table.cells[non_terminal][terminal] is None:
                            table.add_cell(non_terminal, terminal, production)
                        else:
                            # Conflicto: la gramática no es LL(1)
                            return None
        

        return table

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
                next = self.cells.get(element.root, {}).get(input_string[i], None)
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
