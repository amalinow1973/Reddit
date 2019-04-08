# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 10:00:34 2019
assigns similiarity words to all terms (medications and conditions) in 
the list of terms used to source reddit data
@author: Andrew
"""

import gensim
import pandas as pd
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import bokeh.plotting as bp
from bokeh.models import HoverTool, BoxSelectTool
from bokeh.plotting import figure, show, output_notebook
from sklearn.manifold import TSNE

# Load pre-trained Word2Vec model.
df=pd.read_csv("E:\\Reddit_Drug_Search_Terms.txt", sep=" ")
medication_list=df['Name']

model = gensim.models.KeyedVectors.load_word2vec_format("selective_reddit_model.bin")
vocab=model.wv.vocab
similar_terms=[]
base_term=[]
for term in medication_list:
    
    if term in vocab:
        similar_terms.append(model.wv.most_similar(term, topn=3,))
        base_term.append(term)
        continue
    else:
        continue

df=pd.DataFrame()
df['term']=base_term
df['related']=similar_terms
df.to_csv("word2vec-most-similar-complete.json", sep='|')
print ("analysis complete: # of rows in file=",len(df))
    
"""
Plot the results
"""
# defining the chart
output_notebook()
plot_tfidf = bp.figure(plot_width=700, plot_height=600, title="A map of 10000 word vectors",
    tools="pan,wheel_zoom,box_zoom,reset,hover,previewsave",
    x_axis_type=None, y_axis_type=None, min_border=1)

# getting a list of word vectors. limit to 10000. each is of 200 dimensions
word_vectors = [model[w] for w in model.wv.vocab.keys()[:5000]]

# dimensionality reduction. converting the vectors to 2d vectors

tsne_model = TSNE(n_components=2, verbose=1, random_state=0)
tsne_w2v = tsne_model.fit_transform(word_vectors)

# putting everything in a dataframe
tsne_df = pd.DataFrame(tsne_w2v, columns=['x', 'y'])
tsne_df['words'] = model.wv.vocab.keys()[:5000]

# plotting. the corresponding word appears when you hover on the data point.
plot_tfidf.scatter(x='x', y='y', source=tsne_df)
hover = plot_tfidf.select(dict(type=HoverTool))
hover.tooltips={"word": "@words"}
show(plot_tfidf)