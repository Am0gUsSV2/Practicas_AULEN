"""
    Equipo docente de Autómatas y Lenguajes Curso 2024-25
    Última modificación: 26 de septiembre de 2024

    Implementación de un autómata. Para ello, se van a definir las siguientes clases:
        - State: Clase que define un estado del autómata.
        - Transitions: Clase que define el conjunto de transiciones del autómata.
        - FiniteAutomaton: Clase que define el autómata finito.
        - REParser: Clase que parsea de expresión regular a autómata
"""

from src.automaton import FiniteAutomaton
from src.state import State
from src.transitions import Transitions

def _re_to_rpn(re_string):
    """
    Convert re to reverse polish notation (RPN).

    Does not check that the input re is syntactically correct.

    Args:
        re_string: Regular expression in infix notation. Type: str

    Returns:
        Regular expression in reverse polish notation. Type: str

    """
    stack = [] # List of strings
    rpn_string = ""
    for x in re_string:
        if x == "+":
            while len(stack) > 0 and stack[-1] != "(":
                rpn_string += stack.pop()
            stack.append(x)
        elif x == ".":
            while len(stack) > 0 and stack[-1] == ".":
                rpn_string += stack.pop()
            stack.append(x)
        elif x == "(":
            stack.append(x)
        elif x == ")":
            while stack[-1] != "(":
                rpn_string += stack.pop()
            stack.pop()
        else:
            rpn_string += x

    while len(stack) > 0:
        rpn_string += stack.pop()

    return rpn_string



