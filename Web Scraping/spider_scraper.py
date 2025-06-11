""" 
scraper.py - **Main Source**

This version is best suited for testing Spiderfoot,
as it does not write to a csv on every run.

Web Scraper for CyberSafe Internship
This web scraper will be used to pull information from local businesses in the Charlotte area.
This is part of the CyberSafe internship program through the Carolina Cyber Network.
Author: Blake Poindexter
Date: 5/30/2025

"""

from bs4 import BeautifulSoup
import requests
import subprocess


#Define functions

def run_spiderfoot_scan(target):
  """Runs a SpiderFoot scan for the given target."""
  command = f"python3 ./sf.py -m sfp_spider,sfp_email,sfp_skymem -s {target} -t EMAILADDR,EMAILADDR_GENERIC" 
  process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  stdout, stderr = process.communicate()
  print("SpiderFoot Output:\n", stdout.decode())
  if stderr:
    print("SpiderFoot Errors:\n", stderr.decode())

'''
def start_spiderfoot(target_url):
    #Start a Spiderfoot scan for target URLs (email mode only)
    
    scan_name = "Scan_Commerce"
    payload = {
        "scan_target": target_url,
        "modules": "sfp_email",
        "scan_name": scan_name,
        "options": {},
    }

    res = requests.post(f"{SPIDERFOOT_URL}/api/v1/scan", json=payload)
    #res.raise_for_status()  # Ensure the request was successful
    return res.json().get("scan_id")
''' 
'''
def wait_for_scan(scan_id):
    #Wait for the scan to complete
    while True:
        res = requests.get(f"{SPIDERFOOT_URL}/api/v1/scan/{scan_id}/status")
        res.raise_for_status()
        #scan_data = res.json()
        if res.json().get("status") == "FINISHED":
            break
        time.sleep(5) 
'''
'''
def get_emails(scan_id):
    #Retreive all discovered emails from the scan
    res = requests.get(f"{SPIDERFOOT_URL}/api/v1/scan/{scan_id}/data")
    res.raise_for_status()
    results = res.json()
    emails = [item["data"] for item in results if item["type"] == "EMAILADDR"]
    return list(set(emails)) # remove duplicates
'''

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
        #Success! Now to get web links

        # Begin try block to pull web links, if listed
        web_link = company.find(["div"], class_="mn-text")
        try:
            web_link = web_link.find(["a"]) if web_link else "No website found"
            #web_link = web_link.text
            print(web_link.text)
        except AttributeError:
            web_link = "No website found"
            print(web_link)
           
        #Success! 

        # Attempt to run Spiderfoot
        try:
            if web_link != "" and web_link != "No website found":
                if web_link.text.startswith("https://"):
                    web_link = web_link.text.strip("https://")
                    run_spiderfoot_scan(web_link)
        except Exception as e:
            print(f"Error running Spiderfoot scan for {web_link}: {e}")
        #run_spiderfoot_scan(web_link)
        '''
        scan_id = start_spiderfoot(web_link)
        wait_for_scan(scan_id)
        emails = get_emails(scan_id)
        print(f"Emails found for {web_link.text}: {emails}")
        '''
        
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






