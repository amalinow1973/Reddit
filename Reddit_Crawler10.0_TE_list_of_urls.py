#################################################################################################################################
# Reddit Crawler v8.0                                                                                                           #
# Last updated  01/21/19                                                                                                        #
# Crawler now reads from a list of urls (currently 4456 medical related terms including symptoms, medications and conditions)   #
# Added noun group extraction (for posts)           															   #
# Added separate variable for post words and remove stop-words
# Set requests to ignore invalid ssl certs
# To-Do:                                                                                                                        #
#	-sentiment analysis                                                                                                        #
#    -turn geo-coding back on                                                                                                   #
#################################################################################################################################
import nltk
import requests
import re
from bs4 import BeautifulSoup
import time
from fake_useragent import UserAgent
import datetime
import csv
from geotext import GeoText
import geocoder
import nltk
from nltk import word_tokenize, sent_tokenize
from textblob import TextBlob
from nltk.corpus import stopwords
from nltk.corpus import words
import pandas
from requests import ConnectionError
#nltk.download('words')
#nltk.download('stopwords')
#-------------------------------------------Sets Default Endcoding----------------------------------------------------------------
import sys
reload(sys)
sys.setdefaultencoding('UTF8')
#-------------------------------------------Global Variables-----------------------------------------------------------------------
ua = UserAgent()
dt=datetime.datetime.now()
url=""
comment_url=[]
post_geo=()
counter=0
Key=""
word_list = words.words()
stop_words=set(stopwords.words("english"))
url_infile="E:\url_list3.csv"
row=0
location=""
#url="https://www.reddit.com/search?q=pomfret%2C+ct&restrict_sr=&sort=relevance&t=all"
used_urls=[]
#-------------------------------------------Customizing csv writer parameters------------------------------------------------------
csv.register_dialect('pipe_delimited', delimiter='|', skipinitialspace=True)
csv.field_size_limit(2147483647)
#-------------------------------------------Function Definitions-------------------------------------------------------------------
def getURL(file):
	return("")
def getFirst(firstPage):
	return("")

def getPosts(pageUrl):
	return ("")

def tagText(comments):
	return ("")
#--------------------------------------------Begin Crawl----------------------------------------------------------------------------
#print header information
print "Crawl Date: ", dt.strftime('%B %d %Y %H:%M:%S'),"\n"

# Calls getFirst using the hardcoded url in the global variable definition as the start page
def Main():
			url=getURL(url_infile)
			getFirst(url)
			#getPosts(url)
Main()

#...........................................Scraping first page and assigning next page link to url..................................

def getURL():
	global row
	urls=pandas.read_csv(url_infile)
	print urls
	used_urls=[]
	url=urls.iloc[row,0]
	url=str(url).replace('[','').replace(']','').replace(r"'","")
	print "we are inside the getURL function and the url being returned is;", url
	used_urls.append(url)
	#urls.drop(urls.index[0])
	urls.reindex()
	row+=1
	return (url)
getURL()
	
		


def getFirst(firstPage):
	global location
	global url
	url=getURL()
	global post_geo
	global counter
	global Key
	#adding current url for job-flow tracking
	print "Page url:",  url, '\n\n'
	time.sleep(5)
	ua=UserAgent()
	headers={'user-agent': ua.random}
	
	try:
		response=requests.get(url, headers=headers, stream=True, timeout=30, verify=False)
		html=response.text
		soup=BeautifulSoup(html,'lxml')
	except ConnectionError:
		time.sleep(30)
		url=getURL()
		getFirst(url)
	
	#finds relevant content class within the html and creates beautiful soup object	
	try:
		content=soup.findAll(class_='listing search-result-listing')[1]
		
	except IndexError as a:
		print a
		try:
			content=soup.find(class_='listing search-result-listing')
		except AttributeError as b:
			url=getURL()
			getFirst(url)
#will throw attribute error if there are no results for the page
	except Attributerror as a:
		url=getURL()
		getFirst(url)
		
	#finds the second next_page link on the page and re-assigns it to the global variable url; if there is only one next page, assigns to url 
	try:
		next_page=soup.findAll(class_="nav-buttons")[1].findAll('a')[0].attrs['href']
		url=next_page
	
		#content=soup.findAll(class_='listing search-result-listing')[1]
		
	except IndexError:
		try:
			next_page=soup.findAll(class_="nav-buttons")[0].findAll('a')[0].attrs['href']
			url=next_page
			
		except IndexError as a:
			print a
			url=getURL()
		except ConnectionError:
			time.sleep(30)
			url=getURL()
			getFirst(url)		
	
	for results in content.findAll(class_='contents'):
				for post_elements in results:
						comment_url=[]
						comment_url.append(post_elements.find(class_="search-result-meta").find('a').attrs['href'])
						
