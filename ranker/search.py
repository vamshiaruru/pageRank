"""
This is the script that is exposed to the GUI/user. It calls the ranking
script, takes the query and searches for it.
"""
from __future__ import division
import shelve
from contextlib import closing
import math
from collections import Counter
import heapq
import operator
from EditDistace import EditDistance
import nltk
from nltk import word_tokenize


class Searcher(object):
    """
    This class defines all the search methods. It is the one that is exposed
    to Flask (for GUI).
    ;query: String, the query entered by user.
    ;query_score: a dictionary containing scores for each word query_word. The
    score is tf-idf score.
    ;stop_word : a list that contains all the query_words whose df is greater
    than 500. They are considered stop words, and are given score of zero unless
    specifically told otherwise.
    ;weighted : a boolean that checks whether the scores are calculated by the
    tf-idf scores or the scores given by the user.
    ;top_corrections : a dict containing top_corrections for all the words in
    query that have zero df.
    ;boolean_results : set of documents which satisfy boolean search model.
    """
    query = None
    query_score = dict()
    DOCUMENT_NUMBER = 690
    weighted = False
    stop_word = []
    top_corrections = dict()
    boolean_results = set()
    title_results = set()
    QUERY_CORPUS = "query_corpus.db"
    TITLES = "titles.db"
    DICTIONARY = "dictionary.db"
    LENGTH = "length.db"

    def __init__(self, input_query, **kwargs):
        self.query = input_query
        self.top_corrections = {}
        if kwargs.get("query_score"):
            # query_score is teh dictionary that is given by the user which
            # contains custom scores for each words. In that case we don't
            # need to calculate scores at all.
            self.query_score = kwargs.get("query_score")
            self.weighted = True
        else:
            self.query_score = {}

    def query_score_calculator(self, words):
        """
        This method updates the query_score dictionary with the score for each
        word. The score is calculated by tf-idf-cosine normalization for
        query_words. If the user supplies the scores for each words (
        determined by checking the weighted boolean), there is nothing left to do
        in this method, So we simply return. It also fills the boolean results
        set. Any document in boolean results set should be at the top of
        results list.
        1) First, term frequency of each term in the query is calculated.
        2) Df, idf are calculated with respect to the inverted index. if the
        df > 500, it is considered a stop word and added to the stop_words
        list and it's score is zero
        3) we consider each query a vector with dimensions as words and score
        corresponding to each word is used to calculate vector length
        4) score of each word is divided with this vector length to normalize
        and query_score is updated to contain updated scores.
        :param words: list of query_words
        :return:
        """
        if self.weighted:
            return
        self.query_score.update(Counter(words))
        first = True
        for key in self.query_score.iterkeys():
            with closing(shelve.open(self.DICTIONARY)) as db:
                if first:
                    first = False
                    post_set = set(db.get(key, {}).keys())
                    self.boolean_results = set.union(self.boolean_results,
                                                     post_set)
                else:
                    post_set = set(db.get(key, {}).keys())
                    self.boolean_results = set.intersection(self.boolean_results,
                                                            post_set)
                self.query_score[key] = 1 + math.log(self.query_score[key], 10)
                df = len(db.get(key, {}))
                if df == 0:
                    idf = 0
                elif df > 500:
                    idf = 0
                    self.stop_word.append(key)
                else:
                    idf = math.log(self.DOCUMENT_NUMBER/df)
                self.query_score[key] *= idf
        vector_length = 0
        for key in self.query_score.iterkeys():
            vector_length += math.pow(self.query_score[key], 2)
        vector_length = math.pow(vector_length, 0.5)
        if vector_length == 0:
            return
        for key in self.query_score.iterkeys():
            self.query_score[key] /= vector_length

    def cosine_score(self, **kwargs):
        """
        Calculates cosine score for query_words. It also adds query_word to
        query_corpus. If the word was already present in the corpus,
        it increases its value by 1.
        It also populates the stop_word list of this class so as to let the
        user know what are the stop-words.
        Uses heapq.sort to get the top 20 items.
        ;kwargs['ranker'] = True implies we will use this function to return
        just top 50 relevant documents, which will then be sorted by order of
        their page ranks.
        :return: Top 20 documents with highest score
        """
        porter = nltk.PorterStemmer()
        query_words = [porter.stem(t) for t in word_tokenize(self.query.strip())]
        query_words = [word.encode("utf-8") for word in query_words]
        self.query_score_calculator(query_words)
        db = shelve.open(self.DICTIONARY)
        length = shelve.open(self.LENGTH)
        qc = shelve.open(self.QUERY_CORPUS)
        for word in query_words:
            if self.query_score[word]:
                if word in qc:
                    prev = qc[word]
                    qc[word] = prev + 1
                else:
                    qc[word] = 1
            elif not self.query_score[word] and word not in self.stop_word:
                self.top_corrections[word] = EditDistance().top_corrections(word)
        scores = {}
        for query_term in self.query_score.iterkeys():
            posting_list = db.get(query_term, {})
            for file_name in posting_list.iterkeys():
                document_score = scores.get(file_name, 0)
                document_score += self.query_score[query_term] *\
                                  posting_list[file_name]
                scores[file_name] = document_score
        for document in scores:
            scores[document] /= length[document]

        db.close()
        length.close()
        qc.close()
        scores = scores.items()
        sorted_scores = heapq.nlargest(20, scores, key=operator.itemgetter(1))
        self.fill_title_results()
        if kwargs.get('ranker'):
            return heapq.nlargest(50, scores, key=operator.itemgetter(1))
        if len(self.title_results) > 10:
            return sorted_scores
        else:
            top_priority = self.title_results
            if len(self.boolean_results) < 10:
                top_priority = set.union(top_priority, self.boolean_results)
        for document in top_priority:
            sorted_scores = filter(lambda x: x[0] != document, sorted_scores)

        return sorted_scores

    def fill_title_results(self):
        """
        Find the documents which have all the query_terms in their titles and
        fill self.title_results
        :return:
        """
        flag = True
        empty_set = set()
        with closing(shelve.open(self.TITLES)) as db:
            for key in self.query_score.iterkeys():
                if flag:
                    flag = False
                    self.title_results = set.union(self.title_results,
                                                   db.get(key, empty_set))
                else:
                    self.title_results = set.intersection(self.title_results,
                                                          db.get(key, empty_set))

    def get_topic_documents(self):
        """
        Finds all documents that are related to the topic of the current query.
        We assume that documents that can be considered as specific to the topic
        of the query as all those documents that contain non-stop words of the
        query words.
        :return: a list of relevant documents.
        """
        porter = nltk.PorterStemmer()
        query_words = [porter.stem(t) for t in word_tokenize(self.query.strip())]
        query_words = [word.encode("utf-8") for word in query_words]
        self.query_score_calculator(query_words)
        specific_documents = set()
        with closing(shelve.open(self.TITLES)) as db:
            for key in self.query_score.iterkeys():
                specific_documents = set.union(specific_documents,
                                               db.get(key, specific_documents))
        return specific_documents

if __name__ == "__main__":
    pass
