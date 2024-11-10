import automaton, transitions, state, utils

initial_state = state.State("q0", False)

q0 = state.State("q0", False)
q1 = state.State("q1", False)
q2 = state.State("q2", True)
q3 = state.State("q3", False)
q4 = state.State("q4", True)
q5 = state.State("q5", False)
q6 = state.State("qcaca", False)

states = {q0, q1, q2, q3, q4, q5, q6}

transiciones = transitions.Transitions()
transiciones.add_transition(q0, "0", q1)
transiciones.add_transition(q0, "1", q1)
transiciones.add_transition(q1, "0", q2)
transiciones.add_transition(q1, "1", q2)
transiciones.add_transition(q2, "0", q3)
transiciones.add_transition(q2, "1", q3)
transiciones.add_transition(q3, "0", q4)
transiciones.add_transition(q3, "1", q4)
transiciones.add_transition(q4, "0", q5)
transiciones.add_transition(q4, "1", q5)
transiciones.add_transition(q5, "0", q0)
transiciones.add_transition(q5, "1", q0)
transiciones.add_transition(q6, "0", q1)
transiciones.add_transition(q6, "1", q2)
symbols = {0,1}

#NOTE test eliminacion de estados inaccesibles
a = automaton.FiniteAutomaton(q0, states, symbols, transiciones)
with open('automataog.dot', 'w') as fdot:
    fdot.write(utils.write_dot(a))

a1 = a.to_minimized() #Descomentar return de linea 306 de automaton
with open('automataminimized.dot', 'w') as fdot2:
    fdot2.write(utils.write_dot(a1))