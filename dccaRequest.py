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
span = soup.find("span", {"class": "red"}).text
itemPerPage = re.search(r'\d{3}', span)
instanacesOfChar = re.search(r'\d{1,3}\,\d{3}', span)
instanacesOfChar = instanacesOfChar.replace(",", "")
pageCount = int(instanacesOfChar)/int(itemPerPage)
