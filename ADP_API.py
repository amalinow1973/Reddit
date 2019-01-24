import requests
import xml.etree.ElementTree as ET
import csv
import sys
reload(sys)
sys.setdefaultencoding('utf8')


###Global Variables

fname="text file containing list of officers"
outfile=open('ADP_Parsed.csv',"a")
base_url='http://www.reddit.com/r/volvo/search.xml?q=humira'
writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
# list object to hold list of names to complete API request
names=[]
data=requests.get(base_url)
print data.content

#read names from file and store in list object 
#with open(fname) as f:
#    names = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
#names = [x.strip() for x in names] 

#open .csv file for output


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
