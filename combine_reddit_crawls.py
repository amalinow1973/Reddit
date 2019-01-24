import pandas as pd
import xlrd
import sys
import csv
import os
reload(sys)

sys.setdefaultencoding('UTF8')
#Global variables#####################################################################
data=[]
rootdir="C:\\Users\\AM17060\\Desktop\\Reddit"
outfile="Reddit_Combined_Patient_Exp.csv"
idx=0
sheet_name="sheet name"
#read source files from directory and store in list###################################
for subdir, dirs, files in os.walk(rootdir):
	for file in files:
		excel_files=[]
		excel_files.append(os.path.join(subdir, file))
		
#iterate through list and read source data into dataframe#############################
		for ind_file in excel_files:
			worksheet=pd.read_csv(ind_file,sep='|')
#create second dataframe and insert filename (to use for filtering/traceability)######
			filename=pd.Series(file,excel_files)
			worksheet.insert(0,"Filename",file)
#insert content from spreadsheets into list object####################################
			data.insert(idx,worksheet)
##concatenate the content in the list into one dataframe##############################
results=pd.concat(data)
#write data to csv file###############################################################
results.to_csv(outfile,sep='|', header=True,encoding='utf-8')