import sys 
from MDP import State, Action, Transition

def state_print(states, iter=-1):
    if iter != -1:
        print("Iteration: " + str(iter))
        # print(f"Iteration: {iter}")
    for state in states.values():
        print(state.name, state.value)
    dashes = "-" * 10
    print(dashes)

def solve(states, y, e, printer=0):
    iter = 0
    INF = 1e15
    while True:
        if iter>200:
            quote = "Hard break"
            print(quote)
            break

        if printer != 0:
            state_print(states, iter)

        updates = {}
        max_change = 0

        for state in states.values():
            best_action = [-INF, None]

            if state.terminal == 1: continue

            for action in state.actions.values():
                
                action.qvalue = 0
                for transition in action.transitions:
                    temp = y*states[transition.dest].value + transition.reward
                    action.qvalue +=  transition.prob * (temp)

                if iter == 0: 
                    print(str(state.name) + " " + str(action.name) + " " + str(transition.dest) + " " + str(action.qvalue))
                pos_value = action.qvalue -  best_action[0]
                if pos_value > 0:
                    temp = [action.qvalue, action]
                    best_action = temp
            
            updates.update({state.name: best_action})

        for name, best_action in updates.items():
            value = best_action[0]
            
            if best_action[1] is None:
                continue

            change = abs(value - states[name].value)
            pos_value = change - max_change
            if pos_value > 0:
                max_change = change
            states[name].value = value

        if max_change < e:
            og = sys.stdout
            file_name = "outputs/part_2_trace.txt"
            sys.stdout = open(file_name, "w")

            print("Stopping: Delta = " + str(max_change))
            print("Last Iteration: " + str(iter + 1))

            for state in states.values():
                action_name = "End"
                temp = state.terminal
                if temp == 0:
                    temp = updates[state.name][1].name
                    action_name = temp
                print(str(state.repr) + " " + str(state.value) + " " + str(action_name))
            
            dashes = "-" * 10
            print(dashes)

            sys.stdout = og
            break

        iter += 1

    return states