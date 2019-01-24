import pandas as pd
import xlrd
import numpy as np
import sys
import csv
import openpyxl
import os
reload(sys)

sys.setdefaultencoding('UTF8')
#Global variables-------------------------------------------------
data=[]
rootdir="C:\\Users\\AM17060\\Desktop\\Exported_General_Ledgers"
outfile="parsed_data_8_11_17.csv"
idx=0
sheet_name="sheet name"
#read source files from directory and store in list-------------------------------------------------
for subdir, dirs, files in os.walk(rootdir):
	for file in files:
		excel_files=[]
		excel_files.append(os.path.join(subdir, file))
		for ind_file in excel_files:
			print ind_file
			worksheet=pd.read_excel(io=ind_file,worksheet=sheet_name)
			data.insert(idx,worksheet)
			data.append(worksheet)
	
##concatenate the dataframes in the list into one dataframe	
results=pd.concat(data)
print results
#write data to csv file
results.to_csv(outfile,encoding='utf-8')





	

	

