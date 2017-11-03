from __future__ import division
from PreProcessor import PreProcessor
import numpy as np
import scipy.sparse as ss
from search import Searcher
from contextlib import closing
from GraphViewer import GraphViewer
import shelve
import heapq
import operator
import networkx


class PageRanker(object):
    taxation_factor = 0.8
    basic_matrix = None
    trusted_pages = []

    def __init__(self):
        self.basic_matrix = self.build_stochastic_matrix()
        self.trusted_pages = self.get_trusted_pages()
        self.trust_ranker()

    def build_stochastic_matrix(self):
        rows = np.load(PreProcessor.rows)
        cols = np.load(PreProcessor.cols)
        prob = np.load(PreProcessor.link_prob)
        m = ss.csr_matrix((prob, (cols, rows))) * self.taxation_factor
        return m

    def get_trusted_pages(self):
        m = self.basic_matrix
        rank_vector = np.full(m.shape[0], 1/m.shape[0])
        count = 0
        while True:
            count += 1
            rank_vector1 = m * rank_vector
            diff = rank_vector1 - rank_vector
            diff = sum(diff * diff)
            if diff < 1e-20:
                break
            else:
                rank_vector = rank_vector1
        return rank_vector.argsort()[::-1][0:20]

    def topic_specific_ranker(self, query):
        specific_documents = Searcher(query).get_topic_documents()
        m = self.basic_matrix
        specific_doc_ids = list()
        with closing(shelve.open("ids.db")) as db:
            for doc in specific_documents:
                specific_doc_ids.append(db[doc[16:]])
        specific_vector = np.zeros(m.shape[0])
        for doc_id in specific_doc_ids:
            specific_vector[doc_id] = (1 - self.taxation_factor) / \
                                      len(specific_doc_ids)

        rank_vector = np.full(m.shape[0], 1/m.shape[0])
        while True:
            rank_vector1 = m * rank_vector + specific_vector
            diff = rank_vector1 - rank_vector
            diff = sum(diff * diff)
            if diff < 1e-50:
                break
            else:
                rank_vector = rank_vector1

        return rank_vector

    def trust_ranker(self):
        m = self.basic_matrix
        teleport_set = self.trusted_pages
        trust_vector = np.zeros(m.shape[0])
        for doc_id in teleport_set:
            trust_vector[doc_id] = 1/len(teleport_set)
        rank_vector = np.full(m.shape[0], 1/m.shape[0])
        while True:
            rank_vector1 = m * rank_vector + trust_vector
            diff = rank_vector1 - rank_vector
            diff = sum(diff * diff)
            if diff < 1e-50:
                break
            else:
                rank_vector = rank_vector1
        np.save("trustRank.npy", rank_vector)

    def visualize_trust_ranking(self):
        viewer = GraphViewer()
        m = self.basic_matrix
        teleport_set = self.trusted_pages
        trust_vector = np.zeros(m.shape[0])
        for doc_id in teleport_set:
            trust_vector[doc_id] = 1 / len(teleport_set)
        rank_vector = np.full(m.shape[0], 1 / m.shape[0])
        viewer.view_graph(node_list=list(teleport_set))
        count = 0
        while True:
            count += 1
            rank_vector1 = m * rank_vector + trust_vector
            diff = rank_vector1 - rank_vector
            diff = sum(diff * diff)
            if diff < 1e-50:
                break
            else:
                rank_vector = rank_vector1
                if count % 40 == 0:
                    try:
                        viewer.view_graph(node_list=list(teleport_set),
                                          ranks=list(rank_vector),
                                          mult_factor=20000, concat=150)
                    except networkx.exception.NetworkXError as e:
                        print e

    def topic_specific_search(self, query, scheme="topic"):
        if scheme == "trust":
            rank_vector = np.load("trustRank.npy")
        else:
            rank_vector = self.topic_specific_ranker(query)
        results = Searcher(query).cosine_score(ranker=True)
        result_ids = []
        with closing(shelve.open("ids.db")) as db:
            for doc, score in results:
                doc_id = db[doc[16:]]
                doc_rank = rank_vector[doc_id]
                result_ids.append((doc_id, doc_rank))
        sorted_scores = heapq.nlargest(20, result_ids,
                                       key=operator.itemgetter(1))
        return sorted_scores

if __name__ == "__main__":
    ranker = PageRanker()
    ranker.visualize_trust_ranking()
