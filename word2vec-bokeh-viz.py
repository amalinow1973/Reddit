# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 16:24:11 2019
https://botfactory.in/2018/07/04/creating-word-vectors-with-word2vec-and-reduce-dimensionality-using-tsne-and-visualizing-it-using-bokeh/
@author: Andrew
"""

import nltk
from nltk import word_tokenize, sent_tokenize
import gensim
from gensim.models.word2vec import Word2Vec
from sklearn.manifold import TSNE
import pandas as pd
from bokeh.io import output_notebook
from bokeh.plotting import show, figure, save

model = gensim.models.KeyedVectors.load_word2vec_format("selective_reddit_model.bin")
vocab=model.wv.vocab
X = model[model.wv.vocab]
tsne = TSNE(n_components=2, n_iter=1000)
X_2d = tsne.fit_transform(X)
X_2d[0:5]
# create DataFrame for storing results and plotting
coords_df = pd.DataFrame(X_2d, columns=['x','y'])
coords_df['token'] = model.wv.vocab.keys()
coords_df.head()
coords_df.to_csv('reddit_tsne.csv', index=False)
coords_df = pd.read_csv('reddit_tsne.csv')
_ = coords_df.plot.scatter('x', 'y', figsize=(12,12), marker='.', s=10, alpha=0.2)
subset_df = coords_df.sample(n=5000)
p = figure(plot_width=800, plot_height=800)
_ = p.text(x=subset_df.x, y=subset_df.y, text=subset_df.token)
show(p)