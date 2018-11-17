# This is a data scraping project as we don't seem to be able to use existing API's (except for the possible alternate approach).

# We want to use author profiles available at scopus, for example for one of our book authors, Alice Boyes -- here is her scopus page:

# https://www.scopus.com/authid/detail.uri?authorId=15841421100

# We want to create an AWS lambda cloud function that accepts an authorID and returns the following information:

# 1. H-Index score
# 2. Documents by author
# 3. Total citations by how_many docs (so both total and by how many)
# 4. Primary Affiliations (array/list)
# 5. Subject Areas (array/list)
# 6. Number of co-authors

# See values underlined in red in attached image...

# DB: Entries for people, along with their scopus ID's are stored in contentful (contentful.com, we will grant you access)

# CODE: 
# This should be an AWS lambda function using the serverless framework.  Create a new folder in https://github.com/project-lifeview/serverless-functions/tree/master/src like /scopus and deploy a function that does the above scraping for a given scopus ID. It should return a json object with the fields and lists above.

# TOOLS:
# There are several available libraries, like this one: https://github.com/21buttons/pychromeless to allow selenium and headless chrome usage on lambda...

# ACCESS: We will grant you access to github, contentful and AWS for this project

# ACCEPTANCE CRITERIA:
# When passed an author ID the fields above are returned by the function as a json object successfully.  You can use the Alice Boyles record for initial development, but then should test on other people records, that have scopus ID's, in contentful.

# NEXT STEPS: once complete the remaining task will be to integrate this into our pipeline and write results back to contentful

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import pandas as pd
import os
import json
from selenium.webdriver.chrome.options import Options  

chrome_options = Options()  
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"),   chrome_options=chrome_options)  
author_id=input("Input the Author ID you want to process: ")
#Give Author ID as 15841421100 for test
url="https://www.scopus.com/authid/detail.uri?authorId="+str(author_id)
driver.implicitly_wait(30)
driver.get(url)
soup_level1=BeautifulSoup(driver.page_source, 'lxml')
data={}
data['H-Index']= re.sub(r'\D', '',driver.find_element_by_id("authorDetailsHindex").text)
data['Documents by author']= driver.find_element_by_class_name("resultsCountDoc").text
data['Total citations by how_many docs']=driver.find_element_by_id("totalCiteCount").text + ' by ' + driver.find_element_by_id('citationCntLnk').text + ' documents.'
data['Primary Affiliations']=driver.find_element_by_id("authDetailsNameSection").text.split('\n')[1]
data['Subject Areas']=driver.find_element_by_id("subjectAreaBadges").text
data['Number of co-authors']=re.sub(r'\D','',driver.find_element_by_id("coAuthLi").text)
json_data=json.dumps(data)
driver.close()
