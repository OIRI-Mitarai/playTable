import sys
from pypdf import PdfReader

# pdf extract text
textfile = 'extract_plane.txt'
# search objective words
dictionary = 'dict.txt'

objective = 'extract_plane.txt'
# hit words in pdf->plane text
output = 'hitword.txt'

# get 1st argment
pdf_file = sys.argv[1]

# get pdf file from 1st argment
reader = PdfReader(pdf_file)

# display page number
pages = len(reader.pages)
print(f"ページ数: {pages}")



# extact text output with initialize text file(extract_plane.txt)
with open(textfile, mode='w', encoding='utf-8') as f:
    for i in range(pages):
        page = reader.pages[i]
        text = page.extract_text()
        f.write(text)


# load search words
with open(dictionary, encoding='utf-8') as f:
    dict_lines = f.readlines()

# load pdf->plane-text
with open(objective, encoding='utf-8') as f:
    objective_lines = f.readlines()

extract = []
for line in objective_lines:
    for dict_line in dict_lines:
        dict_line = dict_line.replace('\n','')
        if dict_line in line:
            if line not in extract:
                extract.append(line)
                print(line)

# output
with open(output, mode='w', encoding='utf-8') as f:
    for i in range(len(extract)):
        f.write(extract[i])
