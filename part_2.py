from MDP import State, Action, Transition
import ValueIter

GAMMA = 0.999
HEALTH = [0, 25, 50, 75, 100]
DELTA = 1e-3

Y = 0
POSITIONS = ["W", "N", "E", "S", "C"]
STEP_COST = -20
NEGATIVE_REWARD = -40
MATERIALS = [0, 1, 2]
ARROWS = [0, 1, 2, 3]
MM = ["R", "D"]
states = {}
idx = 0 
ref = {}
ACTIONS = ["UP", "LEFT", "DOWN", "RIGHT", "STAY", "SHOOT", "HIT", "CRAFT", "GATHER", "NONE"]

# Add states
a_1 = 0
for p in POSITIONS:
    a_1 += 1
    a_2 = 0
    for m in MATERIALS:
        a_2 += 1
        a_3 = 0
        for a in ARROWS:
            a_3 += 1
            a_4 = 0
            for mm in MM:
                a_4 += 1
                for h in HEALTH:
                    state = (p, m, a, mm, h)
                    reward = 0

                    if h == 0:
                        reward = 50
                        temp = State(idx, reward, state, 1)
                        states[idx] = temp
                    else :
                        temp = State(idx, reward, state)
                        states[idx] = temp

                    ref[state] = idx 
                    idx = 1 + idx 

# Add actions 
a_1 = 0
for p in POSITIONS:
    a_1 += 1
    a_2 = 0
    for m in MATERIALS:
        a_2 += 1
        a_3 = 0
        for a in ARROWS:
            a_3 += 1
            a_4 = 0
            for mm in MM:
                a_4 += 1
                for h in HEALTH:

                    now = ref[(p, m, a, mm, h)]
                    cur = (p, m, a, mm, h)

                    if h == 0:
                        states[now].add_action(Action(now, ACTIONS[9]))
                        continue 

                    states[now].add_action(Action(now, ACTIONS[4]))

                    if p == POSITIONS[0]:
                        states[now].add_action(Action(now, ACTIONS[3]))
                        if a > 0:
                            states[now].add_action(Action(now, ACTIONS[5]))

                    elif p == POSITIONS[2]:
                        states[now].add_action(Action(now, ACTIONS[1]))

                        states[now].add_action(Action(now, ACTIONS[6]))
                        if a > 0:
                            states[now].add_action(Action(now, ACTIONS[5]))

                    elif p == POSITIONS[3]:
                        states[now].add_action(Action(now, ACTIONS[0]))
                        states[now].add_action(Action(now, ACTIONS[8]))

                    elif p == POSITIONS[4]:
                        states[now].add_action(Action(now, ACTIONS[0]))
                        states[now].add_action(Action(now, ACTIONS[3]))
                        states[now].add_action(Action(now, ACTIONS[2]))
                        states[now].add_action(Action(now, ACTIONS[1]))
                        
                        states[now].add_action(Action(now, ACTIONS[6]))
                        if a > 0:
                            states[now].add_action(Action(now, ACTIONS[5]))


                    elif p == POSITIONS[1]:
                        states[now].add_action(Action(now, ACTIONS[2]))
                        if m > 0:
                            states[now].add_action(Action(now, ACTIONS[7]))

# Add transitions
a_1 = 0
for p in POSITIONS:
    a_1 += 1
    a_2 = 0
    for m in MATERIALS:
        a_2 += 1
        a_3 = 0
        for a in ARROWS:
            a_3 += 1
            a_4 = 0
            for mm in MM:
                a_4 += 1
                for h in HEALTH:

                    now = ref[(p, m, a, mm, h)]
                    cur = (p, m, a, mm, h)

                    # Terminal 
                    if h == 0 :
                        states[now].actions[ACTIONS[9]].add_transition(now, 1, 0)
                        continue 

                    if p == POSITIONS[0]:
                        nxt = (POSITIONS[4], m, a, mm, h)
                        pos = ref[nxt] 

                        # states[now].actions[ACTIONS[4]].add_transition(now, 1)
                        # states[now].actions[ACTIONS[3]].add_transition(pos, 1)
                        

                        # if a > 0:
                        #     states[now].actions[ACTIONS[5]].add_transition(ref[(p, m, a - 1, mm, h - 25)], 0.25)
                        #     states[now].actions[ACTIONS[5]].add_transition(ref[(p, m, a - 1, mm, h)], 0.75)

                        if mm == MM[1]:
                            states[now].actions[ACTIONS[4]].add_transition(ref[(p, m, a, mm, h)], .8)
                            states[now].actions[ACTIONS[4]].add_transition(ref[(p, m, a, MM[0], h)], .2)
                            
                            states[now].actions[ACTIONS[3]].add_transition(ref[(POSITIONS[4], m, a, mm, h)], .8)
                            states[now].actions[ACTIONS[3]].add_transition(ref[(POSITIONS[4], m, a, MM[0], h)], .2)
                            
                            if a > 0:
                                states[now].actions[ACTIONS[5]].add_transition(ref[(p, m, a - 1, mm, h - 25)], 0.25 * .8)
                                states[now].actions[ACTIONS[5]].add_transition(ref[(p, m, a - 1, MM[0], h - 25)], 0.25 * .2)

                                states[now].actions[ACTIONS[5]].add_transition(ref[(p, m, a - 1, mm, h)], 0.75 * .8)
                                states[now].actions[ACTIONS[5]].add_transition(ref[(p, m, a - 1, MM[0], h)], 0.75 * .2)

                            
                        else:
                            states[now].actions[ACTIONS[4]].add_transition(ref[(p, m, a, mm, h)], .5)
                            states[now].actions[ACTIONS[4]].add_transition(ref[(p, m, a, MM[1], h)], .5)
                            
                            states[now].actions[ACTIONS[3]].add_transition(ref[(POSITIONS[4], m, a, mm, h)], .5)
                            states[now].actions[ACTIONS[3]].add_transition(ref[(POSITIONS[4], m, a, MM[1], h)], .5)
                            
                            if a > 0:
                                states[now].actions[ACTIONS[5]].add_transition(ref[(p, m, a - 1, mm, h - 25)], 0.25 * .5)
                                states[now].actions[ACTIONS[5]].add_transition(ref[(p, m, a - 1, MM[1], h - 25)], 0.25 * .5)

                                states[now].actions[ACTIONS[5]].add_transition(ref[(p, m, a - 1, mm, h)], 0.75 * .5)
                                states[now].actions[ACTIONS[5]].add_transition(ref[(p, m, a - 1, MM[1], h)], 0.75 * .5)

                    elif p == POSITIONS[2]:
                        if mm == MM[1] :
                            states[now].actions[ACTIONS[4]].add_transition(ref[(p, m, a, mm, h)], .8)
                            states[now].actions[ACTIONS[4]].add_transition(ref[(p, m, a, MM[0], h)], .2)
                            
                            states[now].actions[ACTIONS[1]].add_transition(ref[(POSITIONS[4], m, a, mm, h)], .8)
                            states[now].actions[ACTIONS[1]].add_transition(ref[(POSITIONS[4], m, a, MM[0], h)], .2)

                            max_val = max(0, h - 50)
                            mult = 0.2 * 0.8
                            states[now].actions[ACTIONS[6]].add_transition(ref[(p, m, a, mm, max_val)], mult)
                            states[now].actions[ACTIONS[6]].add_transition(ref[(p, m, a, MM[0], max(0, h - 50) )], 0.2 * .2)
                            
                            states[now].actions[ACTIONS[6]].add_transition(ref[(p, m, a, mm, h)], mult * 4)
                            states[now].actions[ACTIONS[6]].add_transition(ref[(p, m, a, MM[0], h)], mult)
                            
                            if a > 0:
                                states[now].actions[ACTIONS[5]].add_transition(ref[(p, m, a - 1, mm, h - 25)], 0.9 * .8)
                                states[now].actions[ACTIONS[5]].add_transition(ref[(p, m, a - 1, MM[0], h - 25)], 0.9 * .2)

                                states[now].actions[ACTIONS[5]].add_transition(ref[(p, m, a - 1, mm, h)], 0.1 * .8)
                                states[now].actions[ACTIONS[5]].add_transition(ref[(p, m, a - 1, MM[0], h)], 0.1 * .2)

                        else :
                            states[now].actions[ACTIONS[4]].add_transition(ref[(p, m, a, mm, h)], .5)
                            states[now].actions[ACTIONS[4]].add_transition(ref[(p, m, 0, MM[1], min(100, h + 25))], .5, STEP_COST + NEGATIVE_REWARD)
                            
                            states[now].actions[ACTIONS[1]].add_transition(ref[(POSITIONS[4], m, a, mm, h)], .5)
                            states[now].actions[ACTIONS[1]].add_transition(ref[(p, m, 0, MM[1], min(100, h + 25))], .5, STEP_COST + NEGATIVE_REWARD)

                            max_val = max(0, h - 50)
                            mult = 0.2 * 0.5
                            min_val = min(100, h + 25)
                            add = STEP_COST + NEGATIVE_REWARD
                            states[now].actions[ACTIONS[6]].add_transition(ref[(p, m, a, mm, max_val)], mult)
                            states[now].actions[ACTIONS[6]].add_transition(ref[(p, m, a, mm, h)], mult * 4)
                            states[now].actions[ACTIONS[6]].add_transition(ref[(p, m, 0, MM[1], min_val)], .5, add)
                            
                            
                            if a > 0:
                                states[now].actions[ACTIONS[5]].add_transition(ref[(p, m, a - 1, mm, h - 25)], 0.9 * .5)
                                states[now].actions[ACTIONS[5]].add_transition(ref[(p, m, a - 1, mm, h)], 0.1 * .5)
                                
                                states[now].actions[ACTIONS[5]].add_transition(ref[(p, m, 0, MM[1], min(100, h + 25))], .5, STEP_COST + NEGATIVE_REWARD)

                    elif p == POSITIONS[3]:
                        nxt = (POSITIONS[4], m, a, mm, h)
                        pos = ref[nxt] 

                        e = (POSITIONS[2], m, a, mm, h)
                        epos = ref[e] 
                        

                        # states[now].actions[ACTIONS[4]].add_transition(now, .85)
                        if mm == MM[1]:
                            states[now].actions[ACTIONS[4]].add_transition(ref[(p, m, a, mm, h)], .85 * .8)
                            states[now].actions[ACTIONS[4]].add_transition(ref[(p, m, a, MM[0], h)], .85 * .2)

                            states[now].actions[ACTIONS[4]].add_transition(ref[(POSITIONS[2], m, a, mm, h)], .15 * .8)
                            states[now].actions[ACTIONS[4]].add_transition(ref[(POSITIONS[2], m, a, MM[0], h)], .15 * .2)

                            # states[now].actions[ACTIONS[0]].add_transition(pos, .85)
                            states[now].actions[ACTIONS[0]].add_transition(ref[(POSITIONS[4], m, a, mm, h)], .85 * .8)
                            states[now].actions[ACTIONS[0]].add_transition(ref[(POSITIONS[4], m, a, MM[0], h)], .85 * .2)
                            
                            states[now].actions[ACTIONS[0]].add_transition(ref[(POSITIONS[2], m, a, mm, h)], .15 * .8)
                            states[now].actions[ACTIONS[0]].add_transition(ref[(POSITIONS[2], m, a, MM[0], h)], .15 * .2)
                            # states[now].actions[ACTIONS[0]].add_transition(epos, .15)

                            min_val = min(m + 1, 2)
                            mult = 0.75 * 0.2
                            states[now].actions[ACTIONS[8]].add_transition(ref[(p, min_val, a, mm, h)], mult * 4)
                            states[now].actions[ACTIONS[8]].add_transition(ref[(p, min_val, a, MM[0], h)], mult)
                            
                            states[now].actions[ACTIONS[8]].add_transition(ref[(p, m, a, mm, h)], .25 * .8)
                            states[now].actions[ACTIONS[8]].add_transition(ref[(p, m, a, MM[0], h)], .25 * .2)

                        else :
                            states[now].actions[ACTIONS[4]].add_transition(ref[(p, m, a, mm, h)], .5 * .8)
                            states[now].actions[ACTIONS[4]].add_transition(ref[(p, m, a, MM[1], h)], .5 * .2)

                            states[now].actions[ACTIONS[4]].add_transition(ref[(POSITIONS[2], m, a, mm, h)], .5 * .8)
                            states[now].actions[ACTIONS[4]].add_transition(ref[(POSITIONS[2], m, a, MM[1], h)], .5 * .2)

                            states[now].actions[ACTIONS[0]].add_transition(ref[(POSITIONS[4], m, a, mm, h)], .5 * .8)
                            states[now].actions[ACTIONS[0]].add_transition(ref[(POSITIONS[4], m, a, MM[1], h)], .5 * .2)
                            
                            states[now].actions[ACTIONS[0]].add_transition(ref[(POSITIONS[2], m, a, mm, h)], .5 * .8)
                            states[now].actions[ACTIONS[0]].add_transition(ref[(POSITIONS[2], m, a, MM[1], h)], .5 * .2)

                            min_val = min(m + 1, 2)
                            mult = 0.5 * 0.2
                            states[now].actions[ACTIONS[8]].add_transition(ref[(p, min_val, a, mm, h)], mult * 4)
                            states[now].actions[ACTIONS[8]].add_transition(ref[(p, min_val, a, MM[1], h)], mult)
                            
                            states[now].actions[ACTIONS[8]].add_transition(ref[(p, m, a, mm, h)], .5 * .8)
                            states[now].actions[ACTIONS[8]].add_transition(ref[(p, m, a, MM[1], h)], .5 * .2)

                    elif p == POSITIONS[4]:
                        if mm == MM[1] :
                            states[now].actions[ACTIONS[3]].add_transition(ref[(POSITIONS[2], m, a, mm, h)], .8)
                            states[now].actions[ACTIONS[3]].add_transition(ref[(POSITIONS[2], m, a, MM[0], h)], .2)

                            states[now].actions[ACTIONS[4]].add_transition(ref[(p, m, a, mm, h)], .85 * .8)
                            states[now].actions[ACTIONS[4]].add_transition(ref[(p, m, a, MM[0], h)], .85 * .2)
                            
                            states[now].actions[ACTIONS[4]].add_transition(ref[(POSITIONS[2], m, a, mm, h)], .15 * .8)
                            states[now].actions[ACTIONS[4]].add_transition(ref[(POSITIONS[2], m, a, MM[0], h)], .15 * .2)
                            
                            states[now].actions[ACTIONS[2]].add_transition(ref[(POSITIONS[3], m, a, mm, h)], .85 * .8)
                            states[now].actions[ACTIONS[2]].add_transition(ref[(POSITIONS[3], m, a, MM[0], h)], .85 * .2)
                            
                            states[now].actions[ACTIONS[2]].add_transition(ref[(POSITIONS[2], m, a, mm, h)], .15 * .8)
                            states[now].actions[ACTIONS[2]].add_transition(ref[(POSITIONS[2], m, a, MM[0], h)], .15 * .2)
                            
                            states[now].actions[ACTIONS[1]].add_transition(ref[(POSITIONS[0], m, a, mm, h)], .85 * .8)
                            states[now].actions[ACTIONS[1]].add_transition(ref[(POSITIONS[0], m, a, MM[0], h)], .85 * .2)
                            
                            states[now].actions[ACTIONS[1]].add_transition(ref[(POSITIONS[2], m, a, mm, h)], .15 * .8)
                            states[now].actions[ACTIONS[1]].add_transition(ref[(POSITIONS[2], m, a, MM[0], h)], .15 * .2)
                            
                            states[now].actions[ACTIONS[0]].add_transition(ref[(POSITIONS[1], m, a, mm, h)], .85 * .8)
                            states[now].actions[ACTIONS[0]].add_transition(ref[(POSITIONS[1], m, a, MM[0], h)], .85 * .2)
                            
                            states[now].actions[ACTIONS[0]].add_transition(ref[(POSITIONS[2], m, a, mm, h)], .15 * .8)
                            states[now].actions[ACTIONS[0]].add_transition(ref[(POSITIONS[2], m, a, MM[0], h)], .15 * .2)

                            max_val = max(0, h - 50)
                            mult = 0.1 * 0.2
                            states[now].actions[ACTIONS[6]].add_transition(ref[(p, m, a, mm, max_val)], mult * 4)
                            states[now].actions[ACTIONS[6]].add_transition(ref[(p, m, a, MM[0], max_val)], mult)
                            
                            mult = 0.9 * 0.2
                            states[now].actions[ACTIONS[6]].add_transition(ref[(p, m, a, mm, h)], mult * 4)
                            states[now].actions[ACTIONS[6]].add_transition(ref[(p, m, a, MM[0], h)], mult)
                            
                            if a > 0:
                                states[now].actions[ACTIONS[5]].add_transition(ref[(p, m, a - 1, mm, h - 25)], 0.5 * .8)
                                states[now].actions[ACTIONS[5]].add_transition(ref[(p, m, a - 1, MM[0], h - 25)], 0.5 * .2)

                                states[now].actions[ACTIONS[5]].add_transition(ref[(p, m, a - 1, mm, h)], 0.5 * .8)
                                states[now].actions[ACTIONS[5]].add_transition(ref[(p, m, a - 1, MM[0], h)], 0.5 * .2)

                        else :

                            states[now].actions[ACTIONS[4]].add_transition(ref[(p, m, a, mm, h)], .85 * .5)
                            states[now].actions[ACTIONS[4]].add_transition(ref[(POSITIONS[2], m, a, mm, h)], .15 * .5)
                            states[now].actions[ACTIONS[4]].add_transition(ref[(p, m, 0, MM[1], min(100, h + 25))], .5, STEP_COST + NEGATIVE_REWARD)
                            
                            states[now].actions[ACTIONS[1]].add_transition(ref[(POSITIONS[0], m, a, mm, h)], .85 * .5)
                            states[now].actions[ACTIONS[1]].add_transition(ref[(POSITIONS[2], m, a, mm, h)], .15 * .5)
                            states[now].actions[ACTIONS[1]].add_transition(ref[(p, m, 0, MM[1], min(100, h + 25))], .5, STEP_COST + NEGATIVE_REWARD)
                            
                            states[now].actions[ACTIONS[3]].add_transition(ref[(POSITIONS[2], m, a, mm, h)], .5)
                            states[now].actions[ACTIONS[3]].add_transition(ref[(p, m, 0, MM[1], min(100, h + 25))], .5, STEP_COST + NEGATIVE_REWARD)
                            
                            states[now].actions[ACTIONS[2]].add_transition(ref[(POSITIONS[3], m, a, mm, h)], .85 * .5)
                            states[now].actions[ACTIONS[2]].add_transition(ref[(POSITIONS[2], m, a, mm, h)], .15 * .5)
                            states[now].actions[ACTIONS[2]].add_transition(ref[(p, m, 0, MM[1], min(100, h + 25))], .5, STEP_COST + NEGATIVE_REWARD)


                            states[now].actions[ACTIONS[0]].add_transition(ref[(POSITIONS[1], m, a, mm, h)], .85 * .5)
                            states[now].actions[ACTIONS[0]].add_transition(ref[(POSITIONS[2], m, a, mm, h)], .15 * .5)
                            states[now].actions[ACTIONS[0]].add_transition(ref[(p, m, 0, MM[1], min(100, h + 25))], .5, STEP_COST + NEGATIVE_REWARD)

                            max_val = max(0, h - 50)
                            mult = 0.1 * 0.5
                            min_val = min(100, h + 25)
                            add = STEP_COST + NEGATIVE_REWARD
                            states[now].actions[ACTIONS[6]].add_transition(ref[(p, m, a, mm, max_val)], mult)
                            states[now].actions[ACTIONS[6]].add_transition(ref[(p, m, a, mm, h)], mult * 9)
                            states[now].actions[ACTIONS[6]].add_transition(ref[(p, m, 0, MM[1], min_val)], .5, add)
                            
                            
                            if a > 0:
                                states[now].actions[ACTIONS[5]].add_transition(ref[(p, m, a - 1, mm, h - 25)], 0.9 * .5)
                                states[now].actions[ACTIONS[5]].add_transition(ref[(p, m, a - 1, mm, h)], 0.1 * .5)
                                
                                states[now].actions[ACTIONS[5]].add_transition(ref[(p, m, 0, MM[1], min(100, h + 25))], .5, STEP_COST + NEGATIVE_REWARD)

                            


                    elif p == POSITIONS[1]:
                        nxt = (POSITIONS[4], m, a, mm, h)
                        pos = ref[nxt] 

                        e = (POSITIONS[2], m, a, mm, h)
                        epos = ref[e] 
                        
                        # states[now].actions[ACTIONS[4]].add_transition(now, .85)
                        # states[now].actions[ACTIONS[4]].add_transition(epos, .15)

                        # states[now].actions[ACTIONS[2]].add_transition(pos, .85)
                        # states[now].actions[ACTIONS[2]].add_transition(epos, .15)

                        # if m > 0:
                        #     states[now].actions[ACTIONS[7]].add_transition( ref[(p, m - 1, min(3, a + 1), mm, h)], 0.5)
                        #     states[now].actions[ACTIONS[7]].add_transition( ref[(p, m - 1, min(3, a + 2), mm, h)], 0.35)
                        #     states[now].actions[ACTIONS[7]].add_transition( ref[(p, m - 1, min(3, a + 3), mm, h)], 0.15)

                        if mm == MM[1]:
                            
                            states[now].actions[ACTIONS[4]].add_transition(ref[(p, m, a, mm, h)], .85 * .8)
                            states[now].actions[ACTIONS[4]].add_transition(ref[(p, m, a, MM[0], h)], .85 * .2)

                            states[now].actions[ACTIONS[4]].add_transition(ref[(POSITIONS[2], m, a, mm, h)], .15 * .8)
                            states[now].actions[ACTIONS[4]].add_transition(ref[(POSITIONS[2], m, a, MM[0], h)], .15 * .2)

                            # states[now].actions[ACTIONS[0]].add_transition(pos, .85)
                            states[now].actions[ACTIONS[2]].add_transition(ref[(POSITIONS[4], m, a, mm, h)], .85 * .8)
                            states[now].actions[ACTIONS[2]].add_transition(ref[(POSITIONS[4], m, a, MM[0], h)], .85 * .2)
                            
                            states[now].actions[ACTIONS[2]].add_transition(ref[(POSITIONS[2], m, a, mm, h)], .15 * .8)
                            states[now].actions[ACTIONS[2]].add_transition(ref[(POSITIONS[2], m, a, MM[0], h)], .15 * .2)

                            # states[now].actions[ACTIONS[4]].add_transition(now, .85)
                            # states[now].actions[ACTIONS[4]].add_transition(epos, .15)

                            # states[now].actions[ACTIONS[2]].add_transition(pos, .85)
                            # states[now].actions[ACTIONS[2]].add_transition(epos, .15)

                            if m > 0:
                                states[now].actions[ACTIONS[7]].add_transition( ref[(p, m - 1, min(3, a + 1), mm, h)], 0.5 * .8)
                                states[now].actions[ACTIONS[7]].add_transition( ref[(p, m - 1, min(3, a + 1), MM[0], h)], 0.5 * .2)

                                states[now].actions[ACTIONS[7]].add_transition( ref[(p, m - 1, min(3, a + 2), mm, h)], 0.35 * .8)
                                states[now].actions[ACTIONS[7]].add_transition( ref[(p, m - 1, min(3, a + 2), MM[0], h)], 0.35 * .2)

                                states[now].actions[ACTIONS[7]].add_transition( ref[(p, m - 1, min(3, a + 3), mm, h)], 0.15 * .8)
                                states[now].actions[ACTIONS[7]].add_transition( ref[(p, m - 1, min(3, a + 3), MM[0], h)], 0.15 * .2)

                        else :
                            
                            
                            states[now].actions[ACTIONS[4]].add_transition(ref[(p, m, a, mm, h)], .85 * .5)
                            states[now].actions[ACTIONS[4]].add_transition(ref[(p, m, a, MM[1], h)], .85 * .5)

                            states[now].actions[ACTIONS[4]].add_transition(ref[(POSITIONS[2], m, a, mm, h)], .15 * .5)
                            states[now].actions[ACTIONS[4]].add_transition(ref[(POSITIONS[2], m, a, MM[1], h)], .15 * .5)

                            # states[now].actions[ACTIONS[0]].add_transition(pos, .85)
                            states[now].actions[ACTIONS[2]].add_transition(ref[(POSITIONS[4], m, a, mm, h)], .85 * .5)
                            states[now].actions[ACTIONS[2]].add_transition(ref[(POSITIONS[4], m, a, MM[1], h)], .85 * .5)
                            
                            states[now].actions[ACTIONS[2]].add_transition(ref[(POSITIONS[2], m, a, mm, h)], .15 * .5)
                            states[now].actions[ACTIONS[2]].add_transition(ref[(POSITIONS[2], m, a, MM[1], h)], .15 * .5)
                            
                            # states[now].actions[ACTIONS[4]].add_transition(now, .85)
                            # states[now].actions[ACTIONS[4]].add_transition(epos, .15)

                            # states[now].actions[ACTIONS[2]].add_transition(pos, .85)
                            # states[now].actions[ACTIONS[2]].add_transition(epos, .15)

                            if m > 0:
                                states[now].actions[ACTIONS[7]].add_transition( ref[(p, m - 1, min(3, a + 1), mm, h)], 0.5 * .5)
                                states[now].actions[ACTIONS[7]].add_transition( ref[(p, m - 1, min(3, a + 1), MM[1], h)], 0.5 * .5)

                                states[now].actions[ACTIONS[7]].add_transition( ref[(p, m - 1, min(3, a + 2), mm, h)], 0.35 * .5)
                                states[now].actions[ACTIONS[7]].add_transition( ref[(p, m - 1, min(3, a + 2), MM[1], h)], 0.35 * .5)

                                states[now].actions[ACTIONS[7]].add_transition( ref[(p, m - 1, min(3, a + 3), mm, h)], 0.15 * .5)
                                states[now].actions[ACTIONS[7]].add_transition( ref[(p, m - 1, min(3, a + 3), MM[1], h)], 0.15 * .5)
                        
ValueIter.solve(states, GAMMA, DELTA, 0)