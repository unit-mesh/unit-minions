from tika import parser

parsed = parser.from_file('domain-pdf.pdf')
print(parsed["metadata"])
print(parsed["content"])