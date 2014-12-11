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

class FacultyPredictor:
    def __init__(self):
        self.clf = load_classifier("sgd-classifier.clf",import_classifier_location)
        self.count_vect = load_classifier("sgd-count.transform",import_classifier_location)
        self.categories = read_category()

    def predict_label(self,filecontent):
      try:
        docs_new = []
        docs_new.append(filecontent)
        X_new_counts = self.count_vect.transform(docs_new)
        predicted = self.clf.predict(X_new_counts)
        #print predicted
        return predicted#, self.categories[predicted]
      except:
        return 1#,"None"
