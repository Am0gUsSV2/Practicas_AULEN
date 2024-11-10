import automaton, transitions, state, utils

q0 = state.State("q0", False)
q1 = state.State("q1", True)
q2 = state.State("q2", False)
q3 = state.State("q3", True)
q4 = state.State("q4", False)

states = {q0, q1, q2, q3, q4}

transiciones = transitions.Transitions()
transiciones.add_transition(q0, "a", q1)
transiciones.add_transition(q0, "b", q3)
transiciones.add_transition(q1, "a", q2)
transiciones.add_transition(q1, "b", q1)
transiciones.add_transition(q2, "a", q1)
transiciones.add_transition(q2, "b", q2)
transiciones.add_transition(q3, "a", q4)
transiciones.add_transition(q3, "b", q3)
transiciones.add_transition(q4, "a", q3)
transiciones.add_transition(q4, "b", q4)
symbols = {"a","b"}

#NOTE test eliminacion de estados inaccesibles
a = automaton.FiniteAutomaton(q0, states, symbols, transiciones)
with open('automataog.dot', 'w') as fdot:
    fdot.write(utils.write_dot(a))

a1 = a.to_minimized() #Descomentar return de linea 306 de automaton
print(a1)
with open('automataminimized.dot', 'w') as fdot2:
    fdot2.write(utils.write_dot(a1))