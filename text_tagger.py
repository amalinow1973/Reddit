################################################
#Text Tagger v.1                               #
################################################
import pandas as pd
from nltk.corpus import stopwords
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import csv
import numpy
side_effects_file=r'E:\Demo Data Sets\Side Effects.csv'
inputfile=r'E:\Demo Data Sets\reddit_prescription_medications.csv'
df=pd.read_csv(inputfile, sep='|')
headers=df.columns.values
comments=df["Comments"].values
comments_string=str(comments)
df2=pd.read_csv(side_effects_file, sep=",")
side_effects=df2.values
stop_words=set(stopwords.words("english"))
#open output file and write header
with open ('Text_Tagged_Reddit_Data.csv', 'wb') as f:
     fieldnames=['Side-effect','Comment']
     writer=csv.DictWriter(f, delimiter='|', fieldnames=fieldnames, skipinitialspace=True)
     writer.writeheader()
#tokenize side-effects and add to list
for word in side_effects:
     tag_list=[]
     word="".join(word)
     #print word
     word=nltk.sent_tokenize(word)
     tag_list.append(word)

se=[]
sentence=[]
#tokenize comments
for sent in sent_tokenize(comments_string):
     #print sent
     for n in tag_list:
          
          if str(n) in sent:
               print n, sent
               se.append(n)
               sentence.append(sent)
               writer.writerow({'Side-effect':se, 'Comment':sentence})
               
          #else:
           #    continue
          
     
                    
                    
     #words=word_tokenize(sent)
     #filtered_sentence=[w for w in words if not w in stop_words]
     #print (filtered_sentence)
     #if n== (nltk.sent_tokenize(comments))
     


#tokens=nltk.word_tokenize(side_effects_list)
#print tokens
#text=nltk.word_tokenize(comments)

     
