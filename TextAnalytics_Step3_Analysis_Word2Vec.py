# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 12:16:28 2019

word2vec to find similar constructs in the medication and surprise tagged posts and comments

"""

#imports

import nltk
from gensim.models import Word2Vec
import pandas as pd
from nltk.corpus import stopwords

#data

data=pd.read_csv('low-comments.txt',sep='|', encoding='utf-8')
print (data.columns)
all_sentences=[]
all_words=[]
word2vec_results=pd.DataFrame()
med_list=pd.read_csv("E:/med_list.csv")
for index,row in data.iterrows():
    for sent in nltk.sent_tokenize(str(data.loc[index,"full_text"])):
        all_sentences.append(sent)

for word in nltk.word_tokenize(str(all_sentences)):
        all_words.append(word)

print (len(all_words))


#remove stop words  
for i in range(len(all_words)):  
   all_words[i] = [w for w in all_words[i] if w not in stopwords.words('english')]
#analyze
word2vec = Word2Vec(all_words, min_count=2,workers=4)
vocabulary=word2vec.wv.vocab  
sim_word=word2vec.wv.most_similar("abilify")
base_word=[]
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

