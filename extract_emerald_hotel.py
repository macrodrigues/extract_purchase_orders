"""This uses PyPDF to read the content from a pdf file"""

import PyPDF2

# creating a pdf file object
pdf_object = open('files/EMERALD_HOTEL/01.pdf', 'rb')

# creating a pdf reader object
pdf_reader = PyPDF2.PdfReader(pdf_object, strict=True)

pdf_reader = pdf_reader.pages[0]

text = pdf_reader.extract_text()

pdf_object.close()

""" Extracts information from the HOTEL GROUP PO pdf"""
# converts the string to a list of strings separated by '\n'
list_text = text.split('\n')

# iteration to find the indexes that contain the valuable information
index_iterable_items = []
for i, item in enumerate(list_text):
    if item.split(' ')[-1] == 'Line':
        index_iterable_items.append(i)


# filter items in text
for index, filt_item in enumerate(
        [list_text[i] for i in index_iterable_items]):
    print(filt_item)
    try:
        first_number = int(filt_item[0])
        filt_item = filt_item[1:]
        filt_item_list = filt_item.split(' ')
        filt_item_list.pop(-1)
        filt_item_list.pop(-1)
        total = filt_item_list.pop(-1)
        print(filt_item_list)
    except Exception as error:
        print(error)
        missing_row = list_text[index_iterable_items[index] - 1]
        full_row = missing_row + ' ' + filt_item
        print(full_row)
