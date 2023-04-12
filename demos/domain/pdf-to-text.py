import re

import PyPDF2

title_pattern = r'^[一二三四五六七八九十零〇百千万亿]+、(.*?)$'
subtitle_pattern = r'^（[一二三四五六七八九十零〇百千万亿]+）(.*?)$'


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


def read_pdf_file(file: str) -> list[str]:
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
            page_text = re.sub(r'\n\s*\n', '', page_text)

            text_list.append(page_text)

    return text_list


if __name__ == '__main__':
    file = "domain-pdf.pdf"
    question_answers = []
    text_list = read_pdf_file(file)

    # merge all the text into one string
    page_text = ''.join(text_list)

    lines = page_text.split('\n')
    for line in lines:
        if is_valid_title(line):
            # print(line)
            question_answers.append({
                'question': get_valid_title(line),
                'answer': ''
            })

    print(question_answers)
