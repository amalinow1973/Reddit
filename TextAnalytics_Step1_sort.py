#Text Analytics-step 1 sort and split
#last updated 02/04/19

#begin imports

import pandas as pd
import csv

#end imports
csv.register_dialect('pipe_delimited', delimiter='|', skipinitialspace=True,quoting=2,escapechar='~',doublequote=False)
csv.field_size_limit(2147483647)
#global variables
medication_name_file="E:\\Reddit_Drug_Search_Terms.csv"
source_data_file="E:\\reddit_opioids.csv"
## csv
outfile=open('filtered_data.csv','a',encoding='utf-8',errors='ignore')
fieldnames=["term","Post Date","Post","tcs"]
writer=csv.DictWriter(outfile, delimiter='|', fieldnames=fieldnames, skipinitialspace=True)
import sys
sys.stdout.encoding.encode('utf-8')

##data

df=pd.read_csv(source_data_file, header=None, sep="|", names=["key","id",'Title',"Post","extracted","Post Date","Meta","noun_phrases","points","Total_Comments","Comments","Post City","latlon"], engine='python')

###combine text fields into single column and delimit for later use
df['full_text']=df["Title"].map(str)+df["Post"]
df['full_text']=df['full_text'].map(str)+df["Comments"]


original_df=pd.DataFrame(df)
med_terms=pd.read_csv(medication_name_file,encoding='utf-8')
terms=med_terms["Medication"]
filtered_df=pd.DataFrame()
filtered_post=[]
filtered_term=[]
post=df["Post"]
title=df["Title"]

df.drop(columns=["key","id","Post City","latlon","Post","Comments"], axis=1, inplace=True)
df.fillna(0, inplace=True)
df['Total_Comments']=df['Total_Comments'].apply(lambda x: pd.to_numeric(x, errors='coerce')).fillna(0)
df['tcs']=df["Total_Comments"].astype(str).astype(float).astype(int)
tcs=df['tcs']
title=[]

##drop columns
df.set_index('Title',inplace=True)
df.sort_values(by=['Total_Comments'],ascending=False, inplace=True)
df.to_csv("all_posts_sorted.csv")
#create high and low comment dfs
high_comments=df['tcs']>10
df_high_comments=df[high_comments]
low_comments=df['tcs']<=10
df_low_comments=df[low_comments]


##look at results
df_high_comments.to_csv("high-comments.csv", columns=['full_text','tcs','Post Date'])
df_low_comments.to_csv("low-comments.csv", columns=['full_text','tcs','Post Date'])       
print('total number of posts', len(df))
print("number of posts in high:", len(df_high_comments))
print("number of posts in low:", len(df_low_comments))

