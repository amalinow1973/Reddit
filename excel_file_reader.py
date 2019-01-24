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
source_file_directory="C:/Users/AM17060/Desktop/Exported_General_Ledgers"
outfile="parsed_data_from_original.csv"
idx=0
sheet_name="sheet name"
#read source data from Excel file-------------------------------------------------
for excel_file in source_file_directory:
	worksheet=pd.read_excel(io=excel_file,worksheet=sheet_name)
	worksheet.insert(idx,sheet_name,sheet)
	data.append(worksheet)
	print sheet
#store each sheet as a dataframe--------------------------------------------------
frames=xl.sheet_names

#write data to csv file
results.to_csv(outfile,encoding='utf-8')





	

	

