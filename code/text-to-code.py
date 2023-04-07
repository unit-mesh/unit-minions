# open datasets/text-to-code/java.jsonl and fetch the first 4000 items
# ```
# output format:
# [{
#   instruction: "text to java code",
#   input: items[index].text,
#   output: items[index].code
# }]

import json

with open('../datasets/text-to-code/java.jsonl', 'r') as f:
    data = [json.loads(row) for row in f.readlines()]

data = data[:4000]

with open('../datasets/text-to-code/java-train.jsonl', 'w') as f:
    for row in data:
        item = {
            'instruction': 'text to java code',
            'input': row['text'],
            'output': row['code']
        }

        f.write(json.dumps(item) + '\n')
