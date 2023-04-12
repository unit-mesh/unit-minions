# open demo.csv and into jsonl
import csv
import json

with open('demo.csv', 'r') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    with open('demo.jsonl', 'w') as f:
        for row in rows:
            json.dump(row, f)
            f.write('\n')
