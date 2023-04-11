import json
import csv

with open('../datasets/sql/repository-5k.jsonl', 'r') as f:
    data = [json.loads(row) for row in f.readlines()]

    with open('../datasets/sql/repository-5k-train.jsonl', 'w') as f:
        for row in data:
            item = {
                'instruction': 'text to kotlin repository',
                'input': row['output'],
                'output': row['input']
            }

        f.write(json.dumps(item) + '\n')


    # 5kl to csv
    with open('../datasets/sql/repository-5k.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['question', 'code'])
        for row in data:
            writer.writerow([row['output'], row['input']])
