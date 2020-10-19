import pickle
import preprocessing as p
class Indexer:
    def __init__(self, corpus):
        self.corpus_size = len(corpus)
        self.avgdl = 0 # average doc length
        self.doc_freqs = [] #frequencies of words in each doc
        self.doc_len = []   #length of each doc
        self.nd = self._index(corpus)   #word -> number of documents with word

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

tokenized_corpus = p.get_tokenized_corpus(
    'D:/9th semester/Information Retrieval Lab/package/scrapper/data/tokenized_corpus1.pkl') + p.get_tokenized_corpus(
    'D:/9th semester/Information Retrieval Lab/package/scrapper/data/tokenized_corpus2.pkl') + p.get_tokenized_corpus(
    'D:/9th semester/Information Retrieval Lab/package/scrapper/data/tokenized_corpus3.pkl') + p.get_tokenized_corpus(
    'D:/9th semester/Information Retrieval Lab/package/scrapper/data/tokenized_corpus4.pkl') + p.get_tokenized_corpus(
    'D:/9th semester/Information Retrieval Lab/package/scrapper/data/tokenized_corpus5.pkl')
obj = Indexer(tokenized_corpus)
print(obj.nd)
output = open('D:/9th semester/Information Retrieval Lab/package/scrapper/data/indexed_terms.pkl', 'wb')
pickle.dump(obj.nd, output)
output.close()
