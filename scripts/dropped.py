import json
import csv
## TF-IDF 
INPUT_FILE = 'text_stripped.json'
OUTPUT_FILE = 'exp.csv'

with open(INPUT_FILE, encoding="utf8") as f:
    data = json.load(f)

# for company in data:
#     for exp in company['experiences']:
#         print(company['name'] + str(exp['votes']))

with open(OUTPUT_FILE, mode='w',encoding="utf8",newline='') as exp_file:
    exp_writer = csv.writer(exp_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    exp_writer.writerow(['Company', 'Experience'])
    for company in data:
        for exp in company['experiences']:
            # print(company['name'] + str(exp['votes']))
            exp_writer.writerow([company['name'], exp['text']])
