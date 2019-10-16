import requests
from bs4 import BeautifulSoup
import json
# import logging
# import time
# import sys
# import progressbar

url = "https://xlinux.nist.gov/dads/"
OUTPUT_FILE = "output/dsa.json"

data = requests.get(url)

soup = BeautifulSoup(data.text, 'html.parser')

table = soup.find_all('dl')

dict = []
for entry in table:
    for row in entry.find_all('dt'):
        dict.append((row.find('a').text))

with open(OUTPUT_FILE, "w") as writeJSON:
    json.dump(dict, writeJSON, ensure_ascii=False, indent=4)