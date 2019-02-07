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
df=pd.read_csv(inputfile, sep='|',error_bad_lines=False,encoding='utf-8',nrows=1)
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
#df_results=pd.DataFrame()
#End Global Variables###################################################################################################

#Main Function##########################################################################################################
########################################################################################################################




def concordance(ci, word, width=100, lines=25):
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
    #    word="".join(word)
    #    tag_list.append(word)
    #    se=[]
    #    sentence=[]
    counter=0
    results=[]
    for s_word in surprise_words:
        s_word=sent_tokenize(str(s_word))
        s_word="".join(s_word)
        surprise_list.append(s_word)
        
    for row in df['Full_Text']:
        seen=[]
        word_list=[]
        for word in word_tokenize(str(row)):
           word_list.append(word)
           for n in word_list:
                    
               for a in Tag_Word:
                   if a==n:                       
                       tokens=word_tokenize(str(row))
                       text=nltk.text.ConcordanceIndex(tokens)
                       results.append(concordance(text,str(a)))
                       seen.append(n)
                           # print (results)
                       continue
                   else:
                       continue
           counter+=1
           continue
        
    df_results['Tag-Word']=Tag_Word
    df_results['Sentence']=pd.Series(results)
    df_results.dropna()
    df_results.index.name='Index'
    print(df_results)
    df_results.to_csv('null_dropped.csv', sep='|')
    return df_results

results=textTagger()


print("analysis complete", "sentences analyzed:" ,len(results),results.head())