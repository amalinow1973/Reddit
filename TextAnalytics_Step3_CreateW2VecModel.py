# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 12:16:28 2019

word2vec to find similar constructs in the medication and surprise tagged posts and comments

"""

#imports
#from gensim.test.utils import datapath
import nltk
from gensim.models import Word2Vec
#import pandas as pd
from nltk.corpus import stopwords
import datetime
#data
#wv_from_bin = KeyedVectors.load_word2vec_format(datapath('E:\model.bin'), binary=True)
dt=datetime.datetime.now()
print("start-time:",dt)
data=open("E:/surprise_subset.txt", encoding='utf-8').read()
all_sentences=[]
all_words=[]
all_sentences = nltk.sent_tokenize(data)

all_words = [nltk.word_tokenize(sent) for sent in all_sentences]
print(len(all_words))
#remove stop words  
for i in range(len(all_words)):  
   all_words[i] = [w for w in all_words[i] if w not in stopwords.words('english')]
#analyze
word2vec = Word2Vec(all_words,size=500, min_count=5,workers=4)
word2vec.wv.save_word2vec_format('selective_reddit_model.bin')
vocabulary = word2vec.wv.vocab  
print(vocabulary)  
sim_word=word2vec.wv.most_similar("lamictal")
print(sim_word)