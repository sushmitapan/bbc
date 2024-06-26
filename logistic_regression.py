# -*- coding: utf-8 -*-
"""logistic_regression.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/10FuWdkjl9DFMMmFE4WQpxoYeWviQzETo
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import re,string
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest, chi2
import pickle
nltk.download('stopwords')
# %matplotlib inline

df = pd.read_csv('/content/bbc-text.csv', encoding = 'latin1')
df = df.sample(frac = 1)
df

df = df.dropna()

#No of a categories
len(set(df['category']))

df.groupby('category').category.count()

#Analyzing data
df.groupby('category').category.count().plot.bar()
plt.show()

#stop words
nltk.download('stopwords')
words = stopwords.words("english")
print(words)

a = "Hello_World!243"
regs = re.sub("[^a-zA-Z]", " ", a)
regs

# Data Cleaning using regex
regs = re.sub("[^a-zA-Z]", " ", df['text'][126]).lower()
regs

# Data Cleaning using stemmer

stemmer = PorterStemmer()
data = "I am loving computing".split()
print(data)
" ".join([stemmer.stem(i) for i in data])
# stemmer.stem("")

# Data Cleaning using stemmer

stemmer = PorterStemmer()
data = df['text'][0].split()
print(data)
" ".join([stemmer.stem(i) for i in data])
# stemmer.stem("")

#removing stopwords
data = df['text'][0].split()
for i in words:
  if i in data:
    c = data.count(i)
    for j in range(c):
      data.remove(i)
" ".join(data)

# Data Cleaning removing stopwords
words = stopwords.words("english")
print(words)
without_stop_words_of_a_news = " ".join([i for i in regs.lower().split() if i not in words])
without_stop_words_of_a_news

# Doing all cleaning process using regex, stemmer, stopwords for all data
df['cleaned'] = list(map(lambda x: " ".join([i for i in re.sub("[^a-zA-Z]", " ", x).split() if i not in words]),df['text']))
df['cleaned'] = df['cleaned'].apply(lambda x: " ".join([stemmer.stem(i) for i in x.lower().split()]))
df

# " ".join([stemmer.stem(i) for i in without_stop_words_of_a_news.lower().split()])

# list(filter(lambda x: [stemmer.stem(i) for i in re.sub("[^a-zA-Z]", " ", x).split() if i not in words],df['text']))

# #cleaning dataset
# nltk.download('stopwords')
# stemmer = PorterStemmer()
# words = stopwords.words("english")
# words.extend(['a','an','the'])
# df['cleaned'] = df['cleaned'].apply(lambda x: " ".join([stemmer.stem(i) for i in re.sub("[^a-zA-Z]", " ", x.lower()).split() if i not in words]).lower())
# # df['newcleaned'] = [(i for i in list(df['cleaned'])).split() if i not in words ]
# df

df.to_csv('cleaned_news.csv')

# from google.colab import drive
# drive.mount('/content/drive')

# df['cleaned'] = df['text'].apply(lambda x: " ".join([stemmer.stem(i) for i in re.sub("[^a-zA-Z]", " ", x).split() ]).lower())
# df

# print(words)

# words = stopwords.words("nepali")
# words

# df['cleaned'] = df['text'].apply(lambda x: " ".join([stemmer.stem(i) for i in re.sub("[^a-zA-Z]", " ", x).split() if i not in words]).lower())
# df

# Training model
from sklearn.linear_model import LogisticRegression
log_regression = LogisticRegression()

vectorizer = TfidfVectorizer()
X = df['cleaned']
Y = df['category']

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.15) #Splitting dataset

# #Creating Pipeline
pipeline = Pipeline([('vect', vectorizer),
                     ('chi',  SelectKBest(chi2, k=2000)),
                     ('clf', LogisticRegression(random_state=1))])

# from sklearn.pipeline import Pipeline
# from sklearn.svm import SVC
# pipeline = Pipeline([
#     ('bow', CountVectorizer(analyzer=text_process)),  # strings to token integer counts
#     ('tfidf', TfidfTransformer()),  # integer counts to weighted TF-IDF scores
#     ('classifier', SVC()),  # train on TF-IDF vectors w/ SVM
# ])


# #Training model
model = pipeline.fit(X_train, y_train)

# #Creating pickle file
# with open('LogisticRegression.pickle', 'wb') as f:
#     pickle.dump(model, f)

print(X_test,y_test)

#Accuracy
from sklearn.metrics import accuracy_score
predict_test_news_cat = model.predict(X_test)
predict_train_news_cat = model.predict(X_train)
print("Test accuracy = ",accuracy_score(y_test,predict_test_news_cat))
print("Train accuracy = ",accuracy_score(y_train,predict_train_news_cat))
print('\n')

# file = open('/content/news.txt','r')
# news = file.read()
# file.close()

news = input("Enter news = ")
news_data = {'predict_news':[news]}
news_data_df = pd.DataFrame(news_data)

predict_news_cat = model.predict(news_data_df['predict_news'])
print("Predicted news category = ",predict_news_cat[0])

# confusion matrix and classification report(precision, recall, F1-score)
ytest = np.array(y_test)
print(classification_report(ytest,model.predict(X_test)))
print(confusion_matrix(ytest,model.predict(X_test)))


import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay
cm = confusion_matrix(ytest,model.predict(X_test))
# Change figure size and increase dpi for better resolution
# and get reference to axes object
fig, ax = plt.subplots(figsize=(8,8), dpi=100)
class_names = ['business','entertainment','politics','sport','tech']
# initialize using the raw 2D confusion matrix
# and output labels (in our case, it's 0 and 1)
display = ConfusionMatrixDisplay(cm, display_labels=class_names)

# set the plot title using the axes object
ax.set(title='Confusion Matrix for Text Classification')

# show the plot.
# Pass the parameter ax to show customizations (ex. title)
display.plot(ax=ax);