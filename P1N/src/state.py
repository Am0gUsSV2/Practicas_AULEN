"""
    Equipo docente de Autómatas y Lenguajes Curso 2024-25
    Última modificación: 26 de septiembre de 2024

    Implementación de un autómata. Para ello, se van a definir las siguientes clases:
        - State: Clase que define un estado del autómata.
        - Transitions: Clase que define el conjunto de transiciones del autómata.
        - FiniteAutomaton: Clase que define el autómata finito.
        - REParser: Clase que parsea de expresión regular a autómata.
"""

class State():
    """
        Define un estado del autómata. Este está definido por un nombre y si
        es estado de aceptación (final) o no.
    """

    def __init__(self, name: str, is_final = False):
        self.name = name
        self.is_final = is_final

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented

        return self.name == other.name and self.is_final == other.is_final

    def __repr__(self):
        return f"{type(self).__name__}({self.name!r}, is_final={self.is_final!r})"

    def __hash__(self):
        return hash(self.name)
    
    def is_final_state(self):
        return self.is_final
    
    def set_final(self, status):
        self.is_final = status