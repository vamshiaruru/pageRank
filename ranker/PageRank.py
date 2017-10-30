from __future__ import division
from PreProcessor import PreProcessor
import numpy as np
import scipy.sparse as ss
from search import Searcher
from contextlib import closing
import shelve


class PageRanker(object):
    taxation_factor = 0.8
    basic_matrix = None

    def __init__(self):
        self.basic_matrix = self.build_stochastic_matrix()

    def build_stochastic_matrix(self):
        rows = np.load(PreProcessor.rows)
        cols = np.load(PreProcessor.cols)
        prob = np.load(PreProcessor.link_prob)
        m = ss.csr_matrix((prob, (cols, rows))) * self.taxation_factor
        return m

    def topic_specific_ranker(self, query):
        specific_documents = Searcher(query).get_topic_documents()
        m = self.basic_matrix
        specific_doc_ids = list()
        with closing(shelve.open("ids.db")) as db:
            for doc in specific_documents:
                specific_doc_ids.append(db[doc[16:]])
        specific_vector = np.zeros(m.shape[0])
        for doc_id in specific_doc_ids:
            specific_vector[doc_id] = 

if __name__ == "__main__":
    PageRanker().topic_specific_ranker("space")