class REParser():
    """Class for processing regular expressions in Kleene's syntax."""
    
    def __init__(self) -> None:
        self.state_counter = 0

    def _create_automaton_empty(self):
        """
            Crea un 
        Create an automaton that accepts the empty language.

        Returns:
            Automaton that accepts the empty language. Type: FiniteAutomaton

        """
        #---------------------------------------------------------------------
        # TODO: Implement this method...
        #---------------------------------------------------------------------
        initial_state = State("q" + str(self.state_counter)) # Se crea el estado inicial del nuevo automata
        self.state_counter += 1
        final_state = State("q" + str(self.state_counter), True) # Se crea el estado final del nuevo automata
        self.state_counter += 1
        states = {initial_state, final_state}
        return FiniteAutomaton(initial_state, states, {}, None)

    def _create_automaton_lambda(self):
        """
        Create an automaton that accepts the empty string.

        Returns:
            Automaton that accepts the empty string. Type: FiniteAutomaton

        """
        #---------------------------------------------------------------------
        # TODO: Implement this method...
        #---------------------------------------------------------------------
        unique_state = State("q" + str(self.state_counter)) # Se crea el estado inicial del nuevo automata
        self.state_counter += 1
        transitions = Transitions() # Se crea el objeto Transitions, inicialmente vacio
        transitions.add_transition(unique_state, "", unique_state) #Se aniade la transicion lambda al objeto transitions
        return FiniteAutomaton(unique_state, {unique_state}, {""}, transitions) # Se crea el automata

    def _create_automaton_symbol(self, symbol):
        """
        Create an automaton that accepts one symbol.

        Args:
            symbol: Symbol that the automaton should accept. Type: str

        Returns:
            Automaton that accepts a symbol. Type: FiniteAutomaton

        """
        #---------------------------------------------------------------------
        # TODO: Implement this method...
        #---------------------------------------------------------------------
        initial_state = State("q" + str(self.state_counter)) # Se crea el estado inicial del nuevo automata
        self.state_counter += 1
        final_state = State("q" + str(self.state_counter), True) # Se crea el estado final del nuevo automata
        self.state_counter += 1
        transitions = Transitions() # Se crea el objeto Transitions, inicialmente vacio
        transitions.add_transition(initial_state, symbol, final_state) #Se aniade la transicion symbol al objeto transitions
        return FiniteAutomaton(initial_state, {initial_state, final_state}, {symbol}, transitions) # Se crea el automata

    def _create_automaton_star(self, automaton):
        """
        Create an automaton that accepts the Kleene star of another.

        Args:
            automaton: Automaton whose Kleene star must be computed. Type: FiniteAutomaton

        Returns:
            Automaton that accepts the Kleene star. Type: FiniteAutomaton

        """
        #---------------------------------------------------------------------
        # TODO: Implement this method...
        #---------------------------------------------------------------------
        initial_state = State("q" + str(self.state_counter)) # Se crea el estado inicial del nuevo automata
        self.state_counter += 1
        final_state = State("q" + str(self.state_counter), True) # Se crea el estado final del nuevo automata
        self.state_counter += 1
        og_initial_state = automaton.get_initial_state() #Se obtiene el estado inicial del automata original
        og_final_state = automaton.get_final_state() # Se obtiene el estado final del automata original
        og_transitions = automaton.get_object_transitions() # Se obtienen todas las transiciones del automata original
        og_symbols = automaton.get_all_symbols() # Se obtienen el conjunto de todos los simbolos del automata original
        og_states = automaton.get_all_states() # Se obtienen el conjunto de todos los estados del automata original

        #meter simbolo lambda en el conjunto de simbolos si esta no se encuentra en el set
        if None not in og_symbols:
            og_symbols.add(None)
        #transicion lambda del inicial al og inicial
        og_transitions.add_transition(initial_state, None, og_initial_state)
        #transicion lambda del og final al og inicial
        og_transitions.add_transition(og_final_state, None, og_initial_state)
        #transicion lambda del og final al final
        og_transitions.add_transition(og_final_state, None, final_state)
        #transicion lambda del inicial al final
        og_transitions.add_transition(initial_state, None, final_state)
        #quitar status de final a og final en estado y en conjunto
        og_final_state.set_final(False)

        #aniadir los estados nuevos inicial y final al conjunto de estados del automata
        og_states.add(initial_state)
        og_states.add(final_state)

        return FiniteAutomaton(initial_state, og_states, og_symbols, og_transitions) # Se crea el automata

    def _create_automaton_union(self, automaton1, automaton2):
        """
        Create an automaton that accepts the union of two automata.

        Args:
            automaton1: First automaton of the union. Type: FiniteAutomaton.
            automaton2: Second automaton of the union. Type: FiniteAutomaton.

        Returns:
            Automaton that accepts the union. Type: FiniteAutomaton.

        """
        #---------------------------------------------------------------------
        # TODO: Implement this method...
        #---------------------------------------------------------------------
        initial_state = State("q" + str(self.state_counter)) # Se crea el estado inicial del nuevo automata
        self.state_counter += 1
        final_state = State("q" + str(self.state_counter), True) # Se crea el estado final del nuevo automata
        self.state_counter += 1

        og_initial_state_1 = automaton1.get_initial_state() #Se obtiene el estado inicial del automata original
        og_final_state_1 = automaton1.get_final_state() # Se obtiene el estado final del automata original
        og_transitions_1 = automaton1.get_object_transitions() # Se obtienen todas las transiciones del automata original
        og_symbols_1 = automaton1.get_all_symbols() # Se obtienen el conjunto de todos los simbolos del automata original
        og_states_1 = automaton1.get_all_states() # Se obtienen el conjunto de todos los estados del automata original

        og_initial_state_2 = automaton2.get_initial_state() #Se obtiene el estado inicial del automata original
        og_final_state_2 = automaton2.get_final_state() # Se obtiene el estado final del automata original
        og_transitions_2 = automaton2.get_object_transitions() # Se obtienen todas las transiciones del automata original
        og_symbols_2 = automaton2.get_all_symbols() # Se obtienen el conjunto de todos los simbolos del automata original
        og_states_2 = automaton2.get_all_states() # Se obtienen el conjunto de todos los estados del automata original

        #Unir transiciones de ambos automatas
        og_transitions_1.add_transitions(og_transitions_2.get_all_transitions())
        og_transitions = og_transitions_1

        #Union de conjuntos de los simbolos de ambos automatas
        og_symbols = og_symbols_1.union(og_symbols_2)

        #Union de conjuntos de los estados de ambos automatas
        og_states = og_states_1.union(og_states_2)

        #meter simbolo lambda en el conjunto de simbolos si esta no se encuentra en el set
        if None not in og_symbols:
            og_symbols.add(None)

        #transicion lambda del inicial al og inicial 1
        og_transitions.add_transition(initial_state, None, og_initial_state_1)
        #transicion lambda del inicial al og inicial 2
        og_transitions.add_transition(initial_state, None, og_initial_state_2)

        #quitar status de final a og final en estado y en conjunto
        og_final_state_1.set_final(False)
        og_final_state_2.set_final(False)

        #transicion lambda del final 1 al final
        og_transitions.add_transition(og_final_state_1, None, final_state)
        #transicion lambda del final 2 al final
        og_transitions.add_transition(og_final_state_2, None, final_state)

        #aniadir los estados nuevos inicial y final al conjunto de estados del automata
        og_states.add(initial_state)
        og_states.add(final_state)

        return FiniteAutomaton(initial_state, og_states, og_symbols, og_transitions) # Se crea el automata

    def _create_automaton_concat(self, automaton1, automaton2):
        """
        Create an automaton that accepts the concatenation of two automata.

        Args:
            automaton1: First automaton of the concatenation. Type: FiniteAutomaton.
            automaton2: Second automaton of the concatenation. Type: FiniteAutomaton.

        Returns:
            Automaton that accepts the concatenation. Type: FiniteAutomaton.

        """
        #---------------------------------------------------------------------
        # TODO: Implement this method...
        #---------------------------------------------------------------------
        og_initial_state_1 = automaton1.get_initial_state() #Se obtiene el estado inicial del automata original
        og_final_state_1 = automaton1.get_final_state() # Se obtiene el estado final del automata original
        og_transitions_1 = automaton1.get_object_transitions() # Se obtienen todas las transiciones del automata original
        og_symbols_1 = automaton1.get_all_symbols() # Se obtienen el conjunto de todos los simbolos del automata original
        og_states_1 = automaton1.get_all_states() # Se obtienen el conjunto de todos los estados del automata original

        og_initial_state_2 = automaton2.get_initial_state() #Se obtiene el estado inicial del automata original
        og_transitions_2 = automaton2.get_object_transitions() # Se obtienen todas las transiciones del automata original
        og_symbols_2 = automaton2.get_all_symbols() # Se obtienen el conjunto de todos los simbolos del automata original
        og_states_2 = automaton2.get_all_states() # Se obtienen el conjunto de todos los estados del automata original

        #Unir transiciones de ambos automatas
        og_transitions_1.add_transitions(og_transitions_2.get_all_transitions())
        og_transitions = og_transitions_1

        #Union de conjuntos de los simbolos de ambos automatas
        og_symbols = og_symbols_1.union(og_symbols_2)

        #Union de conjuntos de los estados de ambos automatas
        og_states = og_states_1.union(og_states_2)

        #meter simbolo lambda en el conjunto de simbolos si esta no se encuentra en el set
        if None not in og_symbols:
            og_symbols.add(None)

        #quitar status de final a og final de 1 en estado y en conjunto
        og_final_state_1.is_final = False

        #transicion lambda del final 1 al final
        og_transitions.add_transition(og_final_state_1, None, og_initial_state_2)

        return FiniteAutomaton(og_initial_state_1, og_states, og_symbols, og_transitions) # Se crea el automata

    def create_automaton(
        self,
        re_string,
    ):
        """
        Create an automaton from a regex.

        Args:
            re_string: String with the regular expression in Kleene notation. Type: str

        Returns:
            Automaton equivalent to the regex. Type: FiniteAutomaton

        """
        if not re_string:
            return self._create_automaton_empty()
        
        rpn_string = _re_to_rpn(re_string)

        stack = [] # list of FiniteAutomatons

        self.state_counter = 0
        for x in rpn_string:
            if x == "*":
                aut = stack.pop()
                stack.append(self._create_automaton_star(aut))
            elif x == "+":
                aut2 = stack.pop()
                aut1 = stack.pop()
                stack.append(self._create_automaton_union(aut1, aut2))
            elif x == ".":
                aut2 = stack.pop()
                aut1 = stack.pop()
                stack.append(self._create_automaton_concat(aut1, aut2))
            elif x == "λ":
                stack.append(self._create_automaton_lambda())
            else:
                stack.append(self._create_automaton_symbol(x))

        return stack.pop()
