import requests
from bs4 import BeautifulSoup
import time

SPIDERFOOT_URL = 'http://127.0.0.1:5001'

def get_company_links(start_url):
    """Scrapes company website links from a given page"""
    res = requests.get(start_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    return [a['href'] for a in soup.find_all('a', href=True) if 'http' in a['href']]

def start_spiderfoot_scan(target_url):
    """Starts a scan on Spiderfoot for the given URL"""
    scan_name = f"Scan_{int(time.time())}"
    payload = {
        "scan_target": target_url,
        "modules": "sfp_email",  # Only email module
        "scan_name": scan_name,
        "options": {"max_pages": "20"},
    }

    res = requests.post(f"{SPIDERFOOT_URL}/api/v1/scan/new", json=payload)
    scan_id = res.json().get("scan_id")
    return scan_id

def wait_for_scan(scan_id):
    """Polls the Spiderfoot scan status"""
    while True:
        res = requests.get(f"{SPIDERFOOT_URL}/api/v1/scan/{scan_id}/status")
        status = res.json().get("status")
        if status == "FINISHED":
            return
        time.sleep(5)

def get_email_results(scan_id):
    """Fetches email results from the completed Spiderfoot scan"""
    res = requests.get(f"{SPIDERFOOT_URL}/api/v1/scan/{scan_id}/data")
    emails = [r['data'] for r in res.json() if r['type'] == 'EMAILADDR']
    return emails

def main():
    company_page = "https://example.com/companies"
    links = get_company_links(company_page)

    for link in links:
        print(f"Scanning {link}")
        try:
            scan_id = start_spiderfoot_scan(link)
            wait_for_scan(scan_id)
            emails = get_email_results(scan_id)
            print(f"Found emails for {link}: {emails}")
        except Exception as e:
            print(f"Error scanning {link}: {e}")

if __name__ == "__main__":
    main()




