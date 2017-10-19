from __future__ import division
import random
import shelve
import os
import numpy as np
from contextlib import closing


class PreProcessor(object):
    dir_address = "./static/corpus"
    id_dictionary = "ids.db"
    num_nodes = 0
    num_edges = 0
    graph_file = "graphData.txt"
    rows = "rows.npy"
    cols = "cols.npy"
    link_prob = "prob.npy"

    def __init__(self):
        self.create_ids()
        self.graph_maker()
        self.get_rows_and_columns()
        self.get_probability()

    def create_ids(self):
        unique_id = 0
        files = os.listdir(self.dir_address)
        self.num_nodes = len(files)
        with closing(shelve.open(self.id_dictionary)) as db:
            for file_name in files:
                db[file_name] = unique_id
                unique_id = unique_id + 1

    def graph_maker(self):
        with open(self.graph_file, "w") as f:
            for i in xrange(self.num_nodes):
                edge_number = random.randrange(0, 100)
                edges = random.sample(xrange(self.num_nodes), edge_number)
                self.num_edges += len(edges)
                for edge in edges:
                    write_string = "{},{}\n".format(i, edge)
                    f.write(write_string)

    def get_rows_and_columns(self):
        rows = np.zeros(self.num_edges)
        cols = np.zeros(self.num_edges)
        i = 0
        with open(self.graph_file) as f:
            for line in f:
                line = ",".join(line.strip().split())
                try:
                    row, col = line.split(",")
                    rows[i] = int(row)
                    cols[i] = int(col)
                    i += 1
                except ValueError:
                    print "Something went wrong at {}".format(line)
        np.save(self.rows, rows)
        np.save(self.cols, cols)

    def get_probability(self):
        rows = np.load(self.rows)
        prob = np.zeros(len(rows))
        prob_dict = dict()
        for row in rows:
            if row in prob_dict.keys():
                prob_dict[row] += 1
            else:
                prob_dict[row] = 1
        i = 0
        for row in rows:
            prob[i] = 1/prob_dict[row]
            i += 1
        np.save(self.link_prob, prob)


if __name__ == "__main__":
    processor = PreProcessor()