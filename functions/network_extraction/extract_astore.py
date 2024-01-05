""" Group of functions to perform data processing on the pdfs of the
Astore Shop
"""
# importing required modules
# pylint: disable=E1101
# pylint: disable=E1101
# pylint: disable=W0718
# pylint: disable=W0612
# flake8: noqa
import re
import pdfplumber as pdfp
from rich import print


def find_seven_consecutive_numbers(text):
    """This function finds 7 consecutive numbers, which will
    correspond to code of the product"""
    # This regex pattern matches exactly 6 consecutive digits
    pattern = r'(AC\d{7})'
    matches = re.findall(pattern, text)
    return matches


def find_date(text):
    """ Extract dates in the following format"""
    pattern = r'\d{2}/\d{2}/\d{2}'
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


def is_float(text):
    """ detect float"""
    pattern = re.compile(r'^\d+\.\d+$')
    matches = re.findall(pattern, text)
    return matches


def extract_from_astore_shop(path):
    """ Extracts information from Astore Shop pdf"""
    pdf = pdfp.open(path)
    first_page = pdf.pages[0]
    first_page_text = first_page.extract_text().split('\n')
    data = []
    dates = []
    for element in first_page_text:
        date = find_date(element)
        if date:
            dates.append(date[0])
        if 'Número da encomenda:' in element:
            order = element.split(' ')[3].strip()

    date = dates[0]
    date = dates[0].split('/')
    date[-1] = '20' + date[-1] # add the 20 to make 2023 and so on
    date = '/'.join(date)

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

    for key, value in filtered_items.items():
        filt_list = value.split(' ')
        for i, item in enumerate(filt_list):
            if ' €\n' in item:
                filt_list[i] = item.split(' ')[0]
                filt_list.insert(i+1, item.split(' ')[-1])
            elif '€' in item:
                filt_list[i] = item.replace('€', '')
            elif '=' in item:
                filt_list[i] = item.replace('=', '')

        filt_list = [item for item in filt_list if item != '']
        filt_list = filt_list[1:-4]
        isfloat = is_float(filt_list[0])
        if filt_list[-1] == '/':
            if isfloat:
                filt_list.insert(0, 'Não Identificado (ver código)')
            code = filt_list.pop(0)
            filt_list.pop(-1)
            price = float(filt_list.pop(-1))
            product = ' '.join(filt_list)
            quantity = 1.0
            data.append(
                {
                'código': code,
                'produto': product,
                'quantidade': quantity,
                'unidade': 'kg',
                'preço': price,
                'total': price*quantity})
        else:
            if isfloat:
                filt_list.insert(0, 'Não Identificado (ver código)')
            if ('Quilos' in filt_list) or ('Garrafas' in filt_list):
                filt_list = filt_list[:-1]
            code = filt_list.pop(0)
            filt_list = [item for item in filt_list if item != '/']
            quantity = float(filt_list.pop(-1))
            if (filt_list[-1] == 'Quilo') or (filt_list[-1] == 'Litro'):
                filt_list.pop(-1)
            price = float(filt_list.pop(-1))
            product = ' '.join(filt_list)
            data.append(
                    {
                        'código': code,
                        'produto': product,
                        'quantidade': quantity,
                        'unidade': 'kg',
                        'preço': price,
                        'total': price*quantity})


    return {
        'order': order,
        'date': date,
        'data': data}
