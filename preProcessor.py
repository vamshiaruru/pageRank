
unique_ids = set([])
with open("data.txt") as f:
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
for key in id_mapper.keys():
    if id_mapper[key] == 34545:
        print key
