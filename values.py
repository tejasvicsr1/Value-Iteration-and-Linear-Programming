import numpy as np

# [W - 0, N - 1, E - 2, S - 3, C - 4]

NUM_POS = 5
MAX_MAT = 3
MAX_ARROWS = 4
NUM_MM_STATE = 2
MAX_HEALTH = 5

state_max = [5, 3, 4, 2, 5]
num_parameters = 5

STEP_COST = -10
mm_hit = -40

ACTIONS = ["NONE", "UP", "LEFT", "DOWN", "RIGHT", "STAY", "SHOOT", "HIT", "CRAFT", "GATHER"]

POS_MAP = ['W', 'N', 'E', 'S', 'C']
MM_STATE_MAP = ['D', 'R']
final_objective = -466.888986934673