#####################################################################################
#XML API v.1                                                                        #
#Last updated 10.13.17                                                              #    
#- need to add function to parse xml to csv                                         #
#- will need to customize to parse ADP xml response                                 #
#####################################################################################

#Begin Imports#######################################################################
import requests
import logging
import xml.etree.ElementTree as ET
import csv
import sys
import io
import time
import itertools as IT
from xml.etree.ElementTree import ParseError
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
#End Imports##########################################################################
#Set default encoding#################################################################
reload(sys)
sys.setdefaultencoding('utf8')
######################################################################################

#Global Variables#####################################################################
fname='C:\\Users\\AM17060\\Desktop\\ADP Data\\names_last.csv' #modify as needed to complete query
outfile=open('ADP_Parsed.csv',"a")
logging.basicConfig(level=logging.DEBUG, filename='C:\\Users\\AM17060\\Desktop\\ADP Data\\parse_errrors.log')
base_url='http://www.reddit.com/r/volvo/search.xml?q=humira' #replace with ADP query string
writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
ua=UserAgent()
headers={'user-agent': ua.random}
#to manage xml parsing exceptions#####################################################
PY2 = sys.version_info[0] == 2
StringIO = io.BytesIO if PY2 else io.StringIO
tree=""
count=1
#End of Global Variable Defintions####################################################
# Function Defintions#################################################################
def parse_xml(data):
     return("")
######################################################################################
######################################################################################
#MAIN FUNCTION                                                                       #
#read names from file and store in list object 
with open(fname, 'rb') as f:
     reader=csv.reader(f)
     name_list=list(reader)
#iterate through list and concatenate name to API query     
     for n in name_list:
          name="".join(n)
          url=base_url + name
#make api call- delay used to prevent request from timing out
          time.sleep(10)
          response=requests.get(url)
          data= response.text
          bad_xml=BeautifulSoup(data,"xml")
     
#parse XML, iterate over child nodes and manage parsing exceptions
          try:
               root=ET.fromstring(data)
               for child in root:
                    print child.tag, child.attrib,child.text, child.items
#write bad xml to a file and log exceptions
          except ParseError as e:
               print "**************************************bad xml found**************************************************************"
               count+=1
               counter=str(count)
               with open('bad_xml' + counter +'.xml', 'w') as f:
                    f.write(response.text)
                    print e
                    logging.exception("Error:")
               continue

######################################################################################
#Parse XML Function                                                                  #
#def parse_xml(data):
#     try:
#          response = requests.get(url)
#          data=response.content
#          root=ET.fromstring(data)
#          print root.tag
#     except ParseError as e:
#          lineno, column = e.position
#          line = next(IT.islice(StringIO(data), lineno))
#          caret = '{:=>{}}'.format('^', column)
#          e.msg = '{}\n{}\n{}'.format(e, line, caret)
#          print e
#     return root

#parse_xml("")




#Main Function########################################################################

#for name in names:
#     response = requests.get(url+name)
#     tree = ET.fromstring(response.content,ET.XMLParser(encoding='utf-8'))
#     root=tree.getroot()


##############################################################################helpful function to covert XML to dataframe

#xml_data = open('/path/user_agents.xml').read() #Loading the raw XML data

#def xml2df(xml_data):
#    root = ET.XML(xml_data) # element tree
#    all_records = [] #This is our record list which we will convert into a dataframe
#    for i, child in enumerate(root): #Begin looping through our root tree
#        record = {} #Place holder for our record
#        for subchild in child: #iterate through the subchildren to user-agent, Ex: ID, String, Description.
#            record[subchild.tag] = subchild.text #Extract the text create a new dictionary key, value pair
#            all_records.append(record) #Append this record to all_records.
#    return pd.DataFrame(all_records) #return records as DataFrame
