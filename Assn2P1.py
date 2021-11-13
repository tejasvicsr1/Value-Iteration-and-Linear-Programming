from headers import *
#Add states
states = {}
letters = ["A", "B", "C"]
places = ["rt", "dn", "up", "lt"]

states[letters[0]] = State(letters[0])
states[letters[1]] = State(letters[1])
states[letters[2]] = State(letters[2])
states["R"] = State("R", reward, 1)

#Add actions
states[letters[0]].add_action(Action(letters[0], places[0]))
states[letters[2]].add_action(Action(letters[2], places[1]))
states[letters[0]].add_action(Action(letters[0], places[2]))
states[letters[2]].add_action(Action(letters[2], places[0]))
states[letters[1]].add_action(Action(letters[1], places[3]))
states[letters[1]].add_action(Action(letters[1], places[2]))

#Add transitions A
states[letters[0]].actions[places[0]].add_transition(letters[1], 0.8, -1)
states[letters[0]].actions[places[0]].add_transition(letters[0], 0.2, -1)
states[letters[0]].actions[places[2]].add_transition(letters[2], 0.8, -1)
states[letters[0]].actions[places[2]].add_transition(letters[0], 0.2, -1)

#Add transitions B
states[letters[1]].actions[places[3]].add_transition(letters[0], 0.8, -1)
states[letters[1]].actions[places[3]].add_transition(letters[1], 0.2, -1)
states[letters[1]].actions[places[2]].add_transition("R", 0.8, -4)
states[letters[1]].actions[places[2]].add_transition(letters[1], 0.2, -1)

#Add transitions C
states[letters[2]].actions[places[0]].add_transition("R", 0.25, -3)
states[letters[2]].actions[places[0]].add_transition(letters[2], 0.75, -1)
states[letters[2]].actions[places[1]].add_transition(letters[0], 0.8, -1)
states[letters[2]].actions[places[1]].add_transition(letters[2], 0.2, -1)

for transition in states[letters[0]].actions[places[0]].transitions:
    print(transition.source, transition.action, transition.dest)

ValueIter.solve(states, y, e, 1)