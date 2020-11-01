import preprocessing as p
from indexing import Indexer
import re

class SearchEngine():
    def __init__(self, model, corpus):
        self.model = model
        self.corpus = corpus
    def get_top_k_docs(self,query):
        query_words = p.preprocess_query(query) # preprocessing query
        top_k_docs=self.model.get_top_n(query_words, self.corpus,100) # get top 100 docs
        insensitive_comparers = {}
        for qw in query_words:
            insensitive_comparers[qw] = re.compile(re.escape(qw), re.IGNORECASE)
        results = {'titles': [], 'abstracts': [], 'ids': [],'authors':[], 'links': []}
        for i in top_k_docs:
                    abstract = i['abstract'].replace('\n','')
                    title = i['title'].replace('\n','')
                    authors = i['authors'].replace('\n','')
                    if abstract == '' or title == '' or authors == '':
                        continue
                    abstract = p.remove_punctuations(abstract)
                    doc_text = title.lower() + ' ' + abstract.lower() + ' ' + authors.lower()
                    query_words_found = False
                    for qw in query_words:
                        if qw in doc_text:
                            query_words_found = True
                            break
                    if not query_words_found:
                        continue
                    for qw in query_words:
                        abstract = insensitive_comparers[qw].sub('<b>' + qw + '</b>', abstract)
                    results['titles'].append(title.title())
                    results['authors'].append(authors)
                    results['abstracts'].append(abstract)
                    results['ids'].append(i['id'])
                    results['links'].append(i['link'])
        return(results)
