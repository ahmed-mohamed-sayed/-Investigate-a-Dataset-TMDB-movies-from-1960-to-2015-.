#!/usr/bin/env python
# coding: utf-8

# 
# 
# 
# # Project: Tmdb-movies Insights
# 
# ## Table of Contents
# <ul>
# <li><a href="#intro">Introduction</a></li>
# <li><a href="#wrangling">Data Wrangling</a></li>
# <li><a href="#eda">Exploratory Data Analysis</a></li>
# <li><a href="#conclusions">Conclusions</a></li>
# </ul>

# <a id='intro'></a>
# ## Introduction
# 
# >Welcome to this exploration of Tmdb dataset.
# this dataset contains 10000 movie from year 1960 to year 2015. we will discover this data & will make the process needed (wrangling & cleaning) to answer some questions.
# We will be answering :   
# 1- Which genres aremost popular fromyear to year?   
# 2- What kinds of properties are associated with movies that have high revenues?    
# Also, we will explore conitribution of actors, directors & production companies in the most movies.    
# Let's Start Exploring.  
# 

# In[3]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# <a id='wrangling'></a>
# ## Data Wrangling
# 
# ### General Properties

# In[4]:


# read file & take a look of columns
df = pd.read_csv('tmdb-movies.csv')
df.head()


# In[5]:


# view dimensions of dataset
df.shape


# In[6]:


df.info()


# In[7]:


# show statistics & edit some columns format to read it easily
df.describe().style.format({"budget_adj": "{:,.0f}", "revenue_adj": "{:,.0f}","budget": "{:,.0f}","revenue": "{:,.0f}"})


# #### Notes:
# * 1-Revenue mean is 40 million while(min:0 & max:2.87 billion)
# * 2-Budget  mean is 15 million while(min:0 & max:425 million)
# * 3-Voting mean is 6 while(min:1.5 & max:9.2) "scale from 0 to 10"
# * 4-Popularity mean is 0.6 while (min:6.5 & max:33) "very low mean, maybe there are outliers"

# 
# 
# ### Data Cleaning 

# In[8]:


# drop columns from dataset
df.drop(['imdb_id', 'homepage', 'tagline','overview', 'release_date','budget_adj','revenue_adj','keywords'], axis=1, inplace=True)
# confirm changes
df.head()


# In[9]:


# check for any duplicated rows
df.duplicated(subset = None, keep = 'first').sum()


# In[10]:


# drop duplicated rows & check again should be Zero
df.drop_duplicates(inplace=True)
df.duplicated(subset = None, keep = 'first').sum()


# In[11]:


df.info()


# In[12]:


# view missing value count for each column in dataset
df.isnull().sum()


# In[13]:


# drop rows with any null values in dataset
df.dropna(inplace=True)
# checks if any of columns in dataset have null values - should print False
df.isnull().sum().any()


# In[14]:


# refine & split genres & production_copmanies by selecting first word:
# 1-make a copy from df
df1 = df.copy()
# 2-columns to split by "|"
split_columns = ['genres', 'production_companies','cast']

# 3-apply split function to each column of each dataframe copy
for c in split_columns:
    df1[c] = df1[c].apply(lambda x: x.split("|")[0])

df1.head()


# In[15]:


# add new column 'profit' to dataset
df1['profit'] = df1['revenue'] - df1['budget']
# reindex columns 
column_names = ["id", "original_title","cast", "production_companies","director","genres","popularity","runtime","vote_count","vote_average","release_year","budget","revenue","profit"]
df1 = df1.reindex(columns=column_names)
# check new colun existance
df1.head()


# In[16]:


# add comma to separate thousands in budget, revenue & profit to read numbers easily
df1['budget'] = df1['budget'].apply('{:,}'.format)
df1['revenue'] = df1['revenue'].apply('{:,}'.format)
df1['profit'] = df1['profit'].apply('{:,}'.format)
# check df
df1.head()


# In[17]:


# change budget, revenue & profit type from string to int
df1['budget']= df1['budget'].str.extract('(\d+)').astype(int)
df1['revenue']= df1['revenue'].str.extract('(\d+)').astype(int)
df1['profit']= df1['profit'].str.extract('(\d+)').astype(int)
# check types
df1.head()


