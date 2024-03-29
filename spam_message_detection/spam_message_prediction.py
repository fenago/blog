# -*- coding: utf-8 -*-
"""spam_message_prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1imMywBYRaA645hyw3G8B3N1j0Xi_50g2
"""

import pandas as pd
import numpy as np
import pickle

spam_data = pd.read_csv("spam.csv", engine='python')

spam_data.head()

spam_data = spam_data[['v1', 'v2']]                         #deleting unnecessary columns
spam_data['target'] = np.where(spam_data['v1']=='spam',1,0) #converting target column to binary

del spam_data['v1']

from sklearn.model_selection import train_test_split


X_train, X_test, y_train, y_test = train_test_split(spam_data['v2'], 
                                                    spam_data['target'], 
                                                    random_state=0)

from sklearn.feature_extraction.text import CountVectorizer


from sklearn.naive_bayes import MultinomialNB

cv = CountVectorizer().fit(X_train)
    
# Transform both X_train and X_test with the same CV object:
X_train_cv = cv.transform(X_train)
X_test_cv = cv.transform(X_test)
    
# Classifier for prediction:
clf = MultinomialNB(alpha=0.1)
clf.fit(X_train_cv, y_train)

from sklearn.feature_extraction.text import TfidfVectorizer

tf = TfidfVectorizer(min_df=5).fit(X_train)
X_train_tf = tf.transform(X_train)
X_test_tf = tf.transform(X_test)

clf = MultinomialNB(alpha=0.1)
clf.fit(X_train_tf, y_train)

pickle.dump(clf, open('model.pkl', 'wb'))
model = pickle.load(open('model.pkl', 'rb'))

pickle.dump(tf, open("vector.pkl", "wb"))
# newpred = ['congratulations you have earned 10 thousand dollars']
# newpred_tf = tf.transform(newpred)
#
# if str(clf.predict(newpred_tf)) == '[1]':
#     print('Its a spam!')
#
# else:
#     print('Not a spam.')
