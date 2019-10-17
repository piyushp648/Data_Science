import requests
from bs4 import BeautifulSoup

url = "https://xlinux.nist.gov/dads/"

data = requests.get(url)

soup = BeautifulSoup(data.text, 'html.parser')

table = soup.find_all('dl')

dict = []


import csv

OUTPUT_FILE = 'dsa.csv'

with open(OUTPUT_FILE, mode='w',encoding="utf8",newline='') as dict_file:
    dict_writer = csv.writer(dict_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)

    dict_writer.writerow(['Keywords'])
    for entry in table:
        for row in entry.find_all('dt'):
            dict_writer.writerow([row.find('a').text])
    

