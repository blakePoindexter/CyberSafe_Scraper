""" 
scraper.py - Scrapes local business information from the local chamber of commerce directory
and writes it to a CSV file.

Web Scraper for CyberSafe Internship
This is part of the CyberSafe internship program through the Carolina Cyber Network.
Author: Blake Poindexter
Date: 5/30/2025
"""

from bs4 import BeautifulSoup
import requests
import csv

# Naming and instantiating file
with open("charlotte_chamber_scrape.csv", "w",newline="", encoding="utf-8") as csvfile:
    header = ["Company Name", "Phone number", "Website"]
    writer = csv.writer(csvfile)
    writer.writerow(header)

# URL to chamber of commerce directory
url = "https://directory.charlotteareachamber.com/memberdirectory"

response = requests.get(url)

doc = BeautifulSoup(response.text, 'html.parser')

categoryName = doc.find(["div"], class_="mn-cat")
#print(categoryName)

# Finds ALL and puts in a List
categoryNames = doc.find_all("div", class_="mn-cat")

for categoryName in categoryNames:

    #This is grabbing the hyperlinks from the a tags of the page
    link = categoryName.find(["a"])["href"]

    #Accessing the link to the pages for the different categories
    response = requests.get(link)

    doc = BeautifulSoup(response.text, 'html.parser')

    companies = doc.find_all(["div"], class_="mn-row-inner Rank10")

    
    for company in companies:

        info = []

        print('\n')
        name = company.find(["a"], class_="mn-main-heading")
        print(name.text)
        info.append(name.text)
        '''
        with open("charlotte_chamber_scrape.csv", "a",newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(info)
        '''
        # Begin try block to pull phone numbers, if listed
        # Otherwise it will print "No phone number listed"
        try:
            number = company.find(["span"], class_="mn-sub-heading")
        except AttributeError:
            number = "No phone number found"
        print(number.text if number else "No phone number listed")
        #Success! Now to get web links

        # Append phone number to info list
        info.append(number.text if number else "No phone number listed")

        # Begin try block to pull web links, if listed
        web_link = company.find(["div"], class_="mn-text")
        try:
            web_link = web_link.find(["a"]) if web_link else "No website listed"
            web_link = web_link.text
            print(web_link)
        except AttributeError:
            web_link = "No website found"
        #Success! Now to **try and get socials

        # Append web link to info list
        info.append(web_link if web_link else "No website listed")

        with open("charlotte_chamber_scrape.csv", "a",newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(info)
        
        # Begin try block to pull social media links, if listed
        
        # This next part will be to add "https:" to the front
        # of the link if it is not already a full URL
        company_links = company.find(["a"], class_="mn-main-heading")["href"]
        # Check if the link is a full URL or just a path
        if not company_links.startswith("http"):
            company_links = "https:" + company_links
        
        company_response = requests.get(company_links)
        company_doc = BeautifulSoup(company_response.text, 'html.parser')




