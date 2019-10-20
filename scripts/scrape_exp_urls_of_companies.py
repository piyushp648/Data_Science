# get all pages for a company

import requests
from bs4 import BeautifulSoup
import json
import logging
import time
import sys
from tqdm import tqdm


TIMESTR = time.strftime("%d%m%Y_%H%M%S")
INPUT_FILE = 'output/company_urls.json'
OUTPUT_FILE = 'output/companies_with_exp_links.json'
LOG_FILE = 'logs/' + 'log_url_' + TIMESTR + '.log'

# ----------------------------------------------------- #
#               Setting up logger and progres bar       #
# ----------------------------------------------------- #

logging.basicConfig(filename=LOG_FILE,
                    format='%(levelname)s %(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# ----------------------------------------------------- #

with open(INPUT_FILE) as file_companies:
    data = json.load(file_companies)


nextPage = True
pgno = 0
new_data = []
urls_accessed = 0
total_pgs = 0
# for every company in companies.json

for entry in tqdm(data):
    tqdm.write(entry['name'], end='\n')
    entry['experiences'] = []
    pgno = 0
    nextPage = True
    # find links of all the experiences and append to entry

    while nextPage is True:
        pgno = pgno + 1
        pg_url = entry['url']+'page/'+str(pgno)
        try:
            data = requests.get(pg_url)
        except requests.exceptions.HTTPError:
            sys.exit(1)
        except requests.exceptions.RequestException:
            sys.exit(1)
        soup = BeautifulSoup(data.text, 'html.parser')

        for titles in soup.find_all('h2'):
            for links in titles.find_all('a', href=True):
                entry['experiences'].append(links['href'])

        nextPage = False if soup.find(
            'a', {'class': 'nextpostslink'}) is None else True

    new_data.append(entry)
    urls_accessed += len(entry['experiences'])
    total_pgs += pgno


# dump to new json file
with open(OUTPUT_FILE, "w") as writeJSON:
    json.dump(new_data, writeJSON, ensure_ascii=False, indent=4)

logger.info('Finished! Got %s URLs from %s pages.', str(urls_accessed), str(total_pgs))  # noqa:E501
logger.info('Data written to file %s! \n', OUTPUT_FILE)

sys.stdout.write('\nFinished! Got {0} URLs from {1} pages.\n'.format(str(urls_accessed), str(total_pgs)))  # noqa:E501
sys.stdout.write('Data written to file {0}! \n\n'.format(OUTPUT_FILE))
