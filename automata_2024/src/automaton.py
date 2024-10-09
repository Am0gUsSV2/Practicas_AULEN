"""
    Equipo docente de Autómatas y Lenguajes Curso 2024-25
    Última modificación: 26 de septiembre de 2024

    Implementación de un autómata. Para ello, se van a definir las siguientes clases:
        - State: Clase que define un estado del autómata.
        - Transitions: Clase que define el conjunto de transiciones del autómata.
        - FiniteAutomaton: Clase que define el autómata finito.
        - REParser: Clase que parsea de expresión regular a autómata.
"""

from src.state import State
from src.transitions import Transitions
from src.utils import is_deterministic
from collections import deque

class FiniteAutomaton():
    """
        Define un autómata finito.
    """

    def __init__(self, initial_state: State, states: set, symbols: set, transitions: Transitions):

        if initial_state not in states:
            raise ValueError(
                f"Initial state {initial_state.name} "
                f"is not in the set of states",
            )

        self.initial_state = initial_state
        self.states = states
        self.symbols = symbols
        self.transitions = transitions
        

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented

        return (
            self.initial_state == other.initial_state
            and self.states == other.states
            and self.symbols == other.symbols
            and self.transitions == other.transitions
        )

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"initial_state={self.initial_state!r}, "
            f"states={self.states!r}, "
            f"symbols={self.symbols!r}, "
            f"transitions={self.transitions!r})"
        )

    # BEGIN Funciones relacionadas con las transiciones

    def add_transition(self, start_state: State, symbol: str, end_state: State):
        self.transitions.add_transition(start_state, symbol, end_state)
        
    def add_transitions(self, transitions: list):
        self.transitions.add_transitions(transitions)

    def has_transition(self, state: State, symbol: str):
        return self.transitions.state_has_any_transition_with_symbol(state, symbol)
        
    def get_transition(self, state: State, symbol: str):
        return self.transitions.goes_to(state, symbol)
        
    def get_all_transitions(self):
        return self.transitions.get_all_transitions()

    # END Funciones relacionadas con las transiciones


    # BEGIN Funciones relacionadas con el procesamiento de una cadena

    def reset(self):
        """
            Esta función resetea el autómata, volviendo al estado inicial

            Args: No args

            Returns: No return
        """
        current_states = {self.initial_state}
        self.current_states = self._complete_lambdas(current_states)

    def process_symbol(self, symbol: str):
        """
            Esta función procesa un símbolo

            Args:
                symbol: símbolo a consumir

            Returns: No return
        """
        #------------------------------------------------
        # TO-DO por el estudiante
        
        #-------------------------------------------------


    def accepts(self, string: str):
        """
            Esta función procesa una cadena y comprueba si debe ser aceptada
              o no.

            Args:
                string: cadena a procesar

            Returns:
                True si la cadena debe ser aceptada
                False otherwise
        """
        #--------------------------------------------------
        # TO-DO por el estudiante
        
        #--------------------------------------------------


    def _complete_lambdas(self, raw_current_states: set):
        """
            Esta función añade al conjunto de estados actuales todos aquellos
              estados que pueden ser alcanzados con el símbolo lambda.

            Args:
                raw_current_states: conjunto de estados actuales al que hay
                  que añadir todos aquellos estados a los que se puede transitar
                  con el símbolo lambda

            Return:
                Conjunto de estados actualizado

            Observación:
                - Recomendable utilizar el método get_lambda_transitions de Transitions
                
        """
        #----------------------------------------------
        # TO-DO por el estudiante

        #----------------------------------------------

    # END Funciones relacionadas con el procesamiento de una cadena


    # BEGIN Funciones relacionadas con generar el AFD

    def to_deterministic(self):
        """
            Esta función construye un Autómata Finito Determinista a partir del
              automata original.

            Args: No args

            Return:
                Un autómata finito determinista
        """
        #--------------------------------------------------
        # TO-DO por el estudiante

        #--------------------------------------------------
        return FiniteAutomaton(dfa_initial_state, dfa_states, dfa_symbols, dfa_transitions)

    # END Funciones relacionadas con generar el AFD

    # BEGIN Funciones relacionadas con minimizar el AFD

    def to_minimized(self):
        """
            Esta función minimiza un Autómata Finito Determinista"

            Args: No args

            Return:
                Un autómata finito determinista mínimo
        """
        if not is_deterministic(self):
            raise ValueError("The automaton must be deterministic")

        #-------------------------------------------------
        # TO-DO por el estudiante

        #-------------------------------------------------
        return FiniteAutomaton(dfam_initial_state, dfam_states, dfam_symbols, dfam_transitions)
    
    # END Funciones relacionadas con minimizar el AFD
