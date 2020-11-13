import pandas as pd
from sklearn.feature_extraction.text import  CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

data = pd.DataFrame(columns=['id', 'tokens', 'category'])
cat_data=pd.DataFrame(columns=['id','tokens','category','category_code','pred_category'])
def get_data(filename,data):
    data = data.append(pd.read_pickle(filename),ignore_index=True)
    return data
def get_categorised_data(filename,cat_data):
    cat_data=cat_data.append(pd.read_pickle(filename),ignore_index=True)
    return cat_data
def get_category_name(category_id):
    for category, id_ in category_codes.items():
        if id_ == category_id:
            return category
def create_features_from_text(text):
    features = C.transform([text]).toarray()
    return features
def splitDataFrameIntoSmaller(df, chunkSize = 20000):
    listOfDf = list()
    numberChunks = len(df) // chunkSize + 1
    for i in range(numberChunks):
        listOfDf.append(df[i*chunkSize:(i+1)*chunkSize])
    return listOfDf
data = get_data('D:/9th semester/Information Retrieval Lab/package/scrapper/data/data_categorisation1_new.pkl',data)
data=  get_data('D:/9th semester/Information Retrieval Lab/package/scrapper/data/data_categorisation2_new.pkl',data)
data =  get_data('D:/9th semester/Information Retrieval Lab/package/scrapper/data/data_categorisation3_new.pkl',data)
data= get_data('D:/9th semester/Information Retrieval Lab/package/scrapper/data/data_categorisation4_new.pkl',data)
data= get_data('D:/9th semester/Information Retrieval Lab/package/scrapper/data/data_categorisation5_new.pkl',data)
category_codes = {
    'cs': 0,
    'econ': 1,
    'eess': 2,
    'math': 3,
    'physics': 4,
    'q-bio': 5,
    'q-fin': 6,
    'stat': 7
}
data['category_code'] = data['category']
data = data.replace({'category_code':category_codes})
X_train, X_test, y_train, y_test = train_test_split(data['tokens'],data['category_code'],test_size=0.25,random_state=8)
C = CountVectorizer(analyzer='word', token_pattern=r'\w{1,}', max_features=2500, dtype=np.uint8)
features_train = C.fit_transform(X_train).toarray()
labels_train = y_train
features_test = C.transform(X_test).toarray()
labels_test = y_test

mnbc = MultinomialNB(alpha=1.0, class_prior=None, fit_prior=True)
mnbc.fit(features_train, labels_train)
mnbc_pred = mnbc.predict(features_test)
pred_category_list=[]
for i in range(data.shape[0]):
    prediction = mnbc.predict(create_features_from_text(data.iloc[i]['tokens']))[0]
    category_pred = get_category_name(prediction)
    pred_category_list.append(category_pred)
data['pred_category']=pred_category_list
listdfs =  splitDataFrameIntoSmaller(data)
listdfs[0].to_pickle('D:/9th semester/Information Retrieval Lab/package/scrapper/data/data_categorisation1_final.pkl')
listdfs[1].to_pickle('D:/9th semester/Information Retrieval Lab/package/scrapper/data/data_categorisation2_final.pkl')
listdfs[2].to_pickle('D:/9th semester/Information Retrieval Lab/package/scrapper/data/data_categorisation3_final.pkl')
listdfs[3].to_pickle('D:/9th semester/Information Retrieval Lab/package/scrapper/data/data_categorisation4_final.pkl')
listdfs[4].to_pickle('D:/9th semester/Information Retrieval Lab/package/scrapper/data/data_categorisation5_final.pkl')
