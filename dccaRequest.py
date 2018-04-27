#!Python 3

import os
import requests
import bs4 as bs
import csv
import re

response = requests.get('https://hbe.ehawaii.gov/documents/search.html?beginsWith=true&query=a&page=0')
soup = bs.BeautifulSoup(response.text, 'lxml')
parentTable = soup.findAll("table")[1]
mainTable = parentTable.findAll("td")[1]

#figure out page count
span = soup.find("span", {"class": "red"}).text
itemPerPageRegex = re.compile(r'\d{3}')
itemPerPage = itemPerPageRegex.findall(span)[0]

instanacesOfCharRegex = re.compile(r'\d{1,3}\,\d{3}')
instanacesOfChar = instanacesOfCharRegex.findall(span)[0]
instanacesOfChar = instanacesOfChar.replace(",", "")

pageCount = int(instanacesOfChar)/int(itemPerPage)

#isolate company listings
listingTable = mainTable.findAll("span", {"id": "table1"})
