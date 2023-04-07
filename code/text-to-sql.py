# open datasets/sql-train.csv and convert to jsonl
# csv examples:
# ```
# question,sql
# Tell me what the notes are for South Australia ,SELECT Notes FROM table WHERE Current slogan = SOUTH AUSTRALIA
# What is the current series where the new series began in June 2011?,SELECT Current series FROM table WHERE Notes = New series began in June 2011
# ```
# output format:
# [{
#   instruction: "text to sql
#   input: csv.question[index]
#   output: csv.sql[index]
# }]

import csv
import json

with open('../datasets/sql/sql-train.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)
    data = [{
        'instruction': 'text to sql',
        'input': row[0],
        'output': row[1]
    } for row in reader]

with open('../datasets/sql/sql-train.jsonl', 'w') as f:
    for row in data:
        f.write(json.dumps(row) + '\n')
