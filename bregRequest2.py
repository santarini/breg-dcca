#!Python 3

import os
import requests
import bs4 as bs
import csv
import re

#create a CSV
with open('bregDatabase.csv', 'a') as csvfileA:
    fieldnames = ['Company Name','Record Type','File Number', 'Status']
    writer = csv.DictWriter(csvfileB, fieldnames=fieldnames, lineterminator = '\n')
    writer.writeheader()

    #generate a search term
    n=1
    for i in range (65,90):
        for j in range (65,90):
            for k in range (65,90):
                searchTerm = str(n) + ': ' + chr(i) + chr(j) + chr(k)
                print("Starting: " + searchTerm)

                #make a request using search term
                
                response = requests.get('https://hbe.ehawaii.gov/documents/search.html?beginsWith=true&query='+ searchTerm +'&page=0')
                soup = bs.BeautifulSoup(response.text, 'lxml')

                #check if search term has values
                try:
                    noneText = re.search('There are no businesses for this search term.', soup.text)
                    if noneText.group(0) is not None:
                        print(searchTerm + ": returned no results)
                        continue
                except:
                    pass

                #check if more than 300 results for search term
                try:
                    maxText = re.search('Displaying only the first', soup.text)
                    if maxText.group(0) is not None:
                        span = soup.find("span", {"class": "red"}).text
                        instanacesOfCharRegex = re.compile(r'\d{3}')
                        instanacesOfChar = instanacesOfCharRegex.findall(span)[1]
                        instanacesOfChar = instanacesOfChar.replace(",", "")
                        print(searchTerm + ": returned " + instanacesOfChar + " reuslts")
                except:
                    pass

                #list number of page results
                resultNumber = soup.find('strong').text
                

                #get what we came here for
                listingTable = soup.find("div", {"id": "table1"})
                for row in listingTable.findAll("tr")[1:]:
                    companyName = row.findAll('td')[0]
                    recordType = row.findAll('td')[1]
                    fileNumber = row.findAll('td')[2]
                    status = row.findAll('td')[3]

                    #parse to csv
                    writer.writerow({'Company Name': companyName,'Record Type': recordType,'File Number': fileNumber, 'Status': status})
