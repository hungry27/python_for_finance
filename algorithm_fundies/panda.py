from unicodedata import name
import pandas as pd

#%%

#Dataframe is a table
simple = pd.DataFrame({'Yes': [50, 21], 'No': [131, 2]})
#print(simple)

# %%

# list of rows in pandas is known as index
# Dataframe is a dictionary whos key is the column name.
names = pd.DataFrame({'Bob' : ['I like it.', 'It was awful.'], 
'Sue':['Pretty good.', 'Bland.']},

    index=['Product A','Product B'])
#print(names)

# %%

#Series is a list of a sequence of data values
pd.Series([1,2,3,4,5])
#Example
named_series = pd.Series ([30,35,40], index=['2015 Sales', '2016 Sales', '2017 Sales'], name = 'Product A')

print (named_series)

#---------------------------------Indexing, Selecting & Assigning ------------------------------------------

# In pandas you can access the each column by adding a ."column_name" after the dataframe

#loc and iloc are row-first, column-second. this is the opposite of what we do in native python

#iloc uses the Python stdlib indexing scheme, where the first element of the range is included and the last one excluded. So 0:10 will select entries 0,...,9. loc, meanwhile, indexes inclusively. So 0:10 will select entries 0,...,10.

#.iloc index-based selection
#.loc label-based selection
#.isin lets you select data whose values "is in" a list of values.
#.notnull or .isnull allows me to filter out the dataset

# %%
# To get a column with iloc
named_series.iloc[:, 0]
named_series.iloc[:1, 0]

named_series.iloc[-5:]
