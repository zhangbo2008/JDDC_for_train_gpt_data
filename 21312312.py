import json
from datasets import load_dataset
a=load_dataset('json','demo.json')
with open('demo.json') as f:

    a=json.load(f)
print(1)