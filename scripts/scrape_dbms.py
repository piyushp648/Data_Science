import requests
from bs4 import BeautifulSoup
import json
# import logging
# import time
# import sys
# import progressbar

url = "https://raima.com/database-terminology/"
OUTPUT_FILE = "output/dsa.json"

data = requests.get(url)

soup = BeautifulSoup(data.text, 'html.parser')

data = soup.find_all('strong')

for entry in data:
    print(entry.text)
