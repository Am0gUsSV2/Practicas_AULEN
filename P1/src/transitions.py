"""
    Equipo docente de Autómatas y Lenguajes Curso 2024-25
    Última modificación: 26 de septiembre de 2024

    Implementación de un autómata. Para ello, se van a definir las siguientes clases:
        - State: Clase que define un estado del autómata.
        - Transitions: Clase que define el conjunto de transiciones del autómata.
        - FiniteAutomaton: Clase que define el autómata finito.
        - REParser: Clase que parsea de expresión regular a autómata.
"""

from state import State

class Transitions():
    """
    Define el conjunto de transiciones de un autómata. Contiene exclusivamente un
      diccionario de transiciones y el conjunto de métodos para trabajar con ellas.

    Ejemplo:
        {
            q1: {'a': {q1, q2}, 'lambda':{q3}}
            q2: {'a': {q3}, }
            q3: {'lambda':{q1}, 'b':{q2}}
        }

    Observación: Un estado puede ir a varios estados con un mismo símbolo. En el
      ejemplo anterior, de q1 con el símbolo 'a' se puede ir a q1 y a q2.
    """

    def __init__(self):
        self.transitions = {}


    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented

        return self.transitions == other.transitions


    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"{[f'{key}:{self.transitions[key]}' for key in self.transitions.keys()]})"
        )

    def state_get_all_states_from(self, state: State):
        lista = []
        simbolos_transiciones = self.transitions.get(state) #Se obtienen los simbolos y a que estados transicionan
        claves = simbolos_transiciones.keys() #Se obtienen los simbolos que se usan para transicionar
        for clave in claves:
            estados = simbolos_transiciones.get(clave) #Se obtienen los estados dado el simbolo
            for estado in estados:
                lista.append(estado) #Se aniade cada estado a la lista
        return lista



    def state_has_transitions(self, state: State):
        """
            Esta función comprueba si hay alguna transición desde el estado state.
                state -- [?] --> ?

            Args:
                state: estado inicial de la transición

            Returns:
                True si hay alguna transición
                False otherwise
        """

        #NOTE: Status = Implemented, not tested
        ret = self.transitions.get(state)
        if ret is not False:
            return True
        return False


    def state_get_symbols(self, state: State):
        """
            Esta función devuelve los símbolos con los que se puede transitar desde
              el estado state.

            Args:
                state: estado de la transición

            Returns:
                Lista con los símbolos con los que se puede transitar
                None en caso de no haber ningún símbolo

            Observación:
                Recomendable usar la función state_has_transitions
        """
        #NOTE: Status = implemented, not tested
        if self.state_has_transitions(state):
            dict_state = self.transitions.get(state) #Esto deberia devolver el valor de la clave state (que es otro diccionario con claves simbolos y valor estados a donde se puede transicionar)
            if dict_state is None:
                return None
            return list(dict_state.keys()) #Esto deberia devolver la lista con claves (que son los simbolos con los cuales se puede transicionar a otros estados)
        return None


    def state_has_any_transition_with_symbol(self, state: State, symbol: str):
        """
            Esta función comprueba si hay alguna transición desde el estado state
              con el símbolo symbol
                existe state -- [symbol] --> ?

            Args:
                state: estado inicial de la transición
                symbol: símbolo de la transición

            Returns:
                True si hay alguna transición con el símbolo
                False otherwise

            Observación:
                - Recomendable usar la función state_has_transitions
        """
        #NOTE: Status = Implemented, not tested

        symbols = self.state_get_symbols(state) #Esta funcion ya llama a state_has_transitions
        if symbols is None:
            return False
        if symbol in symbols:
            return True
        return False


    def goes_to(self, state: State, symbol: str):
        """
            Esta función devuelve los estados a los que se transita desde el estado
              state con el símbolo symbol

            Args:
                state: estado inicial de la transición
                symbol: símbolo de la transición

            Returns:
                Set de estados a los que se transita. Ejemplo: {q1, q2}
                None en caso de no existir

            Observación:
                - Recomendable usar la función state_has_any_transition_with_symbol
        """
        #NOTE: Status = Implemented, not tested
        if self.state_has_any_transition_with_symbol(state, symbol):
            return self.transitions.get(state).get(symbol)
        return None
    

    def state_has_transition_to(self, start_state: State, symbol: str, end_state: State):
        """
            Esta función comprueba si hay alguna transición desde el estado start_state
              con el símbolo symbol al estado end_state
                existe start_state -- [symbol] --> end_state

            Args:
                start_state: estado inicial de la transición
                symbol: símbolo de la transición
                end_state: estado final de la transición

            Returns:
                True si existe la transición
                False otherwise

            Observación:
                - Recomendable usar la función state_has_any_transition_with_symbol
        """
        #NOTE: Status = Implemented, not tested
        if self.state_has_any_transition_with_symbol(start_state, symbol):
            states = self.goes_to(start_state, symbol)
            if end_state in states:
                return True
                
        return False

        
    def add_transition(self, start_state: State, symbol: str, end_state: State):
        """
            Esta función añade una transición desde el estado start_state con el símbolo
              symbol al estado end_state en caso de no existir previamente.
                start_state -- [symbol] --> end_state

            Args:
                start_state: estado inicial de la transición
                symbol: símbolo de la transición
                end_state: estado final de la transición
            Returns: No return
            Raise Exception:
                - ValueError si la transición ya existe

            Observación:
                - Recomendable usar las funciones:
                    state_has_transition_to
                    state_has_any_transition_with_symbol
                    state_has_transitions
        """

        if self.state_has_transition_to(start_state, symbol, end_state):
            raise ValueError("Repeated transition for state '%s'"%start_state)

        #NOTE: Status = Implemented, not tested
        if start_state not in self.transitions:
            self.transitions[start_state] = {} #Crea una nueva clave con valor vacio
        
        if self.state_has_any_transition_with_symbol(start_state, symbol) == False:
            self.transitions[start_state][symbol] = set() #Crea un conjunto de estados en caso de que no haya transiciones desde el estado inicial con el simbolo dado
        
        self.transitions[start_state][symbol].add(end_state) #Aniade el estado final partiendo del estado inicial y el simbolo con el que se transita
            
            
    def add_transitions(self, transitions: list):
        """
            Esta función añade un conjunto de transiciones a la vez

            Args:
                transitions: lista de transiciones en formato tupla (start, symbol, end)
            Returns: No return
        """
        for (start_state, symbol, end_state) in transitions:
            self.add_transition(start_state, symbol, end_state)
        
    
    def get_all_transitions(self):
        """
            Esta función devuelve todas las transiciones en formato lista de tuplas 
              (start, symbol, end)

            Returns:
                Lista de tuplas (start, symbol, end)
        """
        all_transitions = []

        for start_state in self.transitions:
            for symbol in self.transitions[start_state]:
                for end_state in self.transitions[start_state][symbol]:
                    all_transitions.append((start_state, symbol, end_state))
        
        return all_transitions


    def get_lambda_transitions(self):
        """
            Esta función devuelve un diccionario con todas las transiciones lambda
              start_state -- [lambda] --> end_states
            en un formato simplificado
              start_state --> end_states

            Args: No args

            Return:
                Diccionario de transiciones con lambda.
                  Clave: estado de inicio de transición
                  Valor: set de estados destino

            Observación:
                - El símbolo lambda se representa con None
        """
        lambda_transitions = {}

        for start_state in self.transitions:
            if self.state_has_any_transition_with_symbol(start_state, None):
                end_states = self.goes_to(start_state, None)
                lambda_transitions[start_state] = end_states

        return lambda_transitions
