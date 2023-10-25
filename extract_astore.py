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

def find_numeric_value(text):
    """Uses a regex expression to find numerical values among strings."""
    pattern = r"[A-Za-z]*([0-9.]+)"
    matches = re.findall(pattern, text)
    return matches

def find_decimal_portion_of_floats(text):
    """Uses a regex expression to find numerical float, with one single
    value on the left."""
    pattern = r"(\d)\.(\d+\.\d+|\d+\.\d+|\d+)"
    matches = re.findall(pattern, text)
    return matches


def find_number_followed_by_uppercase(text):
    """Uses a regex expression to find a number followed by Uppercase
    in this order"""
    pattern = r"(\d)([A-Z])"
    matches = re.findall(pattern, text)
    return matches


def find_date(text):
    """ Extract dates in the following format"""
    pattern = r'\d{2}/\d{2}/\d{2}'
    matches = re.findall(pattern, text)
    return matches


def extract_from_astore_shop(text):
    """ Extracts information from Astore Shop pdf"""
    # converts the string to a list of strings separated by '\n'
    list_text = text.split('\n')

    # append the results here
    data = []

    # iteration to find the indexes that contain the valuable information
    index_iterable_items = []
    for i, item in enumerate(list_text):
        if 'Nome do Produto Preço unitário Quantidade Total Líquido' in item:
            start_index = i + 1
        if "Assinatura:" in item:
            end_index = i

    try:
        new_text = ' '.join(list_text[start_index:end_index])
    except Exception as error:
        if "cannot access local variable" in str(error):
            new_text = ' '.join(list_text[start_index:])
    list_new_text = new_text.split('AC')
    list_new_text = [ele for ele in list_new_text if ele != '']

    for index, filt_item in enumerate(list_new_text):
        filt_item_list = filt_item.split(' ')
        filt_item_list = [ele for ele in filt_item_list if ele != '']
        filt_item_list.pop(-1)  # remove euro
        total_bruto = filt_item_list.pop(-1)  # catch total and remove
        filt_item_list.pop(-1)  # remove euro again
        iva = filt_item_list.pop(-1)  # catch IVA
        filt_item_list.pop(-1)  # remove euro again
        total_liquido = find_numeric_value(filt_item_list[-1])[0]
        filt_item_list.pop(-1)  # remove total liquido
        quantity = filt_item_list.pop(-1)   # catch quantity and remove
        filt_item_list.pop(-1)  # remove "="
        unit = filt_item_list.pop(-1)  # catch unit and remove
        filt_item_list.pop(-1)  # remove quantity again
        filt_item_list.pop(-1)  # remove quantity again
        filt_item_list.pop(-1)  # remove '/'
        filt_item_list.pop(-1)  # remove euro again
        price = filt_item_list.pop(-1)  # catch price and remove
        filt_item_list.pop(-1)  # remove unit again
        filt_item_list.pop(-1)  # remove '/' again
        filt_item_list.pop(-1)  # remove euro again
        filt_item_list.pop(-1)  # remove price again
        filt_item_list.pop(-1)  # remove euro again
        price_unneeded = find_decimal_portion_of_floats(filt_item_list[-1])[0]
        price_unneeded = '.'.join(list(price_unneeded))
        filt_item_list[-1] = filt_item_list[-1].replace(price_unneeded, '')
        reference = filt_item_list.pop(0)
        temp = find_number_followed_by_uppercase(filt_item_list[0])
        if temp:
            temp = find_number_followed_by_uppercase(filt_item_list[0])[0][0]
            code = filt_item_list[0].split(temp)[0] + temp
            filt_item_list[0] = filt_item_list[0].replace(code, '')
        else:
            code = filt_item_list.pop(0)
        product = " ".join(filt_item_list)

        data.append({
                'código': code,
                'produto': product,
                'quantidade': float(quantity),
                'unidade': unit,
                'preço': float(price),
                'total': float(price)*float(quantity)})

    # find date
    if data:
        dates = []
        for element in list_text:
            date = find_date(element)
            dates.append(date)
        dates = [ele for ele in dates if ele != []]
        dates = [item for row in dates for item in row]
        date = dates[0]
    else:
        date = None

    return {
        'cliente': 'Astore Shop',
        'data': date,
        'dados': data}
