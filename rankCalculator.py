from __future__ import division
import numpy as np
import scipy.sparse as ss

rows = np.load("rows1.npy")
cols = np.load("cols1.npy")
prob = np.load("prob1.npy")

M = ss.csr_matrix((prob, (rows, cols)))
M = M.transpose()
print M
print rows.shape
print cols.shape
print prob.shape
