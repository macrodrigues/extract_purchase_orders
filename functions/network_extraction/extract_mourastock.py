""" Group of functions to perform data processing on the pdfs of the
Mourastock
"""
# importing required modules
# pylint: disable=E1101
# pylint: disable=E1101
# pylint: disable=W0718
# pylint: disable=W0612
# flake8: noqa
import re
from rich import print
import pdfplumber as pdfp

def find_seven_consecutive_numbers(text):
    """This function finds 7 consecutive numbers, which will
    correspond to code of the product"""
    # This regex pattern matches exactly 6 consecutive digits
    pattern = r'\b\d{7}\b'
    matches = re.findall(pattern, text)
    return matches


def filter_items(list_of_indexes, text_list):
    """This function takes the list of indexes and parses the the text list,
    by saving the values in a dictionary. In this dictionary there are some
    irrelevant items that need to be removed"""

    # filter list
    filtered_items = {}
    for i in list_of_indexes:
        filtered_items[i] = text_list[i]

    return filtered_items


def find_date(text):
    """ Extract dates in the following format"""
    pattern = r'\d{2}/\d{2}/\d{4}'
    matches = re.findall(pattern, text)
    return matches


def extract_from_mourastock(path):
    """ Extracts information from Mourastock pdf"""
    pdf = pdfp.open(path)
    first_page = pdf.pages[0]
    first_page_text = first_page.extract_text().split('\n')
    dates = []
    for element in first_page_text:
        date = find_date(element)
        if date:
            dates.append(date[0])
        if 'Encomenda de Fornecedor -' in element:
            order = element.split(' ')[-1]

    date = dates[0]

    all_text = []
    for page in pdf.pages:
        text = page.extract_text()
        all_text.append(text)

    all_text = '\n'.join(all_text)
    all_text_list = all_text.split('\n')

    index_iterable_items = []
    for i, item in enumerate(all_text_list):
        digits_index = find_seven_consecutive_numbers(item)
        if digits_index:
            index_iterable_items.append(i)

    # filter items in text list
    filtered_items = filter_items(index_iterable_items, all_text_list)

    # units
    units = {
        'KG': 'Kg',
        'UN': 'Un',
        'L': 'L'}

    data = []

    for key, value in filtered_items.items():
        filt_list = value.split(' ')
        filt_list = filt_list[1:-2]
        price = filt_list.pop(-1)
        price = float(price.replace(',', '.'))
        for k, v in units.items():
            if k in filt_list[-1]:
                unit = v
                quantity = float(
                    filt_list[-1].replace(k, '').replace(',', '.'))

        filt_list.pop(-1)
        product = ' '.join(filt_list)
        # some products have 'kg' in the name. Remove it.
        if 'kg' in product:
            product = product.replace('kg','')
        data.append({
            'código': None,
            'produto': product.strip(),
            'quantidade': quantity,
            'unidade': unit,
            'preço': price,
            'total': price*quantity
        })

    return {
        'order': order,
        'date': date,
        'data': data}
