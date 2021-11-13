Y = 0.5
STEP_COST = -20

class Transition:
    def __init__(self, source, action, dest, prob, reward):
        self.dest, self.prob, self.reward = dest, prob, reward
        self.source, self.action = source, action

class Action:
    def __init__(self, source, name, qvalue=0):
        self.qvalue = qvalue
        self.transitions = []
        self.source = source
        self.name = name

    def add_transition(self, dest, prob, reward=STEP_COST):
        temp = Transition(self.source, self.name, dest, prob, reward)
        self.transitions.append(temp)

class State:
    def __init__(self, name, value=0, repr = "", terminal=0):
        self.inf = 99999999
        self.actions = {}
        self.name = name
        self.repr = repr
        self.value = value
        self.terminal = terminal

    def add_action(self, action):
        self.actions.update({action.name : action})

