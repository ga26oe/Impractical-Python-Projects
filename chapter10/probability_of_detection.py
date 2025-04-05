from random import randint
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt

NUM_EQUIV_VOLUMES = 1000  # number of locations in which to place civilizaiton
MAX_CIVS = 5000  # maximum number of advanced civilizations
TRIALS = 1000  # number of times to model a given number of civilizations
CIV_STEP_SIZE = 100  # civilizations count step size

x = []  # x values for polynomial fit
y = []  # y values for polynomial fit

for num_civs in range(2, MAX_CIVS + 2, CIV_STEP_SIZE):  # number of civs to model
    civs_per_vol = num_civs / NUM_EQUIV_VOLUMES
    num_single_civs = 0
    for trial in range(TRIALS):
        locations = []  # equivalent volumes containing a civilzation
        while len(locations) < num_civs:
            location = randint(1, NUM_EQUIV_VOLUMES)
            locations.append(location)
        overlap_count = Counter(locations)
        overlap_rollup = Counter(overlap_count.values())
        num_single_civs += overlap_rollup[1]  # get the numbers that only occur once

    prob = 1 - (
        num_single_civs / (num_civs * TRIALS)
    )  # probability of multiple civilizations per location for the current number of civilizaitons being distributed

    # print ratio of civs-per-volume vs. probability of 2+ civs per location
    print("{:.4f}  {:.4f}".format(civs_per_vol, prob))
    x.append(civs_per_vol)
    y.append(prob)

coefficients = np.polyfit(x, y, 4)  # 4th order polynomial fit
p = np.poly1d(coefficients)
print(f"\n{p}")
xp = np.linspace(0, 5)  # return evenly spaced numbers over interval
_ = plt.plot(x, y, ".", xp, p(xp), "-")
"""
            plot x and y lists as period(dot), then pass predicted x axis 
            (xp) and to get predicted y axis, pass p the same variable -- 
            plots result using dash 
"""
plt.ylim(-0.5, 1.5) # limit y axis to values -0.5 to 1.5
plt.show() # actually display graph
