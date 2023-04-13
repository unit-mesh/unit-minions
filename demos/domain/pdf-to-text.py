import glob
import json
import re

import PyPDF2

title_pattern = r'^[一二三四五六七八九十零〇百千万亿]+、(.*?)$'
subtitle_pattern = r'^（[一二三四五六七八九十零〇百千万亿]+）(.*?)$'


def is_valid_subtitle(title: str) -> bool:
    # Check if the title matches the pattern
    if re.match(subtitle_pattern, title):
        return True
    else:
        return False


def get_valid_subtitle(title: str) -> str:
    if re.match(subtitle_pattern, title):
        return title.strip().split('）')[1].strip()
    else:
        return ""


# a valid title should start with a chinese_numbers then a 、, like `十一、基金的财产`
def is_valid_title(title: str) -> bool:
    # Check if the title matches the pattern
    if re.match(title_pattern, title):
        return True
    else:
        return False


def get_valid_title(title: str) -> str:
    if re.match(title_pattern, title):
        return title.strip().split('、')[1].strip()
    else:
        return ""


def read_pdf_file(file: str, fund_name: str) -> list[str]:
    text_list = []
    with open(file, "rb") as fp:
        # Create a PDF object
        pdf = PyPDF2.PdfReader(fp)

        # Get the number of pages in the PDF document
        num_pages = len(pdf.pages)

        # Iterate over every page
        for page in range(num_pages):
            # Extract the text from the page
            page_text = pdf.pages[page].extract_text()

            # use regex remove footnotes, which are in the form of `招商基金管理有限公司
            # 招募说明书  \n29`
            page_text = re.sub(r'招商基金管理有限公司\s+招募说明书\s+\d+', '', page_text)

            # remove continues empty lines which are in the form of `\n\n\n\n`
            page_text = re.sub(r'\n\n', '', page_text)

            text_list.append(page_text)

    return text_list


question_answers = []


# use regex to match
# input: 2017-10-10-005230.OF---长盛货币B-长盛货币市场基金托管协议.pdf, output: 长盛货币B
# input: 2022-09-09-007725.OF---招商瑞文A-招商瑞文混合型证券投资基金招募说明书更新.pdf, output: 招商瑞文A
def extract_fund_name(file_name: str) -> str:
    pattern = r'.OF---([\w-]+)-'
    match = re.search(pattern, file_name)
    if match:
        # 返回匹配的基金名称
        return match.group(1)
    else:
        # 如果找不到匹配的基金名称，则返回空字符串
        return ""


def process_pdf_to_question(file: str):
    fund_name = extract_fund_name(file)
    product_name = "招赢通:" + fund_name

    text_list = read_pdf_file(file, product_name)
    # merge all the text into one string
    page_text = ''.join(text_list)
    # write page_text to a file
    with open("domain-pdf.txt", "w") as fp:
        fp.write(page_text)

    lines = page_text.split('\n')
    start_question = False
    answer = ""
    last_question = ""

    for line in lines:
        if is_valid_title(line.strip()):
            start_question = False
            continue

        if is_valid_subtitle(line.strip()):
            if len(answer) > 0:
                create_questions(answer, product_name, last_question)
                answer = ""

            last_question = get_valid_subtitle(line)
            start_question = True

        if start_question:
            answer += line

    create_questions(answer, product_name, last_question)


def create_questions(answer, product_name, last_question):
    question_answers.append({
        "instruction": '介绍一下 [' + product_name + '] 的' + last_question + '?',
        "input": "",
        "output": answer
    })
    question_answers.append({
        "instruction": '什么是 [' + product_name + ']' + last_question + '?',
        "input": "",
        "output": answer
    })


if __name__ == '__main__':
    # fetch all files in the directory testsets/*.pdf
    for file in glob.glob("testsets/*.pdf"):
        process_pdf_to_question(file)

    print("question size: ", len(question_answers))
    # write question_answers to jsonl file
    with open("domain-pdf.jsonl", "w") as fp:
        for qa in question_answers:
            fp.write(json.dumps(qa))
            fp.write('\n')
