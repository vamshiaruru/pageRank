from __future__ import division
import numpy as np
import scipy.sparse as ss

taxation_factor = 0.85
rows = np.load("rows.npy")
cols = np.load("cols.npy")
prob = np.load("prob.npy")
rank_vector = np.full(34546, 1/34546)
taxation_vector = np.ones(34546) * (1 - taxation_factor)/34546

M = ss.csr_matrix((prob, (cols, rows))) * taxation_factor

