# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 10:05:34 2019

@author: Andrew
"""
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from sklearn.manifold import TSNE
import time
from pandas.io.json import json_normalize
"""
global variables
"""
df=pd.read_json('E://word2vec-most-similar-complete.json')
term= df['term']
print (term)
#terms=df['term']
#related=df['related']
#df.set_index('term', inplace=True)

df.loc[df['term'][:'Aceon']
print (df)




    for label, x, y in zip(word_labels, x_coords, y_coords):
        plt.annotate(label, xy=(x, y), xytext=(0, 0), textcoords='offset points')
        plt.xlim(x_coords.min()+0.00005, x_coords.max()+0.00005)
        plt.ylim(y_coords.min()+0.00005, y_coords.max()+0.00005)
        plt.show()
        

display_closestwords_tsnescatterplot(model, 'abilify')