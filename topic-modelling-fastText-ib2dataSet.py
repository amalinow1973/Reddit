# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 10:10:14 2019
https://shuaiw.github.io/2016/12/22/topic-modeling-and-tsne-visualzation.html
@author: Andrew
"""
from sklearn.manifold import TSNE
import pickle
from nltk.stem.wordnet import WordNetLemmatizer
import nltk
from nltk.corpus import wordnet as wn
import gensim 
import glob2
import os
import random
import spacy
nlp=spacy.load('en')
from spacy.lang.en import English
from gensim.models import FastText
import numpy as np
import pandas as pd
from bokeh.models import ColumnDataSource, LabelSet
from bokeh.io import push_notebook, show, output_notebook
from bokeh.plotting import figure

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
pickle.dump(corpus, open('corpusib2.pkl', 'wb'))
dictionary.save('dictionaryib2.gensim')

"""
train and save an LDA model
use NUM_TOPICS variable to determine the number of topics for the model, and num_words parameter for how much to show
"""
#NUM_TOPICS = 10

ft_model = FastText((text_data), size=100, window=5, min_count=150, workers=4, min_n=3, max_n=10)
ft_model.save('ft-ib2-model.gensim')
#print(ft_model.wv.most_similar('heart attack'))
ft_model.saveModel('ib2.gensim')
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
X = []
for word in ft_model.wv.vocab:
    X.append(ft_model.wv[word])
 
X = np.array(X)

print("Computed X: ", X.shape)
X_embedded = TSNE(n_components=2, n_iter=250, verbose=2).fit_transform(X)
print("Computed t-SNE", X_embedded.shape)
 
df = pd.DataFrame(columns=['x', 'y', 'word'])
df['x'], df['y'], df['word'] = X_embedded[:,0], X_embedded[:,1], ft_model.wv.vocab
 
source = ColumnDataSource(ColumnDataSource.from_df(df))
labels = LabelSet(x="x", y="y", text="word", y_offset=8,
                  text_font_size="8pt", text_color="#555555",
                  source=source, text_align='center')
 
plot = figure(plot_width=600, plot_height=600)
plot.circle("x", "y", size=12, source=source, line_color="black", fill_alpha=0.8)
plot.add_layout(labels)
show(plot, notebook_handle=True)