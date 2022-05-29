import csv
import re
import pickle
import operator
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter
from scipy.sparse import csr_matrix
from pandas.api.types import is_numeric_dtype


import warnings
warnings.filterwarnings("ignore")

#DATASETS
books = pd.read_csv(r"C:\Alefiya work\Microsoft\Books\Books.csv", error_bad_lines=False, encoding='ISO-8859-1', warn_bad_lines=False)
users = pd.read_csv(r"C:\Alefiya work\Microsoft\Users\Users.csv", error_bad_lines=False, encoding='ISO-8859-1', warn_bad_lines=False)
ratings = pd.read_csv(r"C:\Alefiya work\Microsoft\Ratings\Ratings.csv", error_bad_lines=False, encoding='ISO-8859-1', warn_bad_lines=False)

print("Books Data:", books.shape)
print("Users Data:", users.shape)
print("Books-ratings:", ratings.shape)

#BOOKS PREPROCESSING
#print("Columns:", list(books.columns))
#print(books.head())

## Drop URL columns
books.drop(['Image-URL-S', 'Image-URL-M', 'Image-URL-L'], axis=1, inplace=True)
#print(books.head())

## Checking for null values
#print(books.isnull().sum())

#print(books.loc[books['Book-Author'].isnull(),:])

#print(books.loc[books['Publisher'].isnull(),:])

books.at[187689 ,'Book-Author'] = 'Other'

books.at[128890 ,'Publisher'] = 'Other'
books.at[129037 ,'Publisher'] = 'Other'

## Checking for column Year-of-publication
#print(books['Year-Of-Publication'].unique())

pd.set_option('display.max_colwidth', -1)
#print(books.loc[books['Year-Of-Publication'] == 'DK Publishing Inc',:])
#print(books.loc[books['Year-Of-Publication'] == 'Gallimard',:])

#correction
books.at[209538 ,'Publisher'] = 'DK Publishing Inc'
books.at[209538 ,'Year-Of-Publication'] = 2000
books.at[209538 ,'Book-Title'] = 'DK Readers: Creating the X-Men, How It All Began (Level 4: Proficient Readers)'
books.at[209538 ,'Book-Author'] = 'Michael Teitelbaum'

books.at[221678 ,'Publisher'] = 'DK Publishing Inc'
books.at[221678 ,'Year-Of-Publication'] = 2000
books.at[209538 ,'Book-Title'] = 'DK Readers: Creating the X-Men, How Comic Books Come to Life (Level 4: Proficient Readers)'
books.at[209538 ,'Book-Author'] = 'James Buckley'

books.at[220731 ,'Publisher'] = 'Gallimard'
books.at[220731 ,'Year-Of-Publication'] = '2003'
books.at[209538 ,'Book-Title'] = 'Peuple du ciel - Suivi de Les bergers '
books.at[209538 ,'Book-Author'] = 'Jean-Marie Gustave Le ClÃ?Â©zio'

## Converting year of publication in Numbers
books['Year-Of-Publication'] = books['Year-Of-Publication'].astype(int)
#print(sorted(list(books['Year-Of-Publication'].unique())))

## Replacing Invalid years with max year
count = Counter(books['Year-Of-Publication'])
#print([k for k, v in count.items() if v == max(count.values())]) #returns max year=2002 here

books.loc[books['Year-Of-Publication'] > 2021, 'Year-Of-Publication'] = 2002
books.loc[books['Year-Of-Publication'] == 0, 'Year-Of-Publication'] = 2002

## Uppercasing all alphabets in ISBN
books['ISBN'] = books['ISBN'].str.upper()

## Drop duplicate rows
books.drop_duplicates(keep='last', inplace=True)
books.reset_index(drop = True, inplace = True)

#print(books.info())
#print(books.head())
books.to_csv(r'C:\Users\Alefiya\PycharmProjects\Microsoft\allfiles\cleanbooks.csv')

#USERS PREPROCESSING
#print("Columns: ", list(users.columns))
#print(users.head())

#Checking null values
#print(users.isna().sum())

#Check for all values present in Age column
#print(sorted(list(users['Age'].unique())))

required = users[users['Age'] <= 80]
required = required[required['Age'] >= 10]
mean = round(required['Age'].mean())
#print(mean)

users.loc[users['Age'] > 80, 'Age'] = mean    #outliers with age greater than 80 are substituted with mean
users.loc[users['Age'] < 10, 'Age'] = mean    #outliers with age less than 10 years are substitued with mean
users['Age'] = users['Age'].fillna(mean)      #filling null values with mean
users['Age'] = users['Age'].astype(int)       #changing Datatype of users' age to int

