# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 12:16:28 2019

word2vec to find similar constructs in the medication and surprise tagged posts and comments

"""

#imports
from gensim.test.utils import datapath
import nltk
from gensim.models import Word2Vec,KeyedVectors
import pandas as pd
from nltk.corpus import stopwords
import datetime
#data
#wv_from_bin = KeyedVectors.load_word2vec_format(datapath('E:\model.bin'), binary=True)
dt=datetime.datetime.now()
print("start-time:",dt)
data=pd.read_csv("surprise_subset.txt",sep='|', encoding='utf-8')
all_sentences=[]
all_words=[]
word2vec_results=pd.DataFrame()
med_list=pd.read_csv("E:/med_list.csv")
for index,row in data.iterrows():
    for sent in nltk.sent_tokenize(str(data.loc[index,"Results"])):
        all_sentences.append(sent)

for word in nltk.word_tokenize(str(all_sentences)):
        all_words.append(word)

print (len(all_words))


#remove stop words  
for i in range(len(all_words)):  
   all_words[i] = [w for w in all_words[i] if w not in stopwords.words('english')]
#analyze
word2vec = Word2Vec(tuple(all_words), min_count=2,workers=4)
word2vec.wv.save_word2vec_format('selective_model.bin')
vocabulary=word2vec.wv.vocab 
base_word=[]
sim_word=word2vec.wv.most_similar("lamictal")
print (sim_word)
sim_words=[]
for word in med_list:
    if word in vocabulary:
        base_word.append(word)
        sim_word=word2vec.wv.most_similar(str(word))
        sim_words.append(sim_word)
        continue
    else:
        continue
word2vec_results["base"]=pd.Series(base_word)
word2vec_results["similar"]=pd.Series(sim_words)
word2vec_results.to_csv("word2vec-results.csv", sep ='|',encoding='utf-8')
print("analysis complete: number of results:", len(word2vec_results)) 
print("end-time:",dt)
