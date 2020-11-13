from flask import Flask, jsonify, render_template, request
from flask_cors import CORS, cross_origin
import preprocessing as p
from indexing import Indexer
from searchengine import SearchEngine
import text_classification as t
import pandas as pd
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
    cat_data=pd.DataFrame(columns=['id','tokens','category','category_code','pred_category'])
    cat_data = t.get_categorised_data('D:/9th semester/Information Retrieval Lab/package/scrapper/data/data_categorisation1_final.pkl',cat_data)
    cat_data=  t.get_categorised_data('D:/9th semester/Information Retrieval Lab/package/scrapper/data/data_categorisation2_final.pkl',cat_data)
    cat_data =  t.get_categorised_data('D:/9th semester/Information Retrieval Lab/package/scrapper/data/data_categorisation3_final.pkl',cat_data)
    cat_data= t.get_categorised_data('D:/9th semester/Information Retrieval Lab/package/scrapper/data/data_categorisation4_final.pkl',cat_data)
    cat_data= t.get_categorised_data('D:/9th semester/Information Retrieval Lab/package/scrapper/data/data_categorisation5_final.pkl',cat_data)
    engine = SearchEngine(model, corpus, cat_data )
    print('Done!')
    application.run()
