import pickle
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pandas as pd
import string
import json

lemmatizer = WordNetLemmatizer() #lemmatizing
more_stopwords = [word.strip() for word in open('D:\9th semester\Information Retrieval Lab\package\lemur-stopwords.txt', 'r').readlines()] #lemur stopwords
df = pd.DataFrame(columns=['id', 'title', 'abstract', 'authors', 'link']) # dataframe to read from json
id=0    #track count of docs
def preprocess_document(acad_papers,df,id):
    json_array = json.load(acad_papers) #load jsonarray
    for x in json_array:
        try:
            paper = {}
            paper['id'] = id
            paper['title'] = x['title']
            paper['abstract'] = x['abstract']
            paper['authors'] = ' '.join(map(str, x['authors'])) #making authors list to a string
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
        tokenized_df.to_pickle('D:/9th semester/Information Retrieval Lab/package/scrapper/data/tokenized_corpus11.pkl')
    elif fileno == 2:
        tokenized_df.to_pickle('D:/9th semester/Information Retrieval Lab/package/scrapper/data/tokenized_corpus2.pkl')
    elif fileno == 3:
        tokenized_df.to_pickle('D:/9th semester/Information Retrieval Lab/package/scrapper/data/tokenized_corpus3.pkl')
    elif fileno == 4:
        tokenized_df.to_pickle('D:/9th semester/Information Retrieval Lab/package/scrapper/data/tokenized_corpus4.pkl')
    elif fileno == 5:
        tokenized_df.to_pickle('D:/9th semester/Information Retrieval Lab/package/scrapper/data/tokenized_corpus5.pkl')

def get_tokenized_corpus(filename):
    df = pd.read_pickle(filename)
    tokenized_corpus = []
    for i in range(df.shape[0]):
        tokenized_corpus.append(df.iloc[i]['tokens'])
    return tokenized_corpus

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
