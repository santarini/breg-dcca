#!Python 3

import os
import requests
import bs4 as bs
import csv
import re

#create a CSV
with open('bregDatabase.csv', 'a', encoding="utf-8") as csvfileA:
    fieldnames = ['Company Name','Record Type','File Number', 'Status']
    writer = csv.DictWriter(csvfileA, fieldnames=fieldnames, lineterminator = '\n')
    writer.writeheader()

    #generate a search term
    n=1
    for i in range (65,90):
        for j in range (65,90):
            for k in range (65,90):
                searchTerm = chr(i) + chr(j) + chr(k)
                print("Starting: #"+ str(n) +" -> " + searchTerm)

                #make a request using search term
                
                response = requests.get('https://hbe.ehawaii.gov/documents/search.html?beginsWith=true&query='+ searchTerm +'&page=0')
                soup = bs.BeautifulSoup(response.text, 'lxml')

                #check if search term has values
                try:
                    noneText = re.search('There are no businesses for this search term.', soup.text)
                    if noneText.group(0) is not None:
                        print(searchTerm + ": returned no results")
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
                print(searchTerm + ": returned " + resultNumber + " results")
                

                #get what we came here for
                listingTable = soup.find("div", {"id": "table1"})
                mainTable = listingTable.findAll("table")[0]
                for row in mainTable.findAll("tr")[1:]:
                    companyName = row.findAll('td')[0].text
                    recordType = row.findAll('td')[1].text
                    fileNumber = row.findAll('td')[2].text
                    status = row.findAll('td')[3].text


                    #parse to csv
                    writer.writerow({'Company Name': companyName.strip(),'Record Type': recordType.strip(),'File Number': fileNumber.strip(), 'Status': status.strip()})
