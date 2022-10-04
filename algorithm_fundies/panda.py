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
# %%
