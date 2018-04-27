#!Python 3

import os
import requests
import bs4 as bs
import csv
import re

response = requests.get('https://hbe.ehawaii.gov/documents/search.html?recordType=ALL&status=ALL&beginsWith=true&query=the')
soup = bs.BeautifulSoup(response.text, 'lxml')

#check if search term has values
try:
    noneText = re.search('There are no businesses for this search term.', soup.text)
    if noneText.group(0) is not None:
        #label as being none
        continue
except:

#check if more than 300 results for search term
try:
    maxText = re.search('Displaying only the first', soup.text)
    if maxText.group(0) is not None:
        span = soup.find("span", {"class": "red"}).text
        instanacesOfCharRegex = re.compile(r'\d{3}')
        instanacesOfChar = instanacesOfCharRegex.findall(span)[1]
        instanacesOfChar = instanacesOfChar.replace(",", "")
        print(instanacesOfChar)
except:
    #pull data
    