#capture post metadata and assign to variable post_meta-------------------------------------------------------------------------
						post_meta=post_elements.find(class_='search-result-meta').get_text()
#capture post title and assign to variable title
						title=post_elements.find(class_='search-result-header').find('a').get_text()
#capture post date and assign to variable post_date-----------------------------------------------------------------------------
						post_date_string=post_elements.find(class_='search-time')
						post_date=post_date_string.find('time').attrs['datetime']
#capture only unique url's by converting the comments list to a set, and then back to a list------------------------------------
						comment_url=list(set(comment_url))
						points=post_meta.split("Comments")[-1].split()[0]
						comments_n=post_meta.split("points")[-1].split()[0]
						comments_n=re.sub(",","",comments_n)
						points=re.sub(",","",points)
						try:
							points=int(points)
						except ValueError as a:
							points=points
						try:						
							comments_n=int(comments_n)
						except ValueError as a:
							comments_n=comments_n
						
#iterate through the comment url list and write scraped data to csv------------------------------------------------------------- 
						for link in comment_url:
							try:
									if link is not None:
										with open ('reddit_opioids.csv', 'a') as f:
											counter+=1
											ID=str(counter)
											Key=ID + post_date + link
											fieldnames=['Key','Id','Title','Post','Post_Noun_Phrases','Post Date','Meta','Comments', "Points", "Total Comments", "Post Words",'Post_City','Post_Geo']
											author=[]
											writer=csv.DictWriter(f, delimiter='|', fieldnames=fieldnames, skipinitialspace=True)
#write header--------------------------------------------------------------------------------------------------------------------
											#writer.writeheader()
											headers={'user-agent': ua.random}
											path='/?limit=500'
											link=link+path
											try:
												response=requests.get(link, headers=headers, stream=True, timeout=30, verify=False)
												html=response.text
												soup=BeautifulSoup(html, 'lxml')
												original_post=soup.find(class_='sitetable linklisting').get_text()
												post_words=original_post
#tokenize and clean text-----------------------------------------------------------------------------------------------------------										
												post_blob=TextBlob(original_post)
												post_noun_phrases=post_blob.noun_phrases
												post_noun_phrases=[x.encode("utf-8") for x in post_noun_phrases]
												original_post=sent_tokenize(original_post)
												original_post=[x.encode("utf-8") for x in original_post]
												#post_words=word_tokenize(post_words)
												post_words=post_blob.words
											

											#post_words=list(str(post_words[0]))
#remove stop-words from 'post words'-----------------------------------------------------------------------------------------------													
												post_words=[word for word in post_words if word not in stopwords.words('english')]		
												post_words=[x.encode("utf-8") for x in post_words]
												post_words=" ".join([x for x in post_words if not x.isdigit()])
												"|"
												comments=soup.find(class_='commentarea').get_text()
												html=soup.find(class_='commentarea')
#find comment authors with comments and delimit so individual comments can be parsed in BDD---------------------------------------
											#try:
											#	for ind_comment in html:
											#		author=[]
											#		author.append(html.find(class_="tagline").findAll('a')[1].get_text())
#concatenate list of authors into a single string delimited by a comma
													
											
											#except AttributeError as e:
											#	print e
											#authors= '; '.join(author)+';'
											#print authors
#tag locations--------------------------------------------------------------------------------------------------------------------
												post_location=GeoText(str(post_blob))
												post_location=post_location.cities
											except ConnectionError:
												time.sleep(30)
												url=getURL()
												getFirst(url)
											try:
												for location in post_location:
													post_geo=("","")
													g=geocoder.google(location)
													post_geo=g.latlng
													'|'
											except AttributeError as e:
												print e
#write to csv----------------------------------------------------------------------------------------------------------------------											
											writer.writerow({'Id':ID,'Title':title,'Post': original_post,'Post Words':post_words,'Post_Noun_Phrases':post_noun_phrases,'Post Date': post_date,'Meta':post_meta,'Comments':comments,"Total Comments":comments_n,"Points":points,'Post_City':location,'Post_Geo':post_geo})
											break
#!insert code to find the load more link, and if there is a load more link, open the url, otherwise continue
#Exception Handling									
							except AttributeError as a:
									print a
									continue
									return comments
				return url

	
getFirst("")

#..........................................getPosts function scrapes post/comments for pages 2-n........................................................
	
def getPosts(pageUrl):
	print "------------------------------------------we are now inside the getPosts funtion-------------------------------------------------------------"
	global location
	global url
	global post_geo
	global counter
	global Key
	time.sleep(3)
	ua=UserAgent()
	headers={'user-agent': ua.random}
	
	try:
		response=requests.get(url, headers=headers,stream=True, timeout=30, verify=False)
		html=response.text
		soup=BeautifulSoup(html,'lxml')
	except ConnectionError:
		time.sleep(10)
		url=getURL()
		getFirst(url)
	
	
