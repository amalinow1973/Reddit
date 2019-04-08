#########################################################################################################################
#Text Tagger v.1                                                                                                        #
#lat updated 11/1/17                                                                                                    #
#need to add/try sentiment analysis and explore textblob and nltk capabilities more                                     #
#########################################################################################################################
#Begin imports
from bs4 import BeautifulSoup
import pandas as pd
from nltk.corpus import stopwords
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import csv
import time
from textblob import TextBlob
from parse import *
#End imports
########################################################################################################################
#Global Variables#######################################################################################################
#from NLTK-used to remove non-word strings and stop list to remove words that are not of interest for the analysis
word_list = words.words()
stop_words=set(stopwords.words("english"))
#tag terms- using pandas to store in dataframe, then converting to string so NLTK can tokenize
medication_file="E:/med_list.csv"
df2=pd.read_csv(medication_file)
medications=df2.values
df3=pd.read_csv('surprise_words.txt')
suprise_words=df3.values


#source text file to be analyzed
inputfile=r'E:\all_posts_sorted.csv'
#using pandas to read text values from multi-column source file (reddit data)
df=pd.read_csv(inputfile, sep=',',error_bad_lines=False,encoding='utf-8')
headers=df.columns.values
title=df['Title']
comments=df['Title'].map(str)+df["full_text"]
tcs=df['tcs']
comments_string=str(comments)
surprise_list=[]
tag_list=[]
count=0
symptom_list=[]
sentence_list=[]
#End Global Variables###################################################################################################

#Main Function##########################################################################################################
########################################################################################################################
#open output file and write header
with open('Medication_Surpruse_Tagged_Reddit_Data.csv', 'w', encoding='utf-8') as outfile:
    fieldnames=['Tag-Word','Surprise-Word','Sentence','Full_Text']
    writer=csv.DictWriter(outfile, delimiter='|', fieldnames=fieldnames, skipinitialspace=True)
    writer.writeheader()      
    for word in medications:
        word="".join(word)
        tag_list.append(word)
        se=[]
        sentence=[]
        counter=0
    for s_word in surprise_list:
        s_word="".join(word)
        surprise_list.append(s_word)
    
    
    for row in df['full_text']:
        sentence_list=[]
        row=BeautifulSoup(str(row))
        for script in row(["script","style"]):
            script.extract()
            row=row.text
           
        for sent in sent_tokenize(str(row)):
            sentence_list.append(sent)
            
        #for word in word_tokenize(str(row)):          
#tokenize comments and add to list
            #print (sent)
            counter+=1
            for n in tag_list:
                #print (sent)
                if n in sent:
                    for s in surprise_list:
                        if s in sent:    #print (n, sent)
                            se.append(n)
                            sentence.append(sent)
                            writer.writerow({'Tag-Word':n,'Surprise-Word':s,'Sentence':sent, 'Full_Text':row})
                            continue
                        else:
                            continue
                else:
                    continue
#iterate through list of side effects and prepare for tagging
        
print("analysis complete", "sentences analyzed:", counter)