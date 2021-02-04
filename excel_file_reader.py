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



def get_data (rootdir):
    
    """ Crawls all subdirectories and files from passed parent directory arg
    Reads all .xlsx files (and all worksheets) combines into single dataframe
    Writes combined dataframe to file.  Returns the combined dataframe """
    
    # Output file parameters
    timestr = time.strftime("%Y%m%d-%H%M%S")
    outfile_name="combined_data_dictionary_data_processed-"
    extension=".csv"
    
    # list to hold dataframes
    worksheets=[]
    
    # crawl directory for .xlsx files
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            excel_files=[]
            excel_files.append(os.path.join(subdir, file))
            for ind_file in excel_files:
                print (ind_file)
                # Here the result is a dictionary of DataFrames
                dct = pd.read_excel(ind_file, sheet_name=None)
                # Process each DataFrame from this dictionary
                for df in dct.values():
                    # multiple worksheets to be saved as dataframe
                    data=pd.DataFrame()
                    data = pd.concat([data,df]).drop_duplicates(keep=False)
                    worksheets.append(data)
                    
    # concatenate the list of datframes into one dataframe
    results=pd.concat(worksheets)
    # print data summary metrics to console
    print ("number of rows processed:" + str(len(results)), "from:"+ str(len(worksheets))+ " worksheets")
    
    # write data to csv file
    # results.to_csv(outfile_name+timestr+extension,encoding='utf-8')
    return results

	

	

