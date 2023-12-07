""" script to extract data from aziparque and other pdfs with the same model"""
# importing required modules
# pylint: disable=E1101
# pylint: disable=E1101
# pylint: disable=W0718
# pylint: disable=W0612
# flake8: noqa
import re
import pdfplumber as pdfp


def find_eleven_consecutive_numbers(text):
    """This function finds 11 consecutive numbers, which will
    correspond to code of the product"""
    # This regex pattern matches exactly 6 consecutive digits
    pattern = r'\b\d{11}\b'
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


def extract_from_aziparque_n_more(path) -> dict:
    """ Extracts information from Aziparque and morepdf"""
    pdf = pdfp.open(path)
    first_page = pdf.pages[0]
    first_page_text = first_page.extract_text().split('\n')
    for item in first_page_text:
        if "Ordem de Compra Nº" in item:
            order = item.split('Nº')[-1].strip()
        if "Data do Documento:" in item:
            date = item.split(' ')[3].strip()
            date = date.replace('.', '/')

    all_text = []
    for page in pdf.pages:
        text = page.extract_text()
        all_text.append(text)

    all_text = '\n'.join(all_text)
    all_text_list = all_text.split('\n')

    index_iterable_items = []
    for i, item in enumerate(all_text_list):
        digits_index = find_eleven_consecutive_numbers(item)
        if digits_index:
            index_iterable_items.append(i)

    # append to data list
    data = []

    # filter items in text list
    filtered_items = filter_items(index_iterable_items, all_text_list)

    for key, value in filtered_items.items():
        value = value.replace('Fruta Fresca', '')
        value = value.replace('Leg & Veg Frescos', '')
        value = value.replace('Leg 4ª Gama', '')
        filt_list = value.split(' ')
        filt_list = filt_list[1:]
        unit = filt_list.pop(-1)
        if unit == 'KG':
            unit = 'Kg'
        if unit == 'UN':
            unit = 'Un'
        quantity = filt_list.pop(-1)
        product = ' '.join(filt_list)

        data.append({
            'código': None,
            'produto': product.strip(),
            'quantidade': quantity,
            'unidade': unit,
            'preço': 0.0,
            'total': 0.0,
        })

    return {
        'order': order,
        'date': date,
        'data': data}
