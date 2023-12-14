""" Group of functions to perform data processing on the pdfs of the
Jupyter Hotel
"""
# importing required modules
# pylint: disable=E1101
# pylint: disable=E1101
# pylint: disable=W0718
# pylint: disable=W0612
# flake8: noqa
import re
from rich import print


def find_six_consecutive_numbers(text) -> list:
    """This function finds 6 consecutive numbers, which will
    correspond to code of the product"""
    # This regex pattern matches exactly 6 consecutive digits
    pattern = r'\d{6}'
    matches = re.findall(pattern, text)
    return matches


def detect_zero_followed_by_letter(text):
    """This function finds a letter followed by 0"""
    pattern = r'0[A-Za-z]'
    matches = re.findall(pattern, text)
    return matches


def detect_zero_followed_by_digit(text):
    """This function finds a digit followed by 0"""
    pattern = r'0[0-9]{1,3},'
    matches = re.findall(pattern, text)
    return matches


def find_date(text):
    """ Detect date using a regex function"""
    pattern = r'\d{4}/\d{2}/\d{2}'
    matches = re.findall(pattern, text)
    return matches


def find_missing_numbers(indexes) -> list:
    """When iterating, some products have the continuation of the product's
    name in the next line. I use this function do find the missing number index
    to later use it to grab the extra information of the product"""
    missing_numbers = []
    for i in range(1, len(indexes)):
        if indexes[i] != indexes[i - 1] + 1:
            for missing in range(indexes[i - 1] + 1, indexes[i]):
                missing_numbers.append(missing)
    return missing_numbers


def filter_items(list_of_indexes, text_list):
    """This function takes the list of indexes and parses the the text list,
    by saving the values in a dictionary. In this dictionary there are some
    irrelevant items that need to be removed"""

    # filter list
    filtered_items = {}
    for i in list_of_indexes:
        filtered_items[i] = text_list[i]

    # remove 'WinMax' elements
    filtered_items = {key: value for key, value
                      in filtered_items.items() if 'WinMax' not in value}

    # remove 'NIF'
    filtered_items = {key: value for key, value
                      in filtered_items.items() if 'NIF' not in value}

    # remove 'Total a transportar'
    filtered_items = {key: value.replace('Total a transportar (EUR)','')
                      for key, value in filtered_items.items()}

    # remove the ones starting with '5'
    filtered_items = {key: value for key, value
                      in filtered_items.items() if value[0] != '5'}

    # remove first 6 characters
    filtered_items = {key: value[6:].strip() for key, value
                      in filtered_items.items()}

    return filtered_items


def fix_broken_rows(filtered_items, units):
    """This function looks for broken rows, which are rows that
    don't follow the same order as the majority, and fixes them"""

    broken_row = ''
    for k, v in filtered_items.items():
        for unit_key in units.keys():
            if unit_key in v.split(' ')[0]:
                broken_row = v.replace(unit_key, f" {unit_key} ")

                # this removes the tax letter and adds a space
                tax_letter = detect_zero_followed_by_letter(broken_row)
                broken_row = broken_row.replace(
                    tax_letter[0],
                    f"{tax_letter[0][0]}  {tax_letter[0][1]}")

                # this deals with glued values
                glued = detect_zero_followed_by_digit(broken_row)
                broken_row = broken_row.replace(
                    glued[0], f'{glued[0][0]} {glued[0][1]},')

                print(broken_row)

                # remove discount
                fixed_row = broken_row.replace('0,000,00 ', ' 0,00 0,00')

                # substitution
                filtered_items[k] = fixed_row

    return filtered_items


def extract_from_jupyter_hotel(text) -> dict:
    """ Extracts information from the JUPYTER HOTEL PO pdf"""
    # converts the string to a list of strings separated by '\n'

    list_text = text.split('\n')

    # list of indexes with the right information
    index_iterable_items = []
    for i, item in enumerate(list_text):
        digits_index = find_six_consecutive_numbers(item)
        if digits_index:
            index_iterable_items.append(i)

    # append the results here
    data = []

    # units
    units = {
        'KG': 'Kg',
        'UN': 'Un',
        'L': 'L',
        'GF5':'L',
        'E15':'Kg'}

    # find missing indexes
    missing_indexes = find_missing_numbers(index_iterable_items)

    # filter items in text list
    filtered_items = filter_items(index_iterable_items, list_text)

    # fix broken items
    filtered_items = fix_broken_rows(filtered_items, units)



    # deal with missing values
    important_missing = []
    for i in missing_indexes:
        row = list_text[i]
        if 'EMBALADA' in row:
            important_missing.append(i)

    for key, value in filtered_items.items():
        value = value.split(' ')
        value.pop(0)
        unit = value.pop(0)
        unit = units[unit]
        quantity = value.pop(0)
        quantity = float(quantity.replace(',', '.'))
        price = value.pop(0)
        price = float(price.replace(',', '.'))
        product = ' '.join(value[3:])
        for missing_index in important_missing:
            if missing_index ==  key + 1:
                product = f"{product} {list_text[missing_index]}"

        # some products have '1)' in the name. Remove it.
        if '1)' in product:
            product = product.replace('1)', '')

        data.append({
            'código': None,
            'produto': product.strip(),
            'quantidade': quantity,
            'unidade': unit,
            'preço': price,
            'total': price*quantity
        })

    # find date
    if data:
        dates = []
        for element in list_text:
            date = find_date(element)
            dates.append(date)
        dates = [ele for ele in dates if ele != []]
        dates = [item for row in dates for item in row]
        # change date order
        date = dates[0].split('/')
        date = f'{date[2]}/{date[1]}/{date[0]}'
    else:
        date = None

    # find order
    for element in list_text:
        if 'EF ' in element:
            order = element.split('EF ')[-1].strip()

    return {
        'order': order,
        'date': date,
        'data': data}