#adding header for job-flow tracking
	print "Page url:",  url, '\n\n'
	
	
#finds all comments links in the posts	
	try:
		content=soup.find(class_='listing search-result-listing')	
	except IndexError as a:
		content=soup.findAll(class_='listing search-result-listing')[1]
	try:
		next_page=next_page=soup.findAll(class_="nav-buttons")[0].findAll('a')[1].attrs['href']
		url=next_page
	except IndexError as a:
		url=getURL()
		getFirst(url)
	
	except ConnectionError:
		time.sleep(10)
		url=getURL()
		getFirst(url)
		
	try:		
		for results in content.findAll(class_='contents'):
				for post_elements in results:
						
						comment_url=[]
						comment_url.append(post_elements.find(class_="search-result-meta").find('a').attrs['href'])
#capture post title and assign to variable title
						title=post_elements.find(class_='search-result-header').find('a').get_text()
#capture post metadata and assign to variable post_meta-------------------------------------------------------------------------
						post_meta=post_elements.find(class_='search-result-meta').get_text()
#capture post date--------------------------------------------------------------------------------------------------------------
						post_date_string=post_elements.find(class_='search-time')
						post_date=post_date_string.find('time').attrs['datetime']
#add only unique urls  to comment_url set
						comment_url=list(set(comment_url))
						points=post_meta.split("Comments=")[-1].split()[0]
						comments_n=post_meta.split("points")[-1].split()[0]
						comments_n=re.sub(",","", comments_n)
						points=re.sub(",","",points)
						
						try:
							points=int(points)
						except ValueError as a:
							points=points
						
						try:
							comments_n=int(comments_n)
						except ValueError as a:
							print a
							comments_n=comments_n
						print points, comments_n						
						for link in comment_url:
							try:
#the 'a' parameter in the with open statement appends the data to the file, which was already created/opened in the getFirst() function
								with open ('reddit_opioids.csv', 'a') as f:
									counter+=1
									ID=str(counter)
									Key=ID + post_date + link
									fieldnames=['Key','ID','Title','Post','Post_Noun_Phrases','Post Date','Meta','Comments',"Total Comments", "Points","Post Words",'Post_City','Post_Geo']
									writer=csv.DictWriter(f, delimiter='|', fieldnames=fieldnames,skipinitialspace=True,)
									time.sleep(5)
									headers={'user-agent': ua.random}
									path='/?limit=500'
									link=link+path
									try:
										response=requests.get(link, headers=headers,stream=True, timeout=30, verify=False)
										html=response.text
										soup=BeautifulSoup(html, 'lxml')
										original_post=soup.find(class_='sitetable linklisting').get_text()
										post_words=original_post
#tokenize and clean text-----------------------------------------------------------------------------------------------------------------------											
										post_blob=TextBlob(original_post)
										original_post=sent_tokenize(original_post)
										original_post=[x.encode("utf-8") for x in original_post]
										post_noun_phrases=post_blob.noun_phrases
										post_noun_phrases=[x.encode("utf-8") for x in post_noun_phrases]
										post_words=word_tokenize(post_words)
										post_words=[word for word in post_words if word not in stopwords.words('english')]
										post_words=[x.encode("utf-8") for x in post_words]
										post_words=" ".join([x for x in post_words if not x.isdigit()])
										"|"
										comments=soup.find(class_='commentarea').get_text()
										'|'
#tag location--------------------------------------------------------------------------------------------------------------------
										post_location=GeoText(str(post_blob))
										post_location=post_location.cities
									except ConnectionError:
										time.sleep(30)
										url=getURL()
										getFirst(url)
									
									try:
										for location in post_location:
											post_geo=("","")
											g=geocoder.google(location)
											post_geo=g.latlng
											'|'
									except AttributeError as e:
										print e							
#write to csv----------------------------------------------------------------------------------------------------------------------									
									writer.writerow({"Key":Key,'ID':ID,'Title':title,'Post': original_post,'Post Words':post_words,'Post_Noun_Phrases':post_noun_phrases,'Post Date':post_date,'Meta':post_meta, 'Comments':comments,'Total Comments':comments_n,"Points":points,'Post_City':location,'Post_Geo':post_geo})
									break
#!insert code to find the load more link, and if there is a load more link, open the url, otherwise continue				
# Exception handling
							except AttributeError as a:
									print a
									continue	
									return comments

	except AttributeError as a:
		print a

	getPosts(url)		
getPosts("")
#iterate through list of urls once crawl of intial hardcoded query is complete- as indicated by index error
try:
	url=getURL()
	getFirst(url)
except IndexError as a:
	row=0
	url=getURL()
	getFirst(url)

#tag text----------------------------------------------------------------------------------------------------------------------------
