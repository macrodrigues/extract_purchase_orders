""" Group of functions to perform data processing on the pdfs of the
Emerald Hotel
"""
# importing required modules
# pylint: disable=E1101
# pylint: disable=E1101
# pylint: disable=W0718
# pylint: disable=W0612
# flake8: noqa
import re

def find_numeric_value(text):
    """Uses a regex expression to find numerical values among strings."""
    pattern = r"[A-Za-z]*([0-9.]+)"
    matches = re.findall(pattern, text)
    return matches


def extract_from_emerald_hotel(text):
    """ Extracts information from the Emerald Hotel pdf"""
    # converts the string to a list of strings separated by '\n'
    list_text = text.split('\n')

    # iteration to find the indexes that contain the valuable information
    index_iterable_items = []
    for i, item in enumerate(list_text):
        if item.split(' ')[-1] == 'Line':
            index_iterable_items.append(i)

    # append the results here
    data = []

    # filter items in text
    for index, filt_item in enumerate(
            [list_text[i] for i in index_iterable_items]):
        try:
            first_number = int(filt_item[0])
            filt_item = filt_item[1:]
            filt_item_list = filt_item.split(' ')
            filt_item_list.pop(-1)
            numeric_val = find_numeric_value(filt_item_list[-1])
            if numeric_val:
                total = numeric_val[0]
                filt_item_list.pop(-1)
            else:
                filt_item_list.pop(-1)
                total = filt_item_list.pop(-1)
            price = filt_item_list.pop(-1)
            price = float(price[1:])
            unit = filt_item_list.pop(-1)
            quantity = filt_item_list.pop(-1)
            quantity = float(quantity)
            code = filt_item_list.pop(0)
            product = ' '.join(filt_item_list)
        except Exception as error:
            print(error)
            missing_row = list_text[index_iterable_items[index] - 1]
            full_row = missing_row + ' ' + filt_item
            full_row_list = full_row.split(' ')
            full_row_list.pop(-1)
            numeric_val = find_numeric_value(full_row_list[-1])
            if numeric_val:
                total = numeric_val[0]
                full_row_list.pop(-1)
            else:
                full_row_list.pop(-1)
                total = full_row_list.pop(-1)
            price = full_row_list.pop(-1)
            price = float(price[1:])
            unit = full_row_list.pop(-1)
            quantity = full_row_list.pop(-1)
            quantity = float(find_numeric_value(quantity)[0])
            code = full_row_list.pop(0)
            product = ' '.join(full_row_list)

        data.append({
                'código': code,
                'produto': product,
                'quantidade': quantity,
                'unidade': unit,
                'preço': price,
                'total': price*quantity})

    # find date
    if data:
        date = list_text[0].split(',')[0]
    else:
        date = None
    return {
        'client': 'emerald_hotel',
        'date': date,
        'data': data}