# #### Cleaning steps:
# * 1-Drop unwanted columns. 
# * 2-Remove duplicates.
# * 3-Remove nulls.
# * 4-Split names for production companies, director & cast.
# * 5-Added new column 'profit' that we will need in exploration process.
# * 6-Reordering columns to be more consistent & tidy.
# * 7- Adding comma to separate thousands in budget, revenue & profit to read numbers easily.
# * 8-Change type from string to int for budget, revenue & profit.
# * 9-Saving cleaned df to a new one.

# In[18]:


df1.to_csv('tmdb-movies-cleaned')


# # <a id='eda'></a>
# ## Exploratory Data Analysis
# 
# > Now we are ready to explore, visualize & answering questions about dataset
# 
# ### Which genres are most popular from year to year?

# In[19]:


df1['genres'].value_counts().plot(kind='pie', figsize=(10,10),autopct='%1.1f%%')
plt.title('Movies by Genre, 1960-2015', size=15)


# #### Conclusion:
# * Drama, Comedy & Action genres are representing 60% from all movies from 1960 to 2015
# 

# ### Do higher revenues gain higher profits? 
# 

# In[20]:


df1.plot(x='revenue', y='profit', kind='scatter');


# 
# * Plotting correlation between revenue & profit.

# In[21]:


df1.plot(x='revenue', y='budget', kind='scatter');


# 
# 
# * Plotting correlation between budget & revenue
# 

# #### Conclusion:
# 
# * There is a strong correlation between revenue & profit. in other word, Movies that have bigger revenues got bigger profits.
# * However, the correlation is weak between budget & revenue. Movies with a higher budget may not get higher revenues.

# ### Have Revenues decreased or increased throughout the years?

# In[22]:


rev = df1.groupby('release_year')['revenue'].mean()
plt.plot(rev , color='brown')
plt.title('Revenues thorughout the Years', size=15);
plt.xlabel('Years', size=12)
plt.ylabel('Average Revenue', size=12);
rev


# #### Conclusion:
# 
# * Average revenue throughout the years increased from 4.5 million in 1960 to 47.5 million in 2015
# 

# ### Have Movie length decreased or increased throughout the years?

# In[23]:


mov_len = df1.groupby('release_year')['runtime'].mean()
plt.plot(rev , color='green')
plt.title('Movie length thorughout the Years', size=15);
plt.xlabel('Years', size=12)
plt.ylabel('Average Movie length in min', size=12);
mov_len


# #### Conclusion:
# 
# * Average movie length throughout the years decreased from 110 min in 1960 to 97 min in 2015

# ### Top 10 popular Movies

# In[24]:


df1[['popularity', 'original_title']].sort_values(by='popularity', ascending=False).head(10)


# ### Top 10 profitable Movies

# In[25]:


df1[['profit', 'original_title']].sort_values(by='profit', ascending=False).head(10)


# ###  Which Actors contributed to the most Movies?

# In[26]:


df1['cast'].value_counts().head(15)


# ###  Which Directors  contributed to the most Movies?

# In[27]:


df1['director'].value_counts().head(15)


# ###  Which Production company gained the most profits?

# In[28]:


df1[['profit', 'production_companies']].sort_values(by='profit', ascending=False).head(10)


# ### Which Production company produced the most Movies?

# In[29]:


df1['production_companies'].value_counts().head(15)


# <a id='conclusions'></a>
# ## Conclusions
# 
# > * Drama, Comedy & Action genres are representing 60% from all movies from 1960 to 2015
# > * Strong positive correlation between revenue & profit.
# > * Weak positive correlation between budget & revenue.
# > * Average revenue has increased throughout the years (1960 - 2015).
# > * Average movie length has decreased throughout the years (1960 - 2015).
# 
# 
# 
# 
# 
# 
# 
# 

# <a id='conclusions'></a>
# #### Limitations
# 
# > * Some columns needed much time to modify by splitting such as cast, production companies & director. I had to get a copy of the data when splitting.
# > * popularity is a subjective value because it was collected from users on different websites. also, votes collected in the same way. 
# this may lead to less accurate results.
# > 
# 

# In[30]:


from subprocess import call
call(['python', '-m', 'nbconvert', 'Investigate_a_Dataset.ipynb'])


# In[ ]:




