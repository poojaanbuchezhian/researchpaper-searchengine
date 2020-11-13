import pickle
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
import pandas as pd
import string
import json

lemmatizer = WordNetLemmatizer() #lemmatizing
more_stopwords = [word.strip() for word in open('D:\9th semester\Information Retrieval Lab\package\lemur-stopwords.txt', 'r').readlines()] #lemur stopwords
df = pd.DataFrame(columns=['id', 'title', 'abstract', 'authors', 'link' , 'category']) # dataframe to read from json
id=0    #track count of docs
def preprocess_document(acad_papers,df,id):
    json_array = json.load(open(acad_papers)) #load jsonarray
    l=acad_papers.split('/')
    l1=l[len(l)-1].split('.')
    category=l1[0]
    for x in json_array:
        try:
            paper = {}
            paper['id'] = id
            paper['title'] = x['title']
            paper['abstract'] = x['abstract']
            paper['authors'] = ' '.join(map(str, x['authors'])) #making authors list to a string
            paper['link'] = x['url']
            paper['category']=category
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
def get_corpus(filename):
    df = pd.read_pickle(filename)
    corpus = []
    for i in range(df.shape[0]):
        corpus.append({'title': df.iloc[i]['title'], 'abstract': df.iloc[i]['abstract'], 'authors': df.iloc[i]['authors'],
                       'link': df.iloc[i]['link'], 'id': df.iloc[i]['id']})
    return corpus
def preprocess_query(query_string):
    tokenizer = RegexpTokenizer('\w+|\$[\d\.]+|\S+')
    query_string = query_string.lower()
    new_text = tokenizer.tokenize(query_string)
    new_text = [word.translate(str.maketrans('', '', string.punctuation)) for word in new_text if word not in stopwords.words('english') and word not in more_stopwords]
    new_text = [lemmatizer.lemmatize(word) for word in new_text]
    return new_text
def remove_punctuations(text):
    punc_table = str.maketrans('', '', '"#$\'()*+/:<=>@[\\]^_`{|}~')
    return text.translate(punc_table)

"""
df,id=preprocess_document('D:/9th semester/Information Retrieval Lab/package/scrapper/data/cs.json',df,id)
print(id)
df,id=preprocess_document('D:/9th semester/Information Retrieval Lab/package/scrapper/data/econ.json',df,id)
print(id)
df,id=preprocess_document('D:/9th semester/Information Retrieval Lab/package/scrapper/data/eess.json',df,id)
print(id)
df,id=preprocess_document('D:/9th semester/Information Retrieval Lab/package/scrapper/data/math.json',df,id)
print(id)
df,id=preprocess_document('D:/9th semester/Information Retrieval Lab/package/scrapper/data/physics.json',df,id)
print(id)
df,id=preprocess_document('D:/9th semester/Information Retrieval Lab/package/scrapper/data/q-bio.json',df,id)
print(id)
df,id=preprocess_document('D:/9th semester/Information Retrieval Lab/package/scrapper/data/q-fin.json',df,id)
print(id)
df,id=preprocess_document('D:/9th semester/Information Retrieval Lab/package/scrapper/data/stat.json',df,id)
print(id)
print(df)

df['tokens'] = df['title'] + ' ' + df['abstract'] + ' ' + df['authors']
tokenized_df = pd.DataFrame(columns=['id', 'tokens', 'category'])
for i in range(df.shape[0]):
        paper = df.iloc[i]
        print(i)
        tokens = paper[['tokens']][0].lower().split()
        tokens = [word.translate(str.maketrans('', '', string.punctuation)) for word in tokens if word not in stopwords.words('english') and word not in more_stopwords]
        tokens = [lemmatizer.lemmatize(word) for word in tokens]
        tokenized_df = tokenized_df.append({'id': paper[['id']], 'tokens': tokens, 'category': paper[['category']] }, ignore_index=True)
print(tokenized_df)
listdfs =  splitDataFrameIntoSmaller(tokenized_df)
listdfs[0].to_pickle('D:/9th semester/Information Retrieval Lab/package/scrapper/data/data_categorisation1.pkl')
listdfs[1].to_pickle('D:/9th semester/Information Retrieval Lab/package/scrapper/data/data_categorisation2.pkl')
listdfs[2].to_pickle('D:/9th semester/Information Retrieval Lab/package/scrapper/data/data_categorisation3.pkl')
listdfs[3].to_pickle('D:/9th semester/Information Retrieval Lab/package/scrapper/data/data_categorisation4.pkl')
listdfs[4].to_pickle('D:/9th semester/Information Retrieval Lab/package/scrapper/data/data_categorisation5.pkl')


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



df1 = pd.DataFrame(columns=['id', 'tokens', 'category'])
def get_tokenized_corpus(filename,df1):
    f = pd.read_pickle(filename)
    for i in range(f.shape[0]):
        print(f.iloc[i]['id']['id'])
        data={}
        data['tokens']=' '.join(f.iloc[i]['tokens'])
        data['id']=f.iloc[i]['id']['id']
        data['category']=f.iloc[i]['category']['category']
        df1 = df1.append(data, ignore_index=True)
    return df1
df1=get_tokenized_corpus('D:/9th semester/Information Retrieval Lab/package/scrapper/data/data_categorisation1.pkl',df1)
df1=get_tokenized_corpus('D:/9th semester/Information Retrieval Lab/package/scrapper/data/data_categorisation2.pkl',df1)
df1=get_tokenized_corpus('D:/9th semester/Information Retrieval Lab/package/scrapper/data/data_categorisation3.pkl',df1)
df1=get_tokenized_corpus('D:/9th semester/Information Retrieval Lab/package/scrapper/data/data_categorisation4.pkl',df1)
df1=get_tokenized_corpus('D:/9th semester/Information Retrieval Lab/package/scrapper/data/data_categorisation5.pkl',df1)
print(df1)
listdfs =  splitDataFrameIntoSmaller(df1)
listdfs[0].to_pickle('D:/9th semester/Information Retrieval Lab/package/scrapper/data/data_categorisation1_new.pkl')
listdfs[1].to_pickle('D:/9th semester/Information Retrieval Lab/package/scrapper/data/data_categorisation2_new.pkl')
listdfs[2].to_pickle('D:/9th semester/Information Retrieval Lab/package/scrapper/data/data_categorisation3_new.pkl')
listdfs[3].to_pickle('D:/9th semester/Information Retrieval Lab/package/scrapper/data/data_categorisation4_new.pkl')
listdfs[4].to_pickle('D:/9th semester/Information Retrieval Lab/package/scrapper/data/data_categorisation5_new.pkl')

"""
