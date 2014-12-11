from config import *
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.datasets import load_files
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn import svm
from sklearn.tree import DecisionTreeClassifier
from sklearn import cross_validation
from sklearn.externals import joblib
import nltk
from nltk.stem.porter import PorterStemmer
import numpy as np
import os
import pickle

stemmer = PorterStemmer()

categories = ["faculty","other"]

def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

def tokenize(text):
    tokens = nltk.word_tokenize(text)
    stems = stem_tokens(tokens, stemmer)
    return stems

def save_classifier(obj,filename,path=""):
    filepath = filename
    if len(path) <> 0:
        filepath = os.path.join(path,filename)
    joblib.dump(obj, filepath)

def write_category(categories):
  category_file_path = os.path.join(export_classifier_location,category_filename)
  with open(category_file_path, 'wb') as f:
    pickle.dump(categories, f)


train = load_files(learning_data_train)
#train = load_files("/home/anair10/topic/new_test/clean_faculty/")
#categories = train.target_names
write_category(categories)

count_vect = CountVectorizer(tokenizer=tokenize,stop_words='english')
X_train_counts = count_vect.fit_transform(train.data)
clf = SGDClassifier(loss='hinge', penalty='l1',alpha=1e-3, n_iter=5).fit(X_train_counts, train.target)
save_classifier(clf,"sgd-classifier.clf",export_classifier_location)
save_classifier(count_vect,"sgd-count.transform",export_classifier_location)
