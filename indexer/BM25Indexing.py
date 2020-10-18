import sys
import pickle
sys.path.insert(1, 'C:/Study/NinthSem/Information Retrieval/Package/scrapper')
import arxivScrapper as ax
class BM25:
    def __init__(self, corpus, tokenizer=None):
        self.corpus_size = len(corpus)
        self.avgdl = 0
        self.doc_freqs = []
        self.idf = {}
        self.doc_len = []
        self.tokenizer = tokenizer

        if tokenizer:
            corpus = self._tokenize_corpus(corpus)

        self.nd = self._initialize(corpus)
        """self._calc_idf(nd)"""

    def _initialize(self, corpus):
        nd = {}  # word -> number of documents with word
        num_doc = 0
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

    def _tokenize_corpus(self, corpus):
        pool = Pool(cpu_count())
        tokenized_corpus = pool.map(self.tokenizer, corpus)
        return tokenized_corpus


tokenized_corpus = ax.get_tokenized_corpus(
    'C:/Study/NinthSem/Information Retrieval/Package/scrapper/data/tokenized_corpus1.pkl') + ax.get_tokenized_corpus(
    'C:/Study/NinthSem/Information Retrieval/Package/scrapper/data/tokenized_corpus2.pkl') + ax.get_tokenized_corpus(
    'C:/Study/NinthSem/Information Retrieval/Package/scrapper/data/tokenized_corpus3.pkl') + ax.get_tokenized_corpus(
    'C:/Study/NinthSem/Information Retrieval/Package/scrapper/data/tokenized_corpus4.pkl') + ax.get_tokenized_corpus(
    'C:/Study/NinthSem/Information Retrieval/Package/scrapper/data/tokenized_corpus5.pkl')
obj = BM25(tokenized_corpus)
print(type(obj.nd))
output = open('C:/Study/NinthSem/Information Retrieval/Package/scrapper/data/indexed_terms.pkl', 'wb')
pickle.dump(obj.nd, output)
output.close()