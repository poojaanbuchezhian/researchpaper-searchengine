import pickle
import math
import numpy as np


class Indexer:
    def __init__(self, corpus):
        self.k1 = 1.5 #impact of tryef
        self.b = 0.75 #influence of l (doclen/avg) on scoring
        self.delta = 1
        self.corpus_size = len(corpus)
        self.avgdl = 0 # average doc length
        self.doc_freqs = [] #frequencies of words in each doc
        self.doc_len = []   #length of each doc
        self.idf = {} #ifd of each word
        self.nd = self._index(corpus)   #word -> number of documents with word
        self._calc_idf(self.nd)

    def _index(self, corpus):
        nd = {}  #word -> number of documents with word
        num_doc = 0 #number of words in a doc
        for document in corpus:
            self.doc_len.append(len(document))
            num_doc += len(document)

            frequencies = {}
            for word in document:
                if word not in frequencies:
                    frequencies[word] = 0
                frequencies[word] += 1
            self.doc_freqs.append(frequencies)

            for word, freq in frequencies.items():
                try:
                    nd[word] += 1
                except KeyError:
                    nd[word] = 1

        self.avgdl = num_doc / self.corpus_size
        return nd
    def _calc_idf(self, nd):
        for word, freq in nd.items():
            idf = math.log((self.corpus_size + 1) / freq)
            self.idf[word] = idf
    def get_top_n(self, query, documents, n):
        scores = self.get_scores(query)
        top_n = np.argsort(scores)[::-1][:n]
        return [documents[i] for i in top_n]
    def get_scores(self, query):
        score = np.zeros(self.corpus_size)
        doc_len = np.array(self.doc_len)
        for q in query:
            q_freq = np.array([(doc.get(q) or 0) for doc in self.doc_freqs])
            score += (self.idf.get(q) or 0) * (self.delta + (q_freq * (self.k1 + 1)) /
                                               (self.k1 * (1 - self.b + self.b * doc_len / self.avgdl) + q_freq))
        return score

#obj = Indexer(tokenized_corpus)
#print(obj.nd)
#output = open('D:/9th semester/Information Retrieval Lab/package/scrapper/data/indexed_terms.pkl', 'wb')
#pickle.dump(obj.nd, output)
#output.close()
