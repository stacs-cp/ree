

import sys
sys.path.append('.')
from greee import multiarmed_bandit

MAB = multiarmed_bandit.MultiArmedBandit()

spec = r'''find i : int(0..100)
such that
    i = 1 * 2 + 3 * 4
find a : bool
find b : bool
find c : bool
such that
    a = !(b /\ c)'''

startingID = MAB.essence_graph.add_e_node(spec)
MAB.run_n_trials(startingID,30)

print("arms: ", MAB.arms)
print("total reward: ", MAB.total_reward)
print("rewards: ", MAB.rewards)