list_ = users.Location.str.split(', ')

city = []
state = []
country = []
count_no_state = 0
count_no_country = 0

for i in range(0, len(list_)):
    if list_[i][0] == ' ' or list_[i][0] == '' or list_[i][0] == 'n/a' or list_[i][0] == ',':  # removing invalid entries too
        city.append('other')
    else:
        city.append(list_[i][0].lower())

    if (len(list_[i]) < 2):
        state.append('other')
        country.append('other')
        count_no_state += 1
        count_no_country += 1
    else:
        if list_[i][1] == ' ' or list_[i][1] == '' or list_[i][1] == 'n/a' or list_[i][1] == ',':  # removing invalid entries
            state.append('other')
            count_no_state += 1
        else:
            state.append(list_[i][1].lower())

        if (len(list_[i]) < 3):
            country.append('other')
            count_no_country += 1
        else:
            if list_[i][2] == '' or list_[i][1] == ',' or list_[i][2] == ' ' or list_[i][2] == 'n/a':
                country.append('other')
                count_no_country += 1
            else:
                country.append(list_[i][2].lower())

users = users.drop('Location', axis=1)

temp = []
for ent in city:
    c = ent.split('/')  # handling cases where city/state entries from city list as state is already given
    temp.append(c[0])

df_city = pd.DataFrame(temp, columns=['City'])
df_state = pd.DataFrame(state, columns=['State'])
df_country = pd.DataFrame(country, columns=['Country'])

users = pd.concat([users, df_city], axis=1)
users = pd.concat([users, df_state], axis=1)
users = pd.concat([users, df_country], axis=1)

#print(count_no_country)  # printing the number of countries didnt have any values
#print(count_no_state)  # printing the states which didnt have any values

#Drop duplicate rows
users.drop_duplicates(keep='last', inplace=True)
users.reset_index(drop=True, inplace=True)
#print(users.info())
#print(users.head())
users.to_csv(r'C:\Users\Alefiya\PycharmProjects\Microsoft\allfiles\cleanusers.csv')

#RATINGS PREPROCESSING
#print("Columns: ", list(ratings.columns))
#print(ratings.head())

#Checking for null values
#print(ratings.isnull().sum())

#Checking all ratings number or not
#print(is_numeric_dtype(ratings['Book-Rating']))

#Checking User-ID contains only number or not
#print(is_numeric_dtype(ratings['User-ID']))

#Checking ISBN
flag = 0
k =[]
reg = "[^A-Za-z0-9]"

for x in ratings['ISBN']:
    z = re.search(reg,x)
    if z:
        flag = 1

#if flag == 1:
    #print("False")
#else:
    #print("True")

#Removing extra characters from ISBN (from ratings dataset) existing in books dataset
bookISBN = books['ISBN'].tolist()
reg = "[^A-Za-z0-9]"
for index, row_Value in ratings.iterrows():
    z = re.search(reg, row_Value['ISBN'])
    if z:
        f = re.sub(reg,"",row_Value['ISBN'])
        if f in bookISBN:
            ratings.at[index , 'ISBN'] = f

#Uppercasing all alphabets in ISBN
ratings['ISBN'] = ratings['ISBN'].str.upper()

#Drop duplicate rows
ratings.drop_duplicates(keep='last', inplace=True)
ratings.reset_index(drop=True, inplace=True)
#print(ratings.info())
#print(ratings.head())
ratings.to_csv(r'C:\Users\Alefiya\PycharmProjects\Microsoft\allfiles\cleanratings.csv')

#MERGING OF ALL THREE DATASETS
#dataset = pd.merge(books, ratings, on='ISBN', how='inner')
#dataset = pd.merge(dataset, users, on='User-ID', how='inner')
#print(dataset.info())

# Explicit Ratings Dataset
#dataset1 = dataset[dataset['Book-Rating'] != 0]
#dataset1 = dataset1.reset_index(drop = True)
#print(dataset1.shape)

# Implicit Ratings Dataset
#dataset2 = dataset[dataset['Book-Rating'] == 0]
#dataset2 = dataset2.reset_index(drop = True)
#print(dataset2.shape)

#print(dataset1.head())

#dataset.to_csv(r'C:\Alefiya work\Microsoft\datasets\dataset.csv')
#dataset1.to_csv(r'C:\Alefiya work\Microsoft\datasets\datasetexp.csv')
#dataset2.to_csv(r'C:\Alefiya work\Microsoft\datasets\datasetimp.csv')