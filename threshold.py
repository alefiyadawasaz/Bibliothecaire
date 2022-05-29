import operator
import numpy as np
import pandas as pd
import warnings

#from sklearn.feature_extraction import DictVectorizer
#from sklearn.metrics.pairwise import cosine_similarity

warnings.filterwarnings("ignore")


dataset1 = pd.read_csv(r"C:\Users\Alefiya\PycharmProjects\Microsoft\allfiles\datasetexp.csv", error_bad_lines=False, encoding='ISO-8859-1', warn_bad_lines=False)
books = pd.read_csv(r"C:\Users\Alefiya\PycharmProjects\Microsoft\allfiles\cleanbooks.csv", error_bad_lines=False, encoding='ISO-8859-1', warn_bad_lines=False)

df = pd.DataFrame(dataset1['Book-Title'].value_counts())
df['Total-Ratings'] = df['Book-Title']
df['Book-Title'] = df.index
df.reset_index(level=0, inplace=True)
df = df.drop('index',axis=1)

df = dataset1.merge(df, left_on = 'Book-Title', right_on = 'Book-Title', how = 'left')
df = df.drop(['Year-Of-Publication','Publisher','Age','City','State','Country'], axis=1)


popularity_threshold = 10
popular_book = df[df['Total-Ratings'] >= popularity_threshold]
popular_book = popular_book.reset_index(drop = True)
popular_book.sum().to_csv(r'C:\Alefiya work\Microsoft\datasets\popular.csv')

testdf = pd.DataFrame()
testdf['ISBN'] = popular_book['ISBN']
testdf['Book-Rating'] = popular_book['Book-Rating']
testdf['User-ID'] = popular_book['User-ID']
testdf = testdf[['User-ID','Book-Rating']].groupby(testdf['ISBN'])
testdf.sum().to_csv(r'C:\Alefiya work\Microsoft\datasets\testdf.csv')
#print(pd.read_csv("C:\Alefiya work\Microsoft\datasets\testdf.csv"))
