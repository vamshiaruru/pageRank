"""
This module contains the EditDistance class.
"""
import shelve
import operator


class EditDistance(object):
    """
    Just a small class to calculate edit distance between two words, and find
    the top 5 corrections based on the edit distance and the number of times the
    word was used in a query.
    The source_word comes from query entered by the user, and the target_word
    is from the query corpus which is a dictionary consisting of all the
    query_words so far that have df != zero.
    """
    @staticmethod
    def edit_distance(source_word, target_word):
        """
        A very basic algorithm to calculate levenshtein distance between two
        words.
        :param source_word : (String) The word entered by user in the query.
        This
        function is called only if the df of the source_word is zero.
        :param target_word: (String)The word whose edit distance from
        source_word is
        to be checked
        :return: edit_distance (integer) between source_word and target_word
        """
        max_len = max(len(source_word), len(target_word))
        matrix = [[0 for i in xrange(max_len)] for i in xrange(max_len)]
        for i in xrange(len(source_word)):
            matrix[i][0] = i
        for i in xrange(len(target_word)):
            matrix[0][i] = i
        for i in xrange(len(source_word)):
            for j in xrange(len(target_word)):
                if source_word[i] == target_word[j]:
                    argument1 = matrix[i - 1][j - 1] + 0
                else:
                    argument1 = matrix[i - 1][j - 1] + 1
                matrix[i][j] = min(argument1, matrix[i - 1][j] + 1,
                                   matrix[i][j - 1] + 1)
        return matrix[len(source_word) - 1][len(target_word) - 1]

    def top_corrections(self, source_word):
        """
        Checks edit distance of source_word from every word in query_corpus
        and returns the top 5 corrections. It retrieves the top 5 based on
        pure edit_distance and then sorts them again based on number of times
        the query_word was used prior
        :param source_word: (String) query_word entered by user which has zero
        document frequency.
        :return:
        """
        edit_distances = []
        qc = shelve.open("query_corpus.db")
        for word in qc.iterkeys():
            edit_distances.append((word, self.edit_distance(source_word,
                                                            word), qc[word]))
        edit_distances.sort(key=operator.itemgetter(1))
        edit_distances = edit_distances[0:5]
        # edit_distances.sort(key=operator.itemgetter(2), reverse=True)
        top_corrections = [i[0] for i in edit_distances]
        return top_corrections
