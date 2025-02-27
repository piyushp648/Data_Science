import json
import csv
import io
## TF-IDF 
INPUT_FILE = 'text_stripped.json'
OUTPUT_FILE = 'exp.csv'

with io.open(INPUT_FILE, encoding="utf8") as f:
    data = json.load(f)


with io.open(OUTPUT_FILE, mode='w',encoding="utf8",newline='') as exp_file:
    exp_writer = csv.writer(exp_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)

    exp_writer.writerow(['Company', 'Experience'])
    for company in data:
        for exp in company['experiences']:
            if not exp['text']: continue
            exp_writer.writerow([company['name'], str(exp['text'])])

