# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 12:01:59 2019

@author: Andrew
"""
from random import randint
import random
import pandas as pd
import time
from faker import Faker
fake = Faker()
secure_random = random.SystemRandom()
"""
create variables for data set
"""
name=[]
address=[]
age=[]
income=[]
#for students, 'state_name' will need to be engineered from 'address'
state_name=[]
state_na=[]
#how much the person has spent on elective procedures
pat_paid_elec=[]
#list of chronic conditions with regional variation
conditions=['asthma','diabetes','high-blood-pressure','obesity','smoking','high-cholesterol']
ne_conditions=['asthma','diabetes','high-blood-pressure','obesity','smoking']
sw_conditions=['diabetes','diabetes', 'diabetes', 'obesity', 'obesity', 'obesity', 'smoking', 'smoking', 'high-blood-pressure']
out_conditions=['obesity', 'obesity', 'high-blood-pressure','high-blood-pressure']
northeast=['RI','CT','MA','NH','ME','VT']
southwest=['NM','AZ','TX','AR']
outlier_state=['FL']
y=[]
sys_tmstmp=[]
##
x=1
print (southwest)
##survey questions with 1-6 likert scale responses
q1=[]
q2=[]
q3=[]
q4=[]
q5=[]
condition=[]


"""
create outliers
"""
def createOutlier(integer):
    integer=random.uniform(1.5,3.3)*(integer)
    integer=int(integer)
    return integer

"""
Assign label
"""

def assignLabel(state,income,age,):
    a=income
    b=age
    d=str(state)
    high_prob=[0,1,1,1,1]
    med_prob=[0,0,1,1,1]
    low_prob=[0,0,0,0,0,0,0,0,0,1]
    random_selection=[0,1]
    ##high probabablity 
            
    if (a>175000).all():
        n=random.choice(high_prob)
        
   
    if (b<40).all():
        n=random.choice(high_prob)     
        
    elif d=='CT':
        n=random.choice(med_prob)
       
    elif(d=='FL'):
        print(d)
        n=random.choice(low_prob)
    
    else:
        n=random.choice(random_selection)
        
        
    return n


"""
create base records with outliers
"""
def createRecords(integer):
            
    for i in range(integer):
        income.append(randint(35000,250000))
        age.append(randint(18,85))
        address.append (fake.address())
        sys_tmstmp.append(str(time.ctime()).split(" ")[-2])
        q1.append(randint(0,5))
        q2.append(randint(0,5))
        q3.append(randint(0,5))
        q4.append(randint(0,5))
        q5.append(randint(0,5))
        name.append(fake.name())
        state_na.append(str(address).split(" ")[-2])
        #add geographic variance
        if [i for i in state_na if i in southwest]:
                base=randint(3200,4000)
                pat_paid_elec.append(base)
                condition.append(random.choice(sw_conditions))
                    
        if [i for i in state_na if i in northeast]:
                base=randint(6200,8000)
                pat_paid_elec.append(base)
                condition.append(random.choice(ne_conditions))
                    
        if [i for i in state_na if i in outlier_state]:
                base=randint(10000,15000)
                outlier=(createOutlier(base))
                pat_paid_elec.append(outlier)
                state_name.append(i)   
                condition.append(random.choice(out_conditions))
        else:
                base=randint(3200,8000)
                pat_paid_elec.append(base)
                condition.append(random.choice(conditions))
                continue
    
    df=pd.DataFrame()
    df['previously_purchased']=y
    df['name']=name
    df['address']=address
    df['age']=age
    df['income']=income
    df['sys_tmstmp']=sys_tmstmp
    ##survey questions with 1-5 likert scale responses
    df['q1']=q1
    df['q2']=q2
    df['q3']=q3
    df['q4']=q4
    df['likely_to_try_robot']=q5
    
    #commented for student dataset
    df['state']=state_na
    df['pat-paid-elec']=pd.Series(pat_paid_elec)
    df['condition']=pd.Series(condition)          
    return df    
"""
create data sets
"""
df1=createRecords(100000)
sample=createRecords(500)

"""
assign target
"""
for row in df1.iterrows():
    low_prob=[0,0,0,0,0,0,0,0,0,1]
    ##assign target value
    income=df1.iloc[:,4]
    condition=df1.iloc[:,13]
    age=df1.iloc[:,3] 
    state=df1.iloc[:,11]
    target=assignLabel(state,income,age)
    ##smokers will be very unlikely to purchase
    if 'smoking' in str(row):
        target=random.choice(low_prob)
        continue
    if (df1.at[row,'age'])<40:
        print (row)
    
    y.append(target)


df1['target']=y
df1.to_csv('project5_records.csv')
print ('record creation complete', "number of records created=", len(df1))







#df.to_csv("sample_survey_response_data.csv", encoding='utf-8')
    