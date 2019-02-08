#########################################################################################################################
#Text Tagger v.1                                                                                                        #
#lat updated 11/1/17                                                                                                    #
#need to add/try sentiment analysis and explore textblob and nltk capabilities more                                     #
#########################################################################################################################
#Begin imports
import nltk
import pandas as pd
from nltk.text import ConcordanceIndex 
from nltk.tokenize import word_tokenize, sent_tokenize
import time

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
inputfile=r'E:\all_posts_sorted.csv'
#using pandas to read text values from multi-column source file (reddit data)
df=pd.read_csv(inputfile, sep='|',error_bad_lines=False,encoding='utf-8',low_memory=False,nrows=100)



title=df['Title']
Full_Text=df["full_text"]
tcs=df['tcs']
#comments_string=str(comments)
surprise_list=[]
tag_list=[]
count=0
symptom_list=[]
sentence_list=[]
med_list=[]


#End Global Variables###################################################################################################

#Main Function##########################################################################################################
########################################################################################################################




def concordance(ci, word, width=100, lines=40):
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
def textTagger():
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
    for s_word in surprise_words:
        s_word=sent_tokenize(str(s_word))
        s_word="".join(s_word)
        surprise_list.append(s_word)
        
    for row in df['full_text']:
        #print (row)
        time.sleep(1)
        results=[]
        seen=[]
        word_list=[]
        found=[]
        for word in word_tokenize(str(row)):
            word_list.append(word)
        #for med in word_tokenize(str(medications)):
         #   med_list.append(med)
            for n in word_list:
                          
                for a in word_tokenize(str(medications)):
            #a=re.sub('[\W_]+', '', a)
                    #print (a)    
                    if a == n and a not in seen:                       
                       found.append(a)
                       tokens=word_tokenize(str(row))
                       text=nltk.text.ConcordanceIndex(tokens)
                       #print (a,n,text)
                       results.append(concordance(text,str(a)))
                       seen.append(a)
                       print (results)
                       continue
                    else:
                       continue
        counter+=1
        print (counter)
       
        
    df_results['Tag-Word']=found
    df_results['Sentence']=pd.Series(results)
    df_results.dropna()
    df_results.index.name='Index'
    #print(df_results)
    df_results.to_csv('med_tagged_step2.csv', sep='|')
    return df_results

results=textTagger()


print("analysis complete", "sentences analyzed:" ,len(results),results.head())