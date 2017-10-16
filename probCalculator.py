from __future__ import division
import numpy as np


rows = np.load("rows.npy")
prob = np.zeros(len(rows))
prob_dict = dict()
j = 0
for row in rows:
    if row in prob_dict.keys():
        prob_dict[row] += 1
    else:
        prob_dict[row] = 1

i = 0
for row in rows:
    prob[i] = 1/prob_dict[row]
    i += 1

np.save("prob.npy", prob)
