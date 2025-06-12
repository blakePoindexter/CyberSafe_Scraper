""" 
spider_scraper.py - A web scraper written in Python that calls Spiderfoot to run scans
for email addresses.
Author: Blake Poindexter
Date: 5/30/2025
"""

from bs4 import BeautifulSoup
import requests
import subprocess
import time

#Define functions

def run_spiderfoot_scan(target):
  """Runs a SpiderFoot scan for the given target."""
  command = f"python3 ./sf.py -m sfp_spider,sfp_email,sfp_skymem -s {target} -t EMAILADDR,EMAILADDR_GENERIC -o csv > scan_results.csv" 
  process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  stdout, stderr = process.communicate()
  time.sleep(5)  # Wait for a few seconds for scan
  print("SpiderFoot Output:\n", stdout.decode())
  if stderr:
    print("SpiderFoot Errors:\n", stderr.decode())

# Ensure Spiderfoot is running with API access
#SPIDERFOOT_URL = 'http://127.0.0.1:5001'

# URL to chamber of commerce directory
url = "https://directory.charlotteareachamber.com/memberdirectory"
response = requests.get(url)

# Initialize BeautifulSoup 
doc = BeautifulSoup(response.text, 'html.parser')
categoryName = doc.find(["div"], class_="mn-cat")

# Finds ALL and puts in a List
categoryNames = doc.find_all("div", class_="mn-cat")

for categoryName in categoryNames:

    #This is grabbing the hyperlinks from the a tags of the page
    link = categoryName.find(["a"])["href"]

    #Accessing the link to the pages for the different categories
    response = requests.get(link)
    doc = BeautifulSoup(response.text, 'html.parser')
    companies = doc.find_all(["div"], class_="mn-row-inner Rank10")

    # Cycle through each company listed
    for company in companies:
        print('\n')
        name = company.find(["a"], class_="mn-main-heading")
        print(name.text)

        # Begin try block to pull phone numbers, if listed
        # Otherwise it will print "No phone number listed"
        try:
            number = company.find(["span"], class_="mn-sub-heading")
        except AttributeError:
            number = "No phone number found"
        print(number.text if number else "No phone number listed")
        # Now to get web links

        # Begin try block to pull web links, if listed
        web_link = company.find(["div"], class_="mn-text")
        try:
            web_link = web_link.find(["a"]) if web_link else "No website found"
            #web_link = web_link.text
            print(web_link.text)
        except AttributeError:
            web_link = "No website found"
            print(web_link)

        # Attempt to run Spiderfoot
        try:
            if web_link != "" and web_link != "No website found":
                if web_link.text.startswith("https://"):
                    web_link = web_link.text.strip("https://") # Remove "https://"
                    if web_link.startswith("www."): # Remove "www."
                        web_link = web_link[4:]
                        if web_link.endswith("/"):
                            web_link  = web_link[:-1]  # Remove trailing slash 
            run_spiderfoot_scan(web_link)
        except Exception as e:
            print(f"Error running Spiderfoot scan for {web_link}: {e}")
        
        # Begin try block to pull social media links, if listed
        # This will be a bit more complex, as the scraper needs to 
        # step through each link to find the social media links
        
        company_links = company.find(["a"], class_="mn-main-heading")["href"]
        # Check if the link is a full URL or just a path
        if not company_links.startswith("http"):
            company_links = "https:" + company_links
        
        company_response = requests.get(company_links)
        company_doc = BeautifulSoup(company_response.text, 'html.parser')
        #company_page = company_doc.find(["div"], class_="mn-row-inner Rank10")
        # Now we have the company page, we can search for social media links
        
        # This will be the try block to pull social media links
        try:
            social_links = company.find_all(["a"], target='"_blank"')
            for social_link in social_links:
                if "facebook.com" in social_link["href"]:
                    print(social_link["href"])
                elif "instagram.com" in social_link["href"]:
                    print(social_link["href"])
                elif "linkedin.com" in social_link["href"]:
                    print(social_link["href"])
                elif "twitter.com" in social_link["href"]:
                    print(social_link["href"])
        except AttributeError:
            print("No social media links found")






