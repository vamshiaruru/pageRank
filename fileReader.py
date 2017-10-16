import numpy as np

FILENAME = "data.txt"

rows = np.zeros(421578)
cols = np.zeros(451578)
i = 0
with open(FILENAME) as f:
    for line in f:
        line = ','.join(line.strip().split())
        try:
            row, col = line.split(",")
            rows[i] = int(row)
            cols[i] = int(col)
            i = i + 1
        except ValueError:
            print "some thing went wrong"

np.save("rows.npy", rows)
np.save("cols.npy", cols)
