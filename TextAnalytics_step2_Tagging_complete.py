#########################################################################################################################
#Text Tagger v.1                                                                                                        #
#lat updated 11/1/17                                                                                                    #
#need to add/try sentiment analysis and explore textblob and nltk capabilities more                                     #
#########################################################################################################################
#Begin imports
import nltk
import pandas as pd
from nltk.text import ConcordanceIndex 
from nltk.tokenize import word_tokenize


#End imports
########################################################################################################################
#Global Variables#######################################################################################################
#from NLTK-used to remove non-word strings and stop list to remove words that are not of interest for the analysis
#tag terms- using pandas to store in dataframe, then converting to string so NLTK can tokenize
medication_file="E:/med_list.csv"
df2=pd.read_csv(medication_file,encoding='utf-8')
medications=df2.values
df_results=pd.DataFrame()
df3=pd.read_csv('surprise_words.csv',encoding='utf-8')
surprise_words=df3.values
#source text file to be analyzed
inputfile=r'E:\reddit_opioids.csv'
#using pandas to read text values from multi-column source file (reddit data)
df=pd.read_csv(inputfile, sep='|',error_bad_lines=False,encoding='utf-8',low_memory=False,
               names=["key","id",'Title',"Post","extracted","Post Date","Meta","noun_phrases","points","Total_Comments","Comments","Post City","latlon"],
               nrows=1000)

post=df['Post']
title=df['Title']
comments=df['Comments']
surprise_list=[]
tag_list=[]
count=0
symptom_list=[]
sentence_list=[]
med_list=[]


#End Global Variables###################################################################################################

#Main Function##########################################################################################################
########################################################################################################################

def concordance(ci, word, width=500, lines=200):
    """
    Rewrite of nltk.text.ConcordanceIndex.print_concordance that returns results
    instead of printing them. 
    
    adjust width and lines parameters to control how much text is returned around the word
    of interest

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
def textTaggerMeds():
    """
    tags reddit title-post-comment fields with medication names and 'surprise' words
    write results to file and returns dataframe for additional analysis
    Need to update to include 'surprise words'
    
    """
    df_results=pd.DataFrame()
          
    #for word in medications:
     ##  print (m_word)
       # med_list.append(m_word)
    #    se=[]
    #    sentence=[]
    counter=0
    results=[]
    title=[]
    found=[]
    #for s_word in surprise_words:
     ### surprise_list.append(s_word)
        
    for index,row in df.iterrows():
               
        for word in word_tokenize(str(df.loc[index,"Post"])):
            if word in medications:        
                found.append(word)
                title.append(df.loc[index,'Title'])
                results.append(df.loc[index,'Post'])
            else:
                continue
        for word in word_tokenize(str(df.loc[index,"Comments"])):   
            if word in medications:
                found.append(word)
                title.append(df.loc[index,'Title'])
                results.append(df.loc[index,'Comments'])  
            else:
                continue
           
        continue  
    
    counter+=1
   # print (counter)
    df_results['Tag-Word']=pd.Series(found)   
    df_results['Title']=pd.Series(title)
    df_results['Results']=pd.Series(results)
    df_results.dropna()
    df_results.index.name='Index'
    df_results.to_csv('med_tagged_complete.csv', sep='|')
    return df_results



results=textTaggerMeds()
surprise_tag=[]
for index,row in results.iterrows():
    for word in word_tokenize(str(results.loc[index,"Results"])):
        
        if word in surprise_words:
        
            tokens=word_tokenize(str(results.loc[index,"Results"]))
            text=nltk.text.ConcordanceIndex(tokens)
            surprise_tag.append(concordance(text,str(word)))
        else:
            continue
results['surprise']=pd.Series(surprise_tag)
results.dropna()
results.to_csv('surprise_subset.csv',sep='|')  
   # for word in word_tokenize(str(comments)):

print("analysis complete", "sentences analyzed:" ,len(results))