"""
NOTE: You are only allowed to edit this file between the lines that say:
    # START EDITING HERE
    # END EDITING HERE

This file contains the base Algorithm class that all algorithms should inherit
from. Here are the method details:
    - __init__(self, num_arms, horizon): This method is called when the class
        is instantiated. Here, you can add any other member variables that you
        need in your algorithm.
    
    - give_pull(self): This method is called when the algorithm needs to
        select an arm to pull. The method should return the index of the arm
        that it wants to pull (0-indexed).
    
    - get_reward(self, arm_index, reward): This method is called just after the 
        give_pull method. The method should update the algorithm's internal
        state based on the arm that was pulled and the reward that was received.
        (The value of arm_index is the same as the one returned by give_pull.)

We have implemented the epsilon-greedy algorithm for you. You can use it as a
reference for implementing your own algorithms.
"""

import numpy as np
import math
# Hint: math.log is much faster than np.log for scalars

class Algorithm:
    def __init__(self, num_arms, horizon):
        self.num_arms = num_arms
        self.horizon = horizon
    
    def give_pull(self):
        raise NotImplementedError
    
    def get_reward(self, arm_index, reward):
        raise NotImplementedError

# Example implementation of Epsilon Greedy algorithm
class Eps_Greedy(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        # Extra member variables to keep track of the state
        self.eps = 0.1
        self.counts = np.zeros(num_arms)
        self.values = np.zeros(num_arms)
    
    def give_pull(self):
        if np.random.random() < self.eps:
            return np.random.randint(self.num_arms)
        else:
            return np.argmax(self.values)
    
    def get_reward(self, arm_index, reward):
        self.counts[arm_index] += 1
        n = self.counts[arm_index]
        value = self.values[arm_index]
        new_value = ((n - 1) / n) * value + (1 / n) * reward
        self.values[arm_index] = new_value


# START EDITING HERE
# You can use this space to define any helper functions that you need
def get_log(t):
    if t > 0:
        return math.log(t)
    else:
        return 0

def get_ucb_bonus(count, t):
    if count == 0:
        return 0
    else:
        return math.sqrt(2 * get_log(t) / count)

def get_kl_ucb(value, count, t):
    c = 3
    tolerance = 0.0001

    if count == 0:
        return value

    s = value
    e = 1.0
    m = (s+e)/2.0
    f = (get_log(t) + c*get_log(get_log(t))) / count

    while abs(s - e) > tolerance:
        if value * get_log(value / m) + (1 - value) * get_log((1 - value) / (1 - m)) > f:
            e = m
        else:
            s = m
        m = (s + e) / 2.0

    return m
# END EDITING HERE

class UCB(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        # You can add any other variables you need here
        # START EDITING HERE
        self.t = 0
        self.counts = np.zeros(num_arms)
        self.values = np.zeros(num_arms)
        self.ucbValues = np.zeros(num_arms)
        # END EDITING HERE
    
    def give_pull(self):
        # START EDITING HERE
        if self.t < self.num_arms:
            return self.t
        else:
            return np.argmax(self.ucbValues)
        # END EDITING HERE
    
    def get_reward(self, arm_index, reward):
        # START EDITING HERE
        self.t += 1
        self.counts[arm_index] += 1
        n = self.counts[arm_index]
        value = self.values[arm_index]
        new_value = ((n - 1) / n) * value + (1 / n) * reward
        self.values[arm_index] = new_value
        for ind in range(self.num_arms):
            self.ucbValues[ind] = self.values[ind] + get_ucb_bonus(self.counts[ind], self.t)
        # END EDITING HERE

class KL_UCB(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        # You can add any other variables you need here
        # START EDITING HERE
        self.t = 0
        self.counts = np.zeros(num_arms)
        self.values = np.zeros(num_arms)
        self.klucbValues = np.zeros(num_arms)
        # END EDITING HERE
    
    def give_pull(self):
        # START EDITING HERE
        if self.t < self.num_arms:
            return self.t
        else:
            return np.argmax(self.klucbValues)
        # END EDITING HERE
    
    def get_reward(self, arm_index, reward):
        # START EDITING HERE
        self.t += 1
        self.counts[arm_index] += 1
        n = self.counts[arm_index]
        value = self.values[arm_index]
        new_value = ((n - 1) / n) * value + (1 / n) * reward
        self.values[arm_index] = new_value
        for ind in range(self.num_arms):
            self.klucbValues[ind] = get_kl_ucb(self.values[ind], self.counts[ind], self.t)
        # END EDITING HERE


class Thompson_Sampling(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        # You can add any other variables you need here
        # START EDITING HERE
        self.successes = np.zeros(num_arms)
        self.failures = np.zeros(num_arms)
        self.betaValues = np.zeros(num_arms)
        # END EDITING HERE
    
    def give_pull(self):
        # START EDITING HERE
        for ind in range(self.num_arms):
            self.betaValues[ind] = np.random.beta(self.successes[ind]+1, self.failures[ind]+1)
        return np.argmax(self.betaValues)
        # END EDITING HERE
    
    def get_reward(self, arm_index, reward):
        # START EDITING HERE
        if reward == 1:
            self.successes[arm_index] += 1
        else:
            self.failures[arm_index] += 1
        # END EDITING HERE
