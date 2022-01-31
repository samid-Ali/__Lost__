# -*- coding: utf-8 -*-
"""
Created on Tue Dec 28 17:04:59 2021

@author: Samid

Web scraper to obtain character data from https://lostpedia.fandom.com/wiki

"""
from bs4 import BeautifulSoup
from requests import get
import pandas as pd
import re
import time
import random
import os

os.chdir("G:/Samid work/Lost/")
os.getcwd()

headers = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})


# setting up the lists that will form our dataframe with all the results
Name = []
Age = []
Death = []
Birth = []


start = time.time()

Links = pd.read_csv(r'G:\Samid work\Lost\MainCharacter_Links.csv', header = None )
    
start = time.time()  
sapo= Links[0]          # since Links is s df, use index 0 to turn into a series for later use
for url in range(len(Links)):
    sapo_url =sapo[url]    
    r = get(sapo_url, headers=headers)
    page_html = BeautifulSoup(r.text, 'html.parser')
        
    """
   Lost_containers = page_html.find_all('div', class_="l-searchResult is-list")
    if Lost_containers != []:
        for idx, container in enumerate(Lost_containers ):
   """             
    #Name
    name =re.search('(?<="Title">).*',str(page_html)).group().replace('</h2>','')
    Name.append(name)
    
    
    #Age
    try:
        a= re.search('(Age</h3>)\n.*',str(page_html)).group()
        age= re.search('\d{2}.*',a).group().replace('</div>', '')
        Age.append(age)
    except:
        print('We do not know how old', name, 'is')
        age= "NA"
        Age.append(age)
        
    #Birth
    try:
        b= re.search('(Birth</h3>)\n.*',str(page_html)).group()
        birth =re.search('\d{4}.*',b).group().replace('</div>', '')
        Birth.append(birth)
    except:
        birth = 'NA'
        Birth.append(birth)
           

    #Death              Not all characters dead so need to test for this 
    try:
        d= re.search('(Death</h3>)\n.*',str(page_html)).group()
        death =re.search('\d{4}.*',d).group().replace('</div>', '')
        Death.append(death)
    except:
        print(name, "is not dead")
        death = "Still Alive"
        Death.append(death)
       
    
 
"""
          #Death Reason
          D0= re.search('(Death Reason</h3>)\n.*',str(page_html)).group()
          Death =re.search('\d{4}.*',d).group().replace('</div>', '')
          Death.append(Death)
 
          
    
"""
time.sleep(random.randint(1,3))
       
Lost_df = pd.DataFrame(
{'Name': Name,
 'Age': Age,
 'Death': Death,
 'Birth': Birth,
 })

Name = [],
Age = [],
Death = [],
Birth = []

end = time.time() - start

file = "Lost_characters_" + str(round(end)) +".tsv"

Lost_df.to_csv(file, sep="\t", index= False)  
print(end)          
