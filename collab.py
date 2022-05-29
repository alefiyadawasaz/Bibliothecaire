import operator
import numpy as np
import pandas as pd
import warnings

from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics.pairwise import cosine_similarity

warnings.filterwarnings("ignore")


dataset1 = pd.read_csv(r"C:\Users\Alefiya\PycharmProjects\Microsoft\allfiles\datasetexp.csv", error_bad_lines=False, encoding='ISO-8859-1', warn_bad_lines=False)
books = pd.read_csv(r"C:\Users\Alefiya\PycharmProjects\Microsoft\allfiles\cleanbooks.csv", error_bad_lines=False, encoding='ISO-8859-1', warn_bad_lines=False)
number = 10
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

testdf = pd.DataFrame()
testdf['ISBN'] = popular_book['ISBN']
testdf['Book-Rating'] = popular_book['Book-Rating']
testdf['User-ID'] = popular_book['User-ID']
testdf = testdf[['User-ID','Book-Rating']].groupby(testdf['ISBN'])
#print(testdf)

listOfDictonaries = []
indexMap = {}
reverseIndexMap = {}
ptr = 0

for groupKey in testdf.groups.keys():
    tempDict = {}
    groupDF = testdf.get_group(groupKey)
    for i in range(0, len(groupDF)):
        tempDict[groupDF.iloc[i, 0]] = groupDF.iloc[i, 1]
    indexMap[ptr] = groupKey
    reverseIndexMap[groupKey] = ptr
    ptr = ptr + 1
    listOfDictonaries.append(tempDict)

dictVectorizer = DictVectorizer(sparse=True)
vector = dictVectorizer.fit_transform(listOfDictonaries)
pairwiseSimilarity = cosine_similarity(vector)


def printBookDetails(bookID):
    print(dataset1[dataset1['ISBN'] == bookID]['Book-Title'].values[0])
    """
    print("Title:", dataset1[dataset1['ISBN']==bookID]['Book-Title'].values[0])
    print("Author:",dataset1[dataset['ISBN']==bookID]['Book-Author'].values[0])
    #print("Printing Book-ID:",bookID)
    print("\n")
    """


def getTopRecommandations(bookID):
    collaborative = []
    row = reverseIndexMap[bookID]
    #print("Input Book:")
    #printBookDetails(bookID)

    #print("\nRECOMMENDATIONS:\n")

    mn = 0
    similar = []
    for i in np.argsort(pairwiseSimilarity[row])[:-2][::-1]:
        if dataset1[dataset1['ISBN'] == indexMap[i]]['Book-Title'].values[0] not in similar:
            if mn >= number:
                break
            mn += 1
            similar.append(dataset1[dataset1['ISBN'] == indexMap[i]]['Book-Title'].values[0])
            printBookDetails(indexMap[i])
            collaborative.append(dataset1[dataset1['ISBN'] == indexMap[i]]['Book-Title'].values[0])
    return collaborative

def final(bookName):
    #bookName = input("Enter a book name: ")
    #print(m[k.index(bookName)])
    collaborative = getTopRecommandations(m[k.index(bookName)])
    #print(type(collaborative))
    #d = collaborative['Book-Title'].tolist()
    return collaborative

k = list(dataset1['Book-Title'])
m = list(dataset1['ISBN'])
#final('Deception Point')
