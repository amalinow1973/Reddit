#Text Analytics v.1
#last updated 11/28/17

#begin imports
from geotext import GeoText
import geocoder
from nltk import word_tokenize, sent_tokenize
from textblob import TextBlob
from nltk.corpus import stopwords
from nltk.corpus import words
import pandas as pd
#end imports

#global variables
word_list = words.words()
stop_words=set(stopwords.words("english"))
medication_name_file="E:\\Reddit_Drug_Search_Terms.csv"
source_data_file="E:\\reddit.csv"
enriched_data=pd.DataFrame()
medication_tag=[]

source_data=pd.read_csv(source_data_file, header=None, sep="|", names=['Id','Title','Post','Post Words','Post_Noun_Phrases','Post Date','Meta','Comments',"Total Comments","Points"])
source_data=pd.DataFrame(source_data)
medication_tag=pd.read_csv(medication_name_file,header=None)
tagged_post={}
#prepare post_words for tagging
post_words=source_data['Post Words']
for n in post_words:
   
    post_words=[word for word in post_words if word not in stopwords.words('english')]
for n in medication_tag:
    if str(n) in post_words:
        taggedPost[post]=n
        print tagged_post


