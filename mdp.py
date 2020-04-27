import numpy as np

# The MDP problem is a stochastic shortest path problem


def main():
    # Example: Machine Maintenance Problem
    # Goal: Maximize profit
    # States: {B = broken machine, W = working machine}
    # Action space: A(B) = {R = repair, P = replace}
    #               A(W) = {N = do nothing, M = do maintenance}
    # Profit: In one week, running machine -> $100 profit
    #                      failed machine -> $0 profit
    # Costs: Repair Cost = $40
    #        Replacement Cost = $150

    # transitions[state][action] = (transition probability, result state)
    # probabilities are input data to problem
    transitions = {'B': {'R': [(0.4, 'B'), (0.6, 'W')],
                         'P': [(0, 'B'), (1, 'W')]},
                   'W': {'N': [(0.7, 'B'), (0.3, 'W')],
                         'M': [(0.4, 'B'), (0.6, 'W')]}}
    # rewards are expected value calculations
    # rewards[state][action] = reward value
    rewards = {'B': {'R': 20, 'P': -50},
               'W': {'N': 30, 'M': 40}}

    machine = MDP(transitions, rewards)
    planning_horizon = 3
    exp_profit, opt_policy = optimality_eq(machine, planning_horizon)

    print('RESULTS')
    print('------------------------------------------------')
    letter_sts = machine.convert_state_numeric()
    for p in range(0, len(exp_profit)):
        ste = letter_sts[p]
        print('If we start in state', ste, 'then the expected profit is: $', exp_profit[p])
    for b in range(planning_horizon, 0, -1):
        print('When there are', b, 'periods to go')
        for s in range(0, len(letter_sts)):
            print('\t the optimal action is', opt_policy[b-1][s], 'when starting in state', s)


class MDP:
    # Markov Decision Process class 
    def __init__(self, transitions, rewards):
        self.states = transitions.keys()
        self.transitions = transitions
        self.rewards = rewards

    def convert_state_numeric(self):
        # map state letters to numbers
        x = 0
        let2num = {}
        for s in self.states:
            let2num[x] = s
            x = x+1
        return let2num

    def get_actions(self, state):
        # get possible actions at given state
        return self.transitions[state].keys()

    def get_reward(self, state, action):
        # get reward for taking given action at given state
        return self.rewards[state][action]

    def get_possible_results(self, state, action):
        # get possible result states from taking given action at given state
        return self.transitions[state][action]


def optimality_eq(mach, n):
    # using the Backward Induction DP algorithm
    # Note: For a large state space or action space, I might want to reconsider how I've implemented the algorithm here
    #       to avoid the use of nested for loops if possible. However, for the small test example here, this
    #       implementation does not have runtime issues.

    # initializations
    s = mach.states
    numeric_states = mach.convert_state_numeric()   # mapping to convert between letter states and numeric states
    num_states = len(s)
    mvals = np.zeros((n+1, num_states))
    optactions = np.empty((n, num_states), dtype=str)

    # for each planning period
    for k in range(1, n+1):
        # for each possible state
        for s in range(0, num_states):
            state_let = numeric_states[s]
            action_max = {}
            # for each action we can take in state s
            for a in mach.get_actions(state_let):
                # compute the max reward
                trans = mach.get_possible_results(state_let, a)
                rsa = mach.get_reward(state_let, a)
                tot = 0
                for s2 in range(0, num_states):
                    tot = tot + trans[s2][0]*mvals[k-1][s2]
                action_max[rsa+tot] = a
            mvals[k][s] = max(action_max.keys())  # store max reward value
            optactions[k-1][s] = action_max[mvals[k][s]]  # store action that resulted in max reward
    return mvals[k], optactions


if __name__ == "__main__":
    main()
