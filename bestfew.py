import operator
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

dataset1 = pd.read_csv(r"C:\Users\Alefiya\PycharmProjects\Microsoft\allfiles\datasetexp.csv", error_bad_lines=False, encoding='ISO-8859-1', warn_bad_lines=False)
books = pd.read_csv(r"C:\Users\Alefiya\PycharmProjects\Microsoft\allfiles\cleanbooks.csv", error_bad_lines=False, encoding='ISO-8859-1', warn_bad_lines=False)

def popularity_based(dataframe, n):
        data = pd.DataFrame(dataframe.groupby('ISBN')['Book-Rating'].count()).sort_values('Book-Rating', ascending=False).head(n)
        #result = pd.merge(data, books, on='ISBN', left_index = True)
        result = pd.merge(data, books,on='ISBN',how='outer')
        #print(result['Book-Title'].head(n))
        #print(type(result))
        d = result['Book-Title'].tolist()
        return d[0:15]
        #print(d[0:15])
def trend():
        number = 15
        print("Top", number, "Popular books are: ")
        rd=popularity_based(dataset1, number)
        return rd

