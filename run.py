from flask import Flask, jsonify, render_template, request
from flask_cors import CORS, cross_origin
import preprocessing as p
from indexing import Indexer
from searchengine import SearchEngine

application = Flask(__name__)
CORS(application)


@application.route('/')
def index():
    return render_template('index.html')


@application.route('/search/', methods=['POST'])
def search():
    query = request.form['query'].strip()
    docs = engine.get_top_k_docs(query)
    return jsonify(docs)

if __name__ == '__main__':

    print('Initializing Search Engine...')
    tokenized_corpus = p.get_tokenized_corpus(
        'D:/9th semester/Information Retrieval Lab/package/scrapper/data/tokenized_corpus1.pkl') + p.get_tokenized_corpus(
        'D:/9th semester/Information Retrieval Lab/package/scrapper/data/tokenized_corpus2.pkl') + p.get_tokenized_corpus(
        'D:/9th semester/Information Retrieval Lab/package/scrapper/data/tokenized_corpus3.pkl') + p.get_tokenized_corpus(
        'D:/9th semester/Information Retrieval Lab/package/scrapper/data/tokenized_corpus4.pkl') + p.get_tokenized_corpus(
        'D:/9th semester/Information Retrieval Lab/package/scrapper/data/tokenized_corpus5.pkl')
    model = Indexer(tokenized_corpus)
    corpus = p.get_corpus('D:/9th semester/Information Retrieval Lab/package/scrapper/data/corpus1.pkl') +p. get_corpus('D:/9th semester/Information Retrieval Lab/package/scrapper/data/corpus2.pkl')+p.get_corpus('D:/9th semester/Information Retrieval Lab/package/scrapper/data/corpus3.pkl') + p.get_corpus('D:/9th semester/Information Retrieval Lab/package/scrapper/data/corpus4.pkl')+p.get_corpus('D:/9th semester/Information Retrieval Lab/package/scrapper/data/corpus5.pkl')
    engine = SearchEngine(model, corpus)
    print('Done!')
    application.run()
