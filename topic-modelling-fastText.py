# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 10:10:14 2019
https://shuaiw.github.io/2016/12/22/topic-modeling-and-tsne-visualzation.html
@author: Andrew
"""
import pyLDAvis.gensim
import pickle
from nltk.stem.wordnet import WordNetLemmatizer
import nltk
from nltk.corpus import wordnet as wn
import gensim 
import glob2
import os
from IPython.display import display, HTML
from gensim.test.utils import datapath
import random
import spacy
nlp=spacy.load('en')
from spacy.lang.en import English
from gensim.models import FastText
"""
global variables
"""
parser = English()
en_stop = set(nltk.corpus.stopwords.words('english'))
path="E://source/"

"""
utility functions to find meaning of words, synonms, antonyms, etc
"""
def get_lemma(word):
    lemma = wn.morphy(word)
    if lemma is None:
        return word
    else:
        return lemma
    

def get_lemma2(word):
    return WordNetLemmatizer().lemmatize(word)

"""
tokenize text using Spacy
"""
def tokenize(text):
    lda_tokens = []
    tokens = parser(text)
    for token in tokens:
        if token.orth_.isspace():
            continue
        elif token.like_url:
            lda_tokens.append('URL')
        elif token.orth_.startswith('@'):
            lda_tokens.append('SCREEN_NAME')
        else:
            lda_tokens.append(token.lower_)
    return lda_tokens




"""
prepare text for topic modelling
"""
def prepare_text_for_lda(text):
    tokens = tokenize(text)
    tokens = [token for token in tokens if len(token) > 4]
    tokens = [token for token in tokens if token not in en_stop]
    tokens = [get_lemma(token) for token in tokens]
    return tokens


"""
open data
"""
text_data = []
for file_path in glob2.glob(os.path.join(path, '*.txt')):
    with open (file_path, "r", encoding='utf-8') as myfile:
        for line in myfile:
            tokens=prepare_text_for_lda(line)
            if random.random()>.99:
                text_data.append(tokens)

"""
create dictionary and corpus and save for future use
"""
dictionary = gensim.corpora.Dictionary(text_data)

#create corpus 
corpus = [dictionary.doc2bow(text) for text in text_data]
#save corpus and dictionary
pickle.dump(corpus, open('corpus10.pkl', 'wb'))
dictionary.save('dictionary-med-tagged-complete.gensim')

"""
train and save an LDA model
use NUM_TOPICS variable to determine the number of topics for the model, and num_words parameter for how much to show
"""
NUM_TOPICS = 10
ft_model = FastText((text_data), size=100, window=5, min_count=150, workers=4, min_n=3, max_n=10)
print(ft_model.wv.most_similar('lamictal'))
ft_model.saveModel('fastTextModel.gensim')
#topics = ldamodel.print_topics(num_words=6)
#for topic in topics:
#    print(topic)

"""
pyLDAvis is designed to help users interpret the topics in a topic model
that has been fit to a corpus of text data. The package extracts information
from a fitted LDA topic model to inform an interactive web-based visualization.

Visualizing 10 topics:
"""
#load dictionary, corpus and model created above
dictionary = gensim.corpora.Dictionary.load('dictionary-med-tagged-complete.gensim')
corpus = pickle.load(open('corpus10.pkl', 'rb'))
lda = gensim.models.ldamodel.LdaModel.load('model_10-med-tagged-complete.gensim')


lda_display = pyLDAvis.gensim.prepare(lda, corpus, dictionary, sort_topics=False)
pyLDAvis.display(lda_display)