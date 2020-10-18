import ast
import pickle

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from os import listdir
import pandas as pd
import re
import string
import json
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from hashedindex import textparser
import hashedindex

index = hashedindex.HashedIndex()
lemmatizer = WordNetLemmatizer()
more_stopwords = [word.strip() for word in open('C:/Study/NinthSem/Information Retrieval/Package/lemur-stopwords.txt', 'r').readlines()]
tokenizer = RegexpTokenizer('\w+|\$[\d\.]+|\S+')
punc_table = str.maketrans('', '', '"#$\'()*+/:<=>@[\\]^_`{|}~') # for cleaning paper abstract
df = pd.DataFrame(columns=['id', 'title', 'abstract', 'authors', 'link'])
docs=[]
id=0
def preprocess_document(acad_papers,df,id):
    json_array = json.load(acad_papers)
    for x in json_array:
        try:
            paper = {}
            paper['id'] = id
            paper['title'] = x['title']
            paper['abstract'] = x['abstract']
            paper['authors'] = ' '.join(map(str, x['authors']))
            paper['link'] = x['url']
            df = df.append(paper, ignore_index=True)
            id += 1
        except:
            continue
    return df,id
def splitDataFrameIntoSmaller(df, chunkSize = 20000):
    listOfDf = list()
    numberChunks = len(df) // chunkSize + 1
    for i in range(numberChunks):
        listOfDf.append(df[i*chunkSize:(i+1)*chunkSize])
    return listOfDf
def preprocess_content(filename, fileno):
    f = pd.read_pickle(filename)
    f['tokens'] = f['title'] + ' ' + f['abstract'] + ' ' + f['authors']
    tokenized_df = pd.DataFrame(columns=['id', 'tokens'])
    for i in range(f.shape[0]):
        paper = f.iloc[i]
        tokens = paper[['tokens']][0].lower().split()
        tokens = [word.translate(str.maketrans('', '', string.punctuation)) for word in tokens if word not in stopwords.words('english') and word not in more_stopwords]
        tokens = [lemmatizer.lemmatize(word) for word in tokens]
        tokenized_df = tokenized_df.append({'id': paper[['id']], 'tokens': tokens}, ignore_index=True)
    if fileno == 1:
        tokenized_df.to_pickle('D:/9th semester/Information Retrieval Lab/package/scrapper/data/tokenized_corpus1.pkl')
    elif fileno == 2:
        tokenized_df.to_pickle('D:/9th semester/Information Retrieval Lab/package/scrapper/data/tokenized_corpus2.pkl')
    elif fileno == 3:
        tokenized_df.to_pickle('D:/9th semester/Information Retrieval Lab/package/scrapper/data/tokenized_corpus3.pkl')
    elif fileno == 4:
        tokenized_df.to_pickle('D:/9th semester/Information Retrieval Lab/package/scrapper/data/tokenized_corpus4.pkl')
    elif fileno == 5:
        tokenized_df.to_pickle('D:/9th semester/Information Retrieval Lab/package/scrapper/data/tokenized_corpus5.pkl')

def docs_collect(filename,docs):
    f = pd.read_pickle(filename)
    for i in range(f.shape[0]):
            docs.append(' '.join(map(str,f.iloc[i]['tokens'])))
    return(docs)

def indexing(docs):
    for i in range(len(docs)):
        terms=docs[i].split(' ')
        for term in terms:
            index.add_term_occurrence(term, i)
    return(index.items())



"""
df,id=preprocess_document(open('D:/9th semester/Information Retrieval Lab/package/scrapper/data/cs.json'),df,id)
df,id=preprocess_document(open('D:/9th semester/Information Retrieval Lab/package/scrapper/data/econ.json'),df,id)
df,id=preprocess_document(open('D:/9th semester/Information Retrieval Lab/package/scrapper/data/eess.json'),df,id)
df,id=preprocess_document(open('D:/9th semester/Information Retrieval Lab/package/scrapper/data/math.json'),df,id)
df,id=preprocess_document(open('D:/9th semester/Information Retrieval Lab/package/scrapper/data/physics.json'),df,id)
df,id=preprocess_document(open('D:/9th semester/Information Retrieval Lab/package/scrapper/data/q-bio.json'),df,id)
df,id=preprocess_document(open('D:/9th semester/Information Retrieval Lab/package/scrapper/data/q-fin.json'),df,id)
df,id=preprocess_document(open('D:/9th semester/Information Retrieval Lab/package/scrapper/data/stat.json'),df,id)
print(df)


listdfs =  splitDataFrameIntoSmaller(df)
listdfs[0].to_pickle('D:/9th semester/Information Retrieval Lab/package/scrapper/data/corpus1.pkl')
listdfs[1].to_pickle('D:/9th semester/Information Retrieval Lab/package/scrapper/data/corpus2.pkl')
listdfs[2].to_pickle('D:/9th semester/Information Retrieval Lab/package/scrapper/data/corpus3.pkl')
listdfs[3].to_pickle('D:/9th semester/Information Retrieval Lab/package/scrapper/data/corpus4.pkl')
listdfs[4].to_pickle('D:/9th semester/Information Retrieval Lab/package/scrapper/data/corpus5.pkl')

preprocess_content('D:/9th semester/Information Retrieval Lab/package/scrapper/data/corpus1.pkl', 1)
preprocess_content('D:/9th semester/Information Retrieval Lab/package/scrapper/data/corpus2.pkl', 2)
preprocess_content('D:/9th semester/Information Retrieval Lab/package/scrapper/data/corpus3.pkl', 3)
preprocess_content('D:/9th semester/Information Retrieval Lab/package/scrapper/data/corpus4.pkl', 4)
preprocess_content('D:/9th semester/Information Retrieval Lab/package/scrapper/data/corpus5.pkl', 5)

"""
docs=docs_collect('C:/Study/NinthSem/Information Retrieval/Package/scrapper/data/tokenized_corpus1.pkl',docs)
docs=docs_collect('C:/Study/NinthSem/Information Retrieval/Package/scrapper/data/tokenized_corpus2.pkl',docs)
docs=docs_collect('C:/Study/NinthSem/Information Retrieval/Package/scrapper/data/tokenized_corpus3.pkl',docs)
docs=docs_collect('C:/Study/NinthSem/Information Retrieval/Package/scrapper/data/tokenized_corpus4.pkl',docs)
docs=docs_collect('C:/Study/NinthSem/Information Retrieval/Package/scrapper/data/tokenized_corpus5.pkl',docs)
result=indexing(docs)
