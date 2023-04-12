import json

output_files = "aggregate.jsonl"

# 1. open usestory/userstory_detail_double_clean_cn.jsonl and change item['instruction'] 创建敏捷用户故事
with open('userstory/userstory_detail_double_clean_cn.jsonl', 'r') as f:
    rows = [json.loads(line) for line in f]
    for id, row in enumerate(rows):
        row['instruction'] = '创建敏捷用户故事'

        if id == 0:
            print(row)

        with open(output_files, 'a') as f:
            json.dump(row, f)
            f.write('\n')

# 2. open test-code/test_to_code_output.jsonl and change item['instruction'] 根据下面的类信息，创建测试用例 and item['input'] to item['classInfo']
with open('test-code/test_to_code_output.jsonl', 'r') as f:
    rows = [json.loads(line) for line in f]
    for id, row in enumerate(rows):
        row['instruction'] = '根据下面的类信息，创建对应测试方法的测试用例'
        row['input'] = row['classInfo'] + row['code']
        row['output'] = row['testMethod']

        del row['classInfo']
        del row['code']
        del row['testMethod']

        # print first row
        if id == 0:
            print(row)

        with open(output_files, 'a') as f:
            json.dump(row, f)
            f.write('\n')

# 3. open swagger/swagger_to_userstory_output.jsonl and change item['instruction'] 根据下面的swagger信息，创建用户故事
with open('swagger/swagger_to_userstory_output.jsonl', 'r') as f:
    rows = [json.loads(line) for line in f]
    for id, row in enumerate(rows):
        row['instruction'] = '根据下面的swagger信息，创建用户故事'

        # print first row
        if id == 0:
            print(row)

        with open(output_files, 'a') as f:
            json.dump(row, f)
            f.write('\n')

# 4. open codegen/codegen.jsonl and replace item['instruction'] "Implement the method" to "根据下面的类信息，实现"
with open('codegen/codegen.jsonl', 'r') as f:
    rows = [json.loads(line) for line in f]
    for id, row in enumerate(rows):
        row['instruction'] = '根据下面的类信息，实现'

        # print first row
        if id == 0:
            print(row)

        with open(output_files, 'a') as f:
            json.dump(row, f)
            f.write('\n')

# 5. 生成 Kotlin 的 Repostiory 类方法
type_map = {}
id_prompt_map = {}
with open('sql/llm-prompts.json', 'r') as f:
    data = json.loads(f.read())
    for row in data:
        id_prompt_map[row['id']] = row['requiredType']

with open('sql/repositories-5k.jsonl', 'r') as f:
    data = [json.loads(row) for row in f.readlines()]

    with open('sql/repository-5k-train.jsonl', 'w') as f:
        for idx, row in enumerate(data):
            requiredType = ""
            id = int(row['id'])
            if id in id_prompt_map:
                # id_prompt_map[id] is a list, check if it is empty
                if id_prompt_map[id]:
                    requiredType = "###" + " ".join(id_prompt_map[id]) + "###"

            item = {
                'instruction': '根据下面的文本，生成 Kotlin 的 Repostiory 类方法',
                'input': row['output'] + "\n" + requiredType,
                'output': row['input']
            }

            # print first row
            if idx == 0:
                print(item)

            f.write(json.dumps(item) + '\n')
