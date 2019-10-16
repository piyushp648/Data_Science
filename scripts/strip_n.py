import json
from tqdm import tqdm
## TF-IDF 
INPUT_FILE = 'output/companies_with_exp_text.json'
OUTPUT_FILE = 'output/text_stripped.json'

with open(INPUT_FILE) as f:
    data = json.load(f)

for company in tqdm(data, desc='Total'):
    for exp in tqdm(company['experiences'], desc=company['name']):
        exp['text'] = exp['text'].replace("\n", " ")

print("\n\n")
with open(OUTPUT_FILE, "w") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)
