from __future__ import  division
from PreProcessor import PreProcessor
import numpy as np
import scipy.sparse as ss


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
