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

def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

def tokenize(text):
    tokens = nltk.word_tokenize(text)
    stems = stem_tokens(tokens, stemmer)
    return stems

def load_classifier(filename,path=""):
    filepath = filename
    if len(path) <> 0:
        filepath = os.path.join(path,filename)
    return joblib.load(filepath)

def read_category():
    category_file_path = os.path.join(import_classifier_location,category_filename)
    with open(category_file_path, 'rb') as f:
        return pickle.load(f)

clf = load_classifier("sgd-classifier.clf",import_classifier_location)
count_vect = load_classifier("sgd-count.transform",import_classifier_location)
categories = read_category()

#file= "/home/anair10/topic/new_test/clean_faculty/faculty/"
file= "/home/anair10/topic/new_test/testfacully/"
#file= "/home/anair10/topic/train/other/"

docs_new = []
files_names = []
for filename in os.listdir(file):
    docs_new.append(open(file+filename,"r").read())
    files_names.append(filename)
X_new_counts = count_vect.transform(docs_new)
predicted = clf.predict(X_new_counts)
for doc_name, category in zip(files_names, predicted):
    print(' %s => %s' % ( doc_name,categories[category]))
