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
from transitions import Transitions
from utils import is_deterministic
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
    
    def get_initial_state(self):
        return self.initial_state
    
    def get_final_state(self):
        for state in self.states:
            if state.is_final_state():
                return state
    
    def get_all_states(self):
        return self.states #devuelve el conjunto de estados del automata
    
    def get_all_symbols(self):
        return self.symbols # Devuelve el conjunto de simbolos del automata
        


    # END Funciones relacionadas con las transiciones


    # BEGIN Funciones relacionadas con el procesamiento de una cadena

    def reset(self):
        """
            Esta función resetea el autómata, volviendo al estado inicial

            Args: No args

            Returns: No return
        """
        current_states = {self.initial_state}
        self.current_states = self._complete_lambdas(current_states) #clausura lamda

    def process_symbol(self, symbol: str):
        """
            Esta función procesa un símbolo

            Args:
                symbol: símbolo a consumir

            Returns: No return
        """
        #------------------------------------------------
        # TO-DO por el estudiante
        # for state in self.current_states...
        
        new_states = set()
            
        # Iterar sobre los estados actuales
        for state in self.current_states:
            new_s = self.transitions.goes_to(state, symbol)
            if new_s:
                new_states.update(new_s)
            
        # Si se encontraron nuevos estados, actualizar los estados actuales
        if new_states:
            self.current_states = self._complete_lambdas(new_states)
        else:
            self.current_states = set()

            
        #-------------------------------------------------


    def accepts(self, string: str):
        """
        Esta función procesa una cadena y comprueba si debe ser aceptada
        o no.

        Args:
            string: cadena a procesar

        Returns:
            True si la cadena debe ser aceptada
            False en caso contrario
        """
        self.reset()
        for symbol in string:
            self.process_symbol(symbol)
            
            if not self.current_states:
                print("Cadena no válida: " + string)
                return False
        
        # Verificar si alguno de los estados actuales es un estado final
        for state in self.current_states:
            if state.is_final:  # Comprueba si es un estado final
                return True
        return False


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
        transciones = self.transitions.get_lambda_transitions()
        
        new_states = set(raw_current_states)
        
        queue = deque(raw_current_states)
        
        while queue:
            state = queue.popleft()
            
            for next_state in transciones.get(state, set()):
                if next_state not in new_states:
                    new_states.add(next_state)
                    queue.append(next_state)
        
        return new_states
        #----------------------------------------------

    # END Funciones relacionadas con el procesamiento de una cadena


    # BEGIN Funciones relacionadas con generar el AFD

    def to_deterministic(self):
        self.reset()
        
        dfa_symbols = set(self.symbols) - {None}
        initial_state = self.current_states
        initial_state_name = ','.join(sorted(state.name for state in initial_state))
        dfa_transitions = Transitions()       
        dfa_states = set()
        processed_states = {}
        empty = State('empty', is_final=False)
        
        
        es_final = any(s.is_final for s in initial_state)
        dfa_initial_state = State(initial_state_name, es_final)
        dfa_states.add(dfa_initial_state)
        processed_states[initial_state_name] = dfa_initial_state
        queue = deque([initial_state])
        
        while queue:
            current_state = queue.popleft()
            current_state_name = ','.join(sorted(state.name for state in current_state))
            dfa_state = processed_states[current_state_name]
            
            for symbol in dfa_symbols:
                self.current_states = current_state
                self.process_symbol(symbol)
                
                new_s_with_clausura = self.current_states
                new_s_name = ','.join(sorted(state.name for state in new_s_with_clausura))
                
                if not new_s_with_clausura:
                    new_dfa_state = empty
                    new_s_with_clausura = {empty}
                else:
                    if new_s_name not in processed_states:
                        es_final = any(s.is_final for s in new_s_with_clausura)
                        new_dfa_state = State(new_s_name, es_final)
                        dfa_states.add(new_dfa_state)
                        processed_states[new_s_name] = new_dfa_state
                        queue.append(new_s_with_clausura)
                    else:
                        new_dfa_state = processed_states[new_s_name]

                # Añadir la transición
                if not dfa_transitions.state_has_any_transition_with_symbol(dfa_state, symbol):
                    dfa_transitions.add_transition(dfa_state, symbol, new_dfa_state)

        # Asegurarse de que empty tiene transiciones a sí mismo
        for symbol in dfa_symbols:
            if not dfa_transitions.state_has_any_transition_with_symbol(empty, symbol):
                dfa_transitions.add_transition(empty, symbol, empty)
                
        

        dfa_states.add(empty)

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
        flag = 0

        #-------------------------------------------------
        # TO-DO por el estudiante

        #-------------------------------------------------
        #TODO:
        #   1- Eliminar estados inaccesibles mediante BFS
        #BFS
        cola = deque()
        estados_visitables = set()
        cola.append(self.initial_state)
        #state = cola.popleft() #para extraer el primer elemento de la cola
        while cola:
            estado_actual = cola.popleft()
            estados_encontrados = self.transitions.state_get_all_states_from(estado_actual)
            for estado in estados_encontrados:
                if estado not in estados_visitables:
                    estados_visitables.add(estado)
                    cola.append(estado)
        estados_inalcanzables = self.states.difference(estados_visitables)

        #Se eliminan los estados inalcanzables del conjunto de estados del automata y del diccionario de transiciones
        for estado in estados_inalcanzables:
            self.states.remove(estado)
            del self.transitions.transitions[estado] #NOTE

        #NOTE La eliminacion de estados inaccesibles funciona bien (Probado en notebook)
        #return FiniteAutomaton(self.initial_state, self.states, self.symbols, self.transitions)
        
        # 2- Clases de equivalencia
        dict1 = {}
        dict2 = {}

        #Primera iteracion
        for state in self.states:
            if state.is_final_state() is True:
                dict1[state] = 1
            else:
                dict1[state] = 0
            dict2[state] = None

        counter = len(self.states)
        flag = False
        #og_state : State
        iteration = 0
        print("Transiciones:")
        print(self.transitions)
        print("")
        while flag is False:
            eq_class = 0
            i = 0
            while i < counter:
                first_eq = 1
                for state in self.states: 
                    if dict2[state] == None: #No tiene clase de equivalencia asignada
                        if first_eq > 0:
                            dict2[state] = eq_class
                            first_eq -= 1
                            og_state = state
                            i += 1
                        else:
                            if dict1[state] == dict1[og_state]: #Es equivalente a A en la iteracion anterior
                                flag2 = True
                                for symbol in self.symbols:
                                    if flag2 is True:
                                        xs1 = (self.transitions.transitions[state][str(symbol)])
                                        xs2 = (self.transitions.transitions[og_state][str(symbol)])
                                        val1= dict1[next(iter(xs1))]
                                        val2 = dict1[next(iter(xs2))]
                                        if val1 != val2:
                                            flag2 = False
                                if flag2 is True:#self.transit_to_same_eq_class(dict1, dict2, og_state, state): #NOTE
                                    dict2[state] = eq_class
                                    i += 1
                eq_class += 1

            flag = dicts_are_equal(dict1, dict2)
            print(f"Iteracion completa numero {iteration} ")
            print("Dict1:")
            print(dict1)
            print("Dict2:")
            print(dict2)
            print("")
            
            if flag is False:
                for state in self.states:
                    dict1[state] = dict2[state]
                    dict2[state] = None
            iteration += 1

        
        dict_inv = {}
        for k, v in dict1.items():
            if v not in dict_inv:
                dict_inv[v] = []
            dict_inv[v].append(k)

        """
        {
        0: ['q0', 'q1']
        1: ['q2', 'q3']
        }
        
        """
        print("Resultado de diccionarios iguales:")
        print(dict1)
        print(dict2)
        dfam_states = set()
        dfam_initial_state : State
        dfam_symbols = self.symbols
        dfam_transitions = Transitions()

        dict_transitions = {}
        #Se crean los nuevos estados
        for key in dict_inv:
            is_final = False
            is_initial = False
            for state in dict_inv[key]:
                if state.is_final_state():
                    is_final = True
                if state.__eq__(self.initial_state):
                    is_initial = True
            name = get_set_name(dict_inv[key])
            if is_initial is True:
                dfam_initial_state = State(name, is_final)
                dfam_states.add(dfam_initial_state)
                dict_transitions[dfam_initial_state] = dict_inv[key]
            else:
                aux_state = State(name, is_final)
                dfam_states.add(aux_state)
                dict_transitions[aux_state] = dict_inv[key]
          

        #TODO Crear las nuevas transiciones
        used_states = set()

        for state in self.states:
            if state not in used_states:
                for start_state in dfam_states:
                    if state in dict_transitions[start_state]:
                        for symbol in self.symbols:
                            state_to_transit = self.transitions.goes_to(state, symbol)
                            for end_state in dfam_states:
                                if state_to_transit in dict_transitions[end_state]:
                                    dfam_transitions.add_transition(start_state, symbol, end_state)
                                    for u_state in dict_transitions[start_state]:
                                        used_states.add(u_state)
                                    
        
        return FiniteAutomaton(dfam_initial_state, dfam_states, dfam_symbols, dfam_transitions)
    
    def transit_to_same_eq_class(self, dict1 : dict, dict2 : dict, og_state : State, current_state : State) -> bool: #NOTE
    
        for symbol in self.symbols:
            val1= dict1[(self.transitions.goes_to(og_state, symbol)).pop()]
            val2 = dict1[(self.transitions.goes_to(current_state, symbol)).pop()]
            if val1 != val2:
                return False
        return True
    # END Funciones relacionadas con minimizar el AFD

def get_set_name(state_set):
    return ','.join(sorted(state.name for state in state_set))
    
def has_set_a_final_state(state_set):
    return any(state.is_final for state in state_set)

def dicts_are_equal(dict1 : dict, dict2 : dict) -> bool:
    states = dict1.keys()
    for state in states:
        if dict1[state] != dict2[state]:
            return False
    return True