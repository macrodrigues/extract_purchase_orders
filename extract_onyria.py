
# pylint: disable=E1101
# pylint: disable=W0718
# pylint: disable=W0612
# flake8: noqa
import re


def find_seven_consecutive_numbers(text):
    """This function finds 7 consecutive numbers, which will
    correspond to code of the product"""
    # This regex pattern matches exactly 6 consecutive digits
    pattern = r'\b\d{7}\b'
    matches = re.findall(pattern, text)
    return matches

def find_date(text):
    """ Detect date using a regex function"""
    pattern = r'\d{2}/\d{2}/\d{4}'
    matches = re.findall(pattern, text)
    return matches


def find_unit(text):
    """This function finds the unit"""
    pattern = r"[A-Za-z]+"
    matches = re.findall(pattern, text)
    return matches


def extract_from_onyria(text):
    """ Extracts information from the ONYRIA pdf"""
    # converts the string to a list of strings separated by '\n'
    list_text = text.split('\n')

    # iteration to find the indexes that contain the valuable information
    index_iterable_items = []
    for i, item in enumerate(list_text):
        digits_index = find_seven_consecutive_numbers(item)
        if digits_index:
            index_iterable_items.append(i)

    # append the results here
    data = []

    # filter items in text
    for index, filt_item in enumerate(
            [list_text[i] for i in index_iterable_items]):
        filt_item_list = filt_item.split(' ')
        code = filt_item_list.pop(0)
        total = filt_item_list.pop(-1).split('€')[0].strip()
        iva = filt_item_list.pop(-1)
        tax = filt_item_list.pop(-1)
        discount = filt_item_list.pop(-1)
        price = filt_item_list.pop(-1).split('€')[0].strip()
        price = float(price.replace(',', '.'))
        unit = find_unit(filt_item_list[-1])[0]
        quantity = filt_item_list.pop(-1).replace(unit, '')
        quantity = float(quantity.replace(',', '.'))
        filt_item_list.pop(0)
        filt_item_list.pop(-1)
        product = ' '.join(filt_item_list)
        data.append(
            {
                'código': None,
                'produto': product,
                'quantidade': quantity,
                'unidade': unit,
                'preço': price,
                'total': price*quantity})

    # find date
    if data:
        date = find_date(list_text[1])[0]
    else:
        date = None

    return {
        'cliente': 'Onyria',
        'data': date,
        'dados': data}
