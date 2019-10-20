# get experience paragraph from all the URLs from companies.json

import requests
from bs4 import BeautifulSoup
import json
import sys
import logging
import time
from tqdm import tqdm
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

TIMESTR = time.strftime("%d%m%Y_%H%M%S")
INPUT_FILE = 'output/companies_with_exp_links.json'
LOG_FILE = 'logs/' + 'log_text_' + TIMESTR + '.log'
OUTPUT_FILE = 'output/companies_with_exp_text.json'
# ----------------------------------------------------- #
# to retry in case the connection is interrupted #


def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def get(url):
    try:
        return requests.get(url)
    except Exception:
        # sleep for a bit in case that helps
        tqdm.write('Trying to reconnect...')
        time.sleep(5)
        # try again
        return get(url)


# ----------------------------------------------------- #


logging.basicConfig(filename=LOG_FILE,
                    format='%(levelname)s %(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger()

logger.setLevel(logging.DEBUG)


# ----------------------------------------------------- #


def fprint(str):
    tqdm.write(str)
    logger.info(str)


# ----------------------------------------------------- #
with open(INPUT_FILE) as f:
    company_data = json.load(f)
    logger.info('Reading file {0}'.format(INPUT_FILE))

# pp.pprint(data)

total_pgs = 0

for company in tqdm(company_data, desc="Total"):
    exp_list = []

    for exp_url in tqdm(company['experiences'], desc=company['name']):
        # new container for company['experiences']
        exp_container = {}
        exp_container['url'] = exp_url

        # get data for the experience
        try:
            logger.info('Getting request for URL: {0}'.format(exp_url))
            exp_html_data = get(exp_url)
        except Exception as x:
            fprint('failed  to get URL {1} :( {0}'.format(
                x.__class__.__name__,
                exp_url
            ))
            sys.exit(1)
        total_pgs += 1

        # load into bs4
        soup = BeautifulSoup(exp_html_data.text, 'html.parser')

        # find entry-content
        content = soup.find('div', {'class': 'entry-content'})

        # print(soup.get_text())
        content_str = ""      # to store strings acquired in following 'p' tags
        for exp in content.find_all('p'):
            content_str += ' ' + exp.get_text().strip()
        try:
            difficulty = soup.find('span', {'id': 'rating_box'})
            votes = soup.find('span', {'id': 'vote_count'})
            votes = None if votes is None else votes.find('b')

            exp_container['difficulty'] = 0.0 if difficulty is None else float(difficulty.get_text())  # noqa:E501
            exp_container['text'] = content_str.strip()
            exp_container['votes'] = 0 if votes is None else int(votes.get_text())  # noqa:E501
        except Exception as err:
            fprint('Exception occured while accessing URL {0} \n {1}'.format(       # noqa:E501
                exp_url,
                err
            ))
            fprint('Moving on...')
            continue

        exp_list.append(exp_container.copy())
    company['experiences'] = exp_list


with open(OUTPUT_FILE, "w") as writeJSON:
    json.dump(company_data, writeJSON, ensure_ascii=False, indent=4)

fprint('\n\nFinished! Got data from {0} pages.\n'.format(
    str(total_pgs)))
fprint('Data written to file {0}! \n\n'.format(OUTPUT_FILE))
