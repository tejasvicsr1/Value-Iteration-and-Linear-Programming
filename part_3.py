import json
import cvxpy
from values import *
import numpy as np

rewards = []
sa_pair_cnt = 0
state_action_pair_list = []

number_of_states = NUM_POS * MAX_MAT * MAX_ARROWS * NUM_MM_STATE * MAX_HEALTH
r2d = 0.5
max_number_of_actions = number_of_states * len(ACTIONS)

d2r = 0.2
a_matrix = np.zeros((number_of_states, max_number_of_actions), dtype=float)

def getHash(state_arr):
    # [pos, mat, arrows, state, health]
    for i in range(num_parameters):
        state_arr[i] = max(min(state_arr[i], state_max[i]), 0)
    shash = 0
    for i, state_val in enumerate(state_arr):
        val = int(state_val * np.prod(state_max[i + 1:]))
        shash += val
    return shash

state_tuple = (number_of_states, 1)
alpha = np.zeros(state_tuple)
alpha[getHash([maxx - 1 for maxx in state_max])] = 1

def add_state_action(state_arr, action, extra_reward=0):
    state_action_pair_list.append((state_arr, ACTIONS[action]))
    global sa_pair_cnt

    if action != 0:
        rewards.append(STEP_COST + extra_reward)
    else:
        rewards.append(0 + extra_reward)

    sa_pair_cnt = 1 + sa_pair_cnt


def update_a_matrix(state_arr, shash, prob):
    new_hash = getHash(state_arr)
    global sa_pair_cnt

    if new_hash == shash:
        pass
    else:
        a_matrix[new_hash][sa_pair_cnt] -= prob
        a_matrix[shash][sa_pair_cnt] += prob

def get_dual(state_arr):
    state_arr[3] -= 1
    state_arr[3] *= -1
    return state_arr

def apply_action(new_states, state_arr, hit_probs, action_number):
    shash = getHash(state_arr)
    pos, num_mat, num_arr, mm_state, mm_health = state_arr
    # new_states_dual = [get_dual(new_state) for new_state in new_states]
    new_states_dual = []
    for new_state in new_states:
        new_states_dual.append(get_dual(new_state))
    
    if mm_state == 0:
        statelength = len(new_states)
        for i in range(statelength):
            probability_1 = hit_probs[i] * (1 - d2r)
            update_a_matrix(new_states[i], shash, probability_1)
            probability_1 = hit_probs[i] * d2r
            update_a_matrix(new_states_dual[i], shash, probability_1)
        add_state_action(state_arr,action_number)

    elif mm_state == 1:
        statelength = len(new_states)
        for i in range(statelength):
            probability_1 = hit_probs[i] * (1 - r2d)
            update_a_matrix(new_states[i], shash, probability_1)

        if pos == 2 or pos == 4:
            update_a_matrix([pos, num_mat, 0, 0, mm_health + 1], shash, r2d)
            probability_1 = mm_hit * 0.5
            add_state_action(state_arr, action_number, probability_1)
        else:
            statelength = len(new_states)
            for i in range(statelength):
                probability_1 = hit_probs[i] * (1 - r2d)
                update_a_matrix(new_states_dual[i], shash, probability_1)
            add_state_action(state_arr, action_number)


def gather(state_arr):
    action_number = 9
    pos, num_mat, num_arr, mm_state, mm_health = state_arr
    hit_prob = 0.75
    
    if pos != 3:
        return
    states = [state_arr, [pos, num_mat + 1, num_arr, mm_state, mm_health]]
    hit_probs = [1 - hit_prob, hit_prob]
    apply_action(states, state_arr, hit_probs, action_number)

def craft(state_arr):
    action_number = 8
    pos, num_mat, num_arr, mm_state, mm_health = state_arr
    hit_prob = [.5,.35,.15]
    # hit_prob = [0,0,0]

    if pos != 1 or num_mat==0:
        return

    state_1 = [pos, num_mat - 1, num_arr + 1, mm_state, mm_health]
    state_2 = [pos, num_mat - 1, num_arr + 2, mm_state, mm_health]
    state_3 = [pos, num_mat - 1, num_arr + 3, mm_state, mm_health]
    states = [state_1, state_2, state_3]
    apply_action(states, state_arr, hit_prob, action_number)
    

def hit(state_arr):
    action_number = 7
    pos, num_mat, num_arr, mm_state, mm_health = state_arr

    hit_prob = 0.2 if pos == 2 else 0.1


    if pos in [0, 1, 3]:
        return

    states = [state_arr, [pos, num_mat, num_arr, mm_state, mm_health - 2]]
    apply_action(states, state_arr, [1 - hit_prob, hit_prob], action_number)
    

def shoot(state_arr):
    action_number = 6
    pos, num_mat, num_arr, mm_state, mm_health = state_arr
    hit_prob = 0.25 if pos == 0 else 0.9 if pos == 2 else 0.5

    if num_arr == 0 or pos in [1, 3]:
        return

    state_1 = [pos, num_mat, num_arr - 1, mm_state, mm_health]
    state_2 = [pos, num_mat, num_arr - 1, mm_state, mm_health - 1]
    states = [state_1, state_2]
    apply_action(states, state_arr, [1 - hit_prob, hit_prob], action_number)

