import re
from pathlib import Path
from typing import Dict, List, Optional

import PyPDF2

file = "domain-pdf.pdf"

text_list = []
question_answers = []

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
        print(page_text)

# print(text_list)

