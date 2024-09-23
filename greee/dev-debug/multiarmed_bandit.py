""" Skeleton for multiarmed bandit selecting GP2 transforms
not in use
"""

from greee import essence_transforms
import random
import numpy as np 

class MultiArmedBandit():

    def __init__(self):

        self.essence_graph = essence_transforms.EssenceTransforms()
        self.arms = essence_transforms.gp2Interface.scanPrecompiledPrograms()
        print(self.arms)
        self.epsilon = 0.9  # Exploration rate
        self.rewards = [0] * len(self.arms)
        self.counts = [0] * len(self.arms)
        self.total_reward = 0

    def epsilon_greedy(self,epsilon, rewards, arms, x):
        if random.random() < epsilon:  # Exploration
            chosen_func = random.randint(0,len(arms)-1)
        else:  # Exploitation
            chosen_func = np.argmax(rewards)
        print(chosen_func)
        return chosen_func
    
    def run_n_trials(self, specID, num_trials):
        for _ in range(num_trials):
            chosen_func_index = self.epsilon_greedy(self.epsilon, self.rewards, self.arms, 0)
            resultID = self.essence_graph.transform_with_GP2_and_record(specID,self.arms[chosen_func_index])
            reward = 0
            if resultID != specID:
                reward = 1
            self.counts[chosen_func_index] += 1
            self.rewards[chosen_func_index] += reward
            self.total_reward += reward


    


