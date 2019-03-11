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

# Load pre-trained Word2Vec model.
df=pd.read_csv("E:\\Reddit_Drug_Search_Terms.txt", sep=" ")
medication_list=df['Name']
print (medication_list)
model = gensim.models.KeyedVectors.load_word2vec_format("E:/reddit_model.bin")
vocab=model.wv.vocab
similar_terms=[]
base_term=[]
for term in medication_list:
    print (term)
    if term in vocab:
        similar_terms.append(model.wv.most_similar(term, topn=3,))
        base_term.append(term)
        continue
    else:
        continue

df=pd.DataFrame()
df['term']=base_term
df['related']=similar_terms
df.to_csv("word2vec-most-similar-complete.csv", encoding="utf-8", sep ="|")
print ("analysis complete: # of rows in file=",len(df))
    
"""
Plot the results
"""
def tsne_plot(model):
    "Creates TSNE model and plots it"
    labels = []
    tokens = []

    for word in model.wv.vocab:
        tokens.append(model[word])
        labels.append(word)
    
    tsne_model = TSNE(perplexity=40, n_components=2, init='pca', n_iter=2500, random_state=23)
    new_values = tsne_model.fit_transform(tokens)

    x = []
    y = []
    for value in new_values:
        x.append(value[0])
        y.append(value[1])
        
    plt.figure(figsize=(16, 16)) 
    for i in range(len(x)):
        plt.scatter(x[i],y[i])
        plt.annotate(labels[i],
                     xy=(x[i], y[i]),
                     xytext=(5, 2),
                     textcoords='offset points',
                     ha='right',
                     va='bottom')
    plt.show()
tsne_plot(model)    