def stay(state_arr):
    action_number = 5
    pos, num_mat, num_arr, mm_state, mm_health = state_arr

    hit_prob = 1.0 if pos in [0,2] else 0.85

    state_1 = [2, num_mat, num_arr, mm_state, mm_health]
    state_2 = [pos, num_mat, num_arr, mm_state, mm_health]
    states = [state_1, state_2]
    apply_action(states, state_arr, [1 - hit_prob, hit_prob], action_number)

def right(state_arr):
    action_number = 4
    pos, num_mat, num_arr, mm_state, mm_health = state_arr

    if pos == 0 or pos == 2:
        hit_prob = 1.0
    else:
        hit_prob = 0.85

    if pos not in [0,4]:
        return

    state_1 = [2, num_mat, num_arr, mm_state, mm_health]
    state_2 = [4 if pos == 0 else 2, num_mat, num_arr, mm_state, mm_health]
    states = [state_1, state_2]
    apply_action(states, state_arr, [1 - hit_prob, hit_prob], action_number)

def down(state_arr):
    action_number = 3
    pos, num_mat, num_arr, mm_state, mm_health = state_arr

    hit_prob = 1.0 if pos in [0,2] else 0.85

    if pos not in [1,4]:
        return

    state_1 = [2, num_mat, num_arr, mm_state, mm_health]
    state_2 = [4 if pos == 1 else 3, num_mat, num_arr, mm_state, mm_health]
    states = [state_1, state_2]
    apply_action(states, state_arr, [1 - hit_prob, hit_prob], action_number)

def left(state_arr):
    action_number = 2
    pos, num_mat, num_arr, mm_state, mm_health = state_arr

    hit_prob = 1.0 if pos in [0,2] else 0.85

    if pos not in [2,4]:
        return

    state_1 = [2, num_mat, num_arr, mm_state, mm_health]
    state_2 = [4 if pos == 2 else 0, num_mat, num_arr, mm_state, mm_health]
    states = [state_1, state_2]
    apply_action(states, state_arr, [1 - hit_prob, hit_prob], action_number)

def up(state_arr):
    action_number = 1
    pos, num_mat, num_arr, mm_state, mm_health = state_arr
    hit_prob = 1.0 if pos in [0,2] else 0.85

    if pos not in [3,4]:
        return

    state_1 = [2, num_mat, num_arr, mm_state, mm_health]
    state_2 = [4 if pos == 3 else 1, num_mat, num_arr, mm_state, mm_health]
    states = [state_1, state_2]
    apply_action(states, state_arr, [1 - hit_prob, hit_prob], action_number)

positions = range(state_max[0])
mats = range(state_max[1])
shoots = range(state_max[2])
states = range(state_max[3])
healths = range(state_max[4])

for pos in positions:
    for mat in mats:
        for arrows in shoots:
            for state in states:
                for health in healths:
                    shash = getHash([pos, mat, arrows, state, health])
                    state_arr = [pos, mat, arrows, state, health]
                    if health == 0: 
                        a_matrix[shash][sa_pair_cnt] = 1
                        add_state_action([pos, mat, arrows, state, health], 0)
                    else:
                        shoot(state_arr)
                        hit(state_arr)
                        gather(state_arr)
                        craft(state_arr)
                        stay(state_arr)
                        right(state_arr)
                        left(state_arr)
                        up(state_arr)
                        down(state_arr)

policy = {}
final_answer = {}
rewards = np.array(rewards)
a_matrix = a_matrix[:, :sa_pair_cnt]
cnt_tuple = (sa_pair_cnt, 1)

x = cvxpy.Variable(shape=cnt_tuple, name="x")
constraints = [a_matrix@x == alpha, x >= 0]
rw = rewards.T @ x
objective = cvxpy.Maximize(rw)
solution = cvxpy.Problem(objective,constraints).solve()
x = x.value.tolist()

for number, val in enumerate(state_action_pair_list):
    state, action = val
    if getHash(state) not in policy.keys():
        policy[getHash(state)] = (x[number], [state, action])
        
    else:
        policyarray = policy[getHash(state)]
        if x[number] > policyarray[0]:
            policy[getHash(state)] = (x[number], [state, action])

a = a_matrix.tolist()
b = rewards.tolist()
c = alpha.tolist()

final_answer['a'] = a
final_answer['r'] = b
final_answer['alpha'] = c
final_answer['x'] = x
final_answer['policy'] = [v[1] for k, v in policy.items()]
final_answer['objective'] = solution

# with open("outputs/policy",'w+') as f:
#     for state,action in [v[1] for k, v in policy.items()]:
#         print("[pos: {}, mat: {}, arrows: {}, state: {}, health: {}]".format(*state),action,file=f)

# with open("outputs/part_3_output.json", "w+") as f:
#     json.dump(final_answer, f, indent=2)

print(final_objective)