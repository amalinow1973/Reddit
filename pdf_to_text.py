import pypdf
import sys
import os
reload(sys)

sys.setdefaultencoding('UTF8')
#Global variables#####################################################################
rootdir="C:\\Users\\AM17060\\Desktop\\EHR PDFs"
outdir="C:\\Users\\AM17060\\Desktop\\EHR TXT"

#read source PDF files from directory and write out txt files#########################
for files in os.walk(rootdir):
	print files
		
		