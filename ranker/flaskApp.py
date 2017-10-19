"""
Defines various methods that are used to render templates with data obtained
from python and then use flask to serve them.
"""
from search import Searcher
from flask import Flask, render_template, request
import unicodedata
import time
app = Flask(__name__)


@app.route("/")
def main():
    """
    Displays a basic search_bar
    :return:
    """
    return render_template("index.html")


@app.route("/displayResults", methods=['POST'])
def search():
    """
    When a user enters a search query, it is obtained here. It calculates the
    top documents by using the Searcher class.
    :return: A template which is populated by input_query, top 20 results,
    cosine scores of various query_words, and words whose document frequency
    is zero.
    """
    query = request.form.get('searchBar')
    query = unicodedata.normalize('NFKD', query).encode('ascii', 'ignore')
    now = time.clock()
    searcher = Searcher(query)
    results = searcher.cosine_score()
    scores = searcher.query_score
    print time.clock() - now
    zero_scores = searcher.top_corrections
    boolean_results = searcher.boolean_results
    if len(boolean_results) == 0:
        boolean_error = True
    else:
        boolean_error = False
    title_results = searcher.title_results
    if len(title_results) > 10 :
        title_results = []
    return render_template("displayResults.html", input_query=query,
                           results=results, scores=scores,
                           zero_scores=zero_scores, title_results=title_results,
                           error=boolean_error, boolean_results=boolean_results)


@app.route("/displayWeightedResults", methods=['POST'])
def weighted_search():
    """
    When a user Enters weights to use for different query_words, those are
    obtained by this method.
    :return: A template populated by input_query, results obtained due to
    weighted search, the scores of various query_words as given by the user
    and words whose document frequency is zero
    """
    weights = {}
    query = request.form.get("query")
    for key in request.form:
        if key == "query":
            query = request.form[key]
            query = unicodedata.normalize('NFKD', query).encode('ascii',
                                                                'ignore')

        else:
            weights[key] = request.form[key]
            weights[key] = unicodedata.normalize('NFKD', weights[key]).encode(
                                                            'ascii', 'ignore')
            weights[key] = float(weights[key])/100

    searcher = Searcher(query, query_score=weights)
    results = searcher.cosine_score()
    scores = searcher.query_score
    zero_scores = searcher.top_corrections
    boolean_results = searcher.boolean_results
    if len(boolean_results) == 0:
        boolean_error = True
    else:
        boolean_error = False
    title_results = searcher.title_results
    return render_template("displayResults.html", input_query=query,
                           results=results, scores=scores,
                           zero_scores=zero_scores, title_results=title_results,
                           error=boolean_error)

if __name__ == '__main__':
    app.debug = True
    app.run()
