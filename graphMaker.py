import random

NUMBER_OF_NODES = 600
with open("newData.txt", "w") as f:
    for i in xrange(NUMBER_OF_NODES):
        edge_number = random.randrange(0, 5)
        edges = random.sample(xrange(NUMBER_OF_NODES), edge_number)
        for edge in edges:
            writeString = "{} {}\n".format(i, edge)
            f.write(writeString)
