#########################################################################################################################
#Text Tagger v.1                                                                                                        #
#lat updated 11/1/17                                                                                                    #
#need to add/try sentiment analysis and explore textblob and nltk capabilities more                                     #
#########################################################################################################################
#Begin imports
import nltk
from bs4 import BeautifulSoup
import pandas as pd
from nltk.corpus import stopwords
from nltk import Text
from nltk.text import ConcordanceIndex 
from nltk.tokenize import word_tokenize, sent_tokenize
import csv
import time
from textblob import TextBlob
from parse import *
#End imports
########################################################################################################################
#Global Variables#######################################################################################################
#from NLTK-used to remove non-word strings and stop list to remove words that are not of interest for the analysis
#tag terms- using pandas to store in dataframe, then converting to string so NLTK can tokenize
medication_file="E:/med_list.csv"
df2=pd.read_csv(medication_file,encoding='utf-8')
medications=df2.values
df3=pd.read_csv('surprise_words.csv',encoding='utf-8')
surprise_words=df3.values
#source text file to be analyzed
inputfile=r'E:\Medication_Tagged_Reddit_Data.csv'
#using pandas to read text values from multi-column source file (reddit data)
df=pd.read_csv(inputfile, sep='|',error_bad_lines=False,encoding='utf-8',nrows=10)
Tag_Word=df["Tag-Word"]

#title=df['Title']
Full_Text=df["Full_Text"]
#tcs=df['tcs']
#comments_string=str(comments)
surprise_list=[]
tag_list=[]
count=0
symptom_list=[]
sentence_list=[]
#End Global Variables###################################################################################################

#Main Function##########################################################################################################
########################################################################################################################
def concordance(ci, word, width=80, lines=25):
    """
    Rewrite of nltk.text.ConcordanceIndex.print_concordance that returns results
    instead of printing them. 

    See:
    http://www.nltk.org/api/nltk.html#nltk.text.ConcordanceIndex.print_concordance
    """
    half_width = (width - len(word) - 2) // 2
    context = width // 4 # approx number of words of context

    results = []
    offsets = ci.offsets(word)
    if offsets:
        lines = min(lines, len(offsets))
        for i in offsets:
            if lines <= 0:
                break
            left = (' ' * half_width +
                    ' '.join(ci._tokens[i-context:i]))
            right = ' '.join(ci._tokens[i+1:i+context])
            left = left[-half_width:]
            right = right[:half_width]
            results.append('%s %s %s' % (left, ci._tokens[i], right))
            lines -= 1

    return results

#open output file and write header
with open('Medication_Surprise_Tagged_Reddit_Data-Surprise.csv', 'w', encoding='utf-8') as outfile:
    fieldnames=['Surprise-Word','Sentence','Full_Text']
    writer=csv.DictWriter(outfile, delimiter='|', fieldnames=fieldnames, skipinitialspace=True)
    writer.writeheader()      
    #for word in medications:
    #    word="".join(word)
    #    tag_list.append(word)
    #    se=[]
    #    sentence=[]
    counter=0
    for s_word in surprise_words:
        s_word=sent_tokenize(str(s_word))
        s_word="".join(s_word)
        surprise_list.append(s_word)
        
    
    for row in df['Full_Text']:
        seen=[]
        sentence_list=[]
        word_list=[]
#        for sentence in sent_tokenize(str(row)):
#            sentence_list.append(sentence)
        seen.append(row)
        for word in word_tokenize(str(row)):
            word_list.append(word)
            for n in word_list:
                results=[]
                #print (n,surprise_list)
                for a in Tag_Word:
                
                    if a==n:
                        
                        print('!!!!!MATCHMATCHMATCH!!!!!!!',a, n)
                        tokens=word_tokenize(str(row))
                        text=nltk.text.ConcordanceIndex(tokens)
                        #text.ConcordanceIndex(text)
                        results.append(concordance(text,str(a)))
                        #results.append(text.concordance(str(a)))
                        #print(results)
                        #writer.writerow({'Surprise-Word':n,'Sentence':results})
                        seen.append(n)
                        continue
                    else:
                        continue
            
        #for word in word_tokenize(str(row)):          
#tokenize comments and add to list
            
        
            writer.writerow({'Surprise-Word':a,'Sentence':results})
            counter+=1
            continue
            #for n in surprise_list:
             ##  if ([x for x in suprise_list and x in sent]):    #print (n, sent)
               #     se.append(n)
                #    sentence.append(sent)
                    
                  #  continue
                #else:
                 #   continue
#iterate through list of side effects and prepare for tagging
        
print("analysis complete", "sentences analyzed:", counter)