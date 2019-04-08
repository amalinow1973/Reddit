# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 12:41:55 2019

@author: Andrew
"""
import nltk
import pandas as pd
import os
import argparse
import time
import gensim.models
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.datasets import fetch_20newsgroups
from sklearn.manifold import TSNE
import bokeh.plotting as bp
from bokeh.plotting import save
from bokeh.models import HoverTool
import spacy
nlp=spacy.load('en')
from spacy.lang.en import English
parser = English()
en_stop = set(nltk.corpus.stopwords.words('english'))
path="E://source/"



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

def prepare_text_for_lda(text):
    tokens = tokenize(text)
    tokens = [token for token in tokens if len(token) > 4]
    tokens = [token for token in tokens if token not in en_stop]
    #tokens = [get_lemma(token) for token in tokens]
    return tokens

data=prepare_text_for_lda(data)
n_topics = 10
n_iter = 15
n_top_words = 20
threshold = .99
data=pd.read_csv("E:/med_tagged_complete.txt", sep="|",encoding='utf-8')
t0 = time.time()
cvectorizer = CountVectorizer(stop_words='english')
cvz = cvectorizer.fit_transform(data)
dictionary = gensim.corpora.Dictionary(data)
corpus = [dictionary.doc2bow(text) for text in data]
NUM_TOPICS = 10
ldamodel = gensim.models.LdaMulticore(corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=15, workers=3)

lda_model = gensim.models.LDA(num_topics=20, workers=3)
X_topics = lda_model.fit_transform(cvz)
lda_model.save('lda-model.gensim')
t1 = time.time()
print ('LDA training done; took',(t1-t0)/60)
_idx = np.amax(X_topics, axis=1) > threshold  # idx of news that > threshold
_topics = X_topics[_idx]

num_example = len(_topics)

  # t-SNE: 50 -> 2D
tsne_model = TSNE(n_components=2, verbose=1, random_state=0, angle=.99,
                    init='pca')
tsne_lda = tsne_model.fit_transform(_topics[:num_example])

# find the most probable topic for each news
lda_keys = []
for i in xrange(_topics.shape[0]):
    _lda_keys += _topics[i].argmax(),

  # show topics and their top words
topic_summaries = []
topic_word = lda_model.topic_word_  # get the topic words
vocab = cvectorizer.get_feature_names()
for i, topic_dist in enumerate(topic_word):
    topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n_top_words+1):-1]
    topic_summaries.append(' '.join(topic_words))

  # 20 colors
colormap = np.array([
    "#1f77b4", "#aec7e8", "#ff7f0e", "#ffbb78", "#2ca02c",
    "#98df8a", "#d62728", "#ff9896", "#9467bd", "#c5b0d5",
    "#8c564b", "#c49c94", "#e377c2", "#f7b6d2", "#7f7f7f",
    "#c7c7c7", "#bcbd22", "#dbdb8d", "#17becf", "#9edae5"
  ])

  # plot
title = "[20 newsgroups] t-SNE visualization of LDA model trained on {} news, " \
          "{} topics, thresholding at {} topic probability, {} iter ({} data " \
          "points and top {} words)".format(
    X_topics.shape[0], n_topics, threshold, n_iter, num_example, n_top_words)

plot_lda = bp.figure(plot_width=1400, plot_height=1100,
                       title=title,
                       tools="pan,wheel_zoom,box_zoom,reset,hover,previewsave",
                       x_axis_type=None, y_axis_type=None, min_border=1)

plot_lda.scatter(x=tsne_lda[:, 0], y=tsne_lda[:, 1],
                   color=colormap[_lda_keys][:num_example],
                   source=bp.ColumnDataSource({
                     "content": news[:num_example],
                     "topic_key": _lda_keys[:num_example]
                     }))

  # randomly choose a news (in a topic) coordinate as the crucial words coordinate
topic_coord = np.empty((X_topics.shape[1], 2)) * np.nan
for topic_num in _lda_keys:
    if not np.isnan(topic_coord).any():
      break
    topic_coord[topic_num] = tsne_lda[_lda_keys.index(topic_num)]

  # plot crucial words
for i in xrange(X_topics.shape[1]):
    plot_lda.text(topic_coord[i, 0], topic_coord[i, 1], [topic_summaries[i]])

  # hover tools
hover = plot_lda.select(dict(type=HoverTool))
hover.tooltips = {"content": "@content - topic: @topic_key"}

save(plot_lda, '20_news_tsne_lda_viz_{}_{}_{}_{}_{}_{}.html'.format(
    X_topics.shape[0], n_topics, threshold, n_iter, num_example, n_top_words))

t2 = time.time()
print ('\n>>> whole process done; took {} mins\n',(t2 - t0))
