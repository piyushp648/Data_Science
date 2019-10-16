# getting list of companies and their URLs

import requests
from bs4 import BeautifulSoup
import json
import logging
import time
import sys
import progressbar

OUTPUT_FILE = "output/company_urls.json"
TIMESTR = time.strftime("%d%m%Y_%H%M%S")
LOG_FILE = 'logs/' + 'log_names_' + TIMESTR + '.log'
URL_INT_CORNER = 'https://www.geeksforgeeks.org/company-interview-corner/'


# ----------------------------------------------------- #
#               Setting up logger and progres bar       #
# ----------------------------------------------------- #
progressbar.streams.wrap_stderr()

logging.basicConfig(filename=LOG_FILE,
                    format='%(levelname)s %(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger()

logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stderr)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # noqa:E501
handler.setFormatter(formatter)
logger.addHandler(handler)
# ----------------------------------------------------- #
# get the data
try:
    data = requests.get(URL_INT_CORNER)
except requests.exceptions.HTTPError as err:
    logger.error('HTTP Error occured accessing the URL {0}.\n Error Message: {1}'.format(URL_INT_CORNER, err))  # noqa:E501
    sys.exit(1)
except requests.exceptions.RequestException as err:
    logger.error('RequestException occured accessing the URL {0}.\n Exception: {1}'.format(URL_INT_CORNER, err))  # noqa:E501
    sys.exit(1)

# load data into bs4
soup = BeautifulSoup(data.text, 'html.parser')

companies = soup.find('ul', {'class': 'sUlClass'})

company_list = []
for links in progressbar.progressbar(companies.find_all('a', href=True)):
    data = {}
    url = str(links['href'])
    name = str(links.text.split('[')[0]).replace(u'\xa0', u'')

    data['url'] = url
    data['name'] = name
    company_list.append(data)

with open(OUTPUT_FILE, "w") as writeJSON:
    json.dump(company_list, writeJSON, ensure_ascii=False, indent=4)

logger.info("Finished! Got %s entries.", str(len(company_list)))
