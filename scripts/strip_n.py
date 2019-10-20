import json
from tqdm import tqdm
import io
import re

## TF-IDF 
INPUT_FILE = 'companies_with_exp_text.json'
OUTPUT_FILE = 'text_stripped.json'
def deEmojify(inputString):
    return inputString.encode('ascii', 'ignore').decode('ascii')

with io.open(INPUT_FILE, encoding="utf-8") as f:
    data = json.load(f)

for company in tqdm(data, desc='Total'):
    for exp in tqdm(company['experiences'], desc=company['name']):
        exp['text'] = exp['text'].replace("\n", " ")
        re.sub(r'[^\x00-\x7F]+',' ', exp['text'])
        exp['text'] = deEmojify(exp['text'])

print("\n\n")
with io.open(OUTPUT_FILE, "w", encoding='utf8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)
