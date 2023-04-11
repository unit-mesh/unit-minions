import json
import csv

type_map = {}
# open datasets/sql/types.json


# open datasets/sql/prompts.json
# create id map for prompts in datasets/sql/prompts.json
id_prompt_map = {}
with open('../datasets/sql/prompts.json', 'r') as f:
    data = json.loads(f.read())
    for row in data:
        id_prompt_map[row['id']] = row['prompt']


with open('../datasets/sql/repositories-5k.jsonl', 'r') as f:
    data = [json.loads(row) for row in f.readlines()]

    with open('../datasets/sql/repository-5k-train.jsonl', 'w') as f:
        for row in data:
            print(row)
            id = int(row['id'])
            item = {
                'instruction': 'text to kotlin repository with class',
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
