import numpy as np

FILENAME = "data.txt"
unique_ids = set([])
with open(FILENAME) as f:
    for line in f:
        line = ','.join(line.strip().split())
        row, col = line.split(',')
        unique_ids.add(int(row))
        unique_ids.add(int(col))
id_mapper = dict()
curr_id = 0
unique_ids = list(unique_ids)
unique_ids.sort()
for unique_id in unique_ids:
    if unique_id not in id_mapper.keys():
        id_mapper[unique_id] = curr_id
        curr_id += 1
rows = np.zeros(421579)
cols = np.zeros(421579)
i = 0
with open(FILENAME) as f:
    for line in f:
        line = ','.join(line.strip().split())
        try:
            row, col = line.split(",")
            rows[i] = id_mapper[int(row)]
            cols[i] = id_mapper[int(col)]
            i = i + 1
        except ValueError:
            print "some thing went wrong"

np.save("rows.npy", rows)
np.save("cols.npy", cols)
