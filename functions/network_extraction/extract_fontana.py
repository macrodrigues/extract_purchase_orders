# importing required modules
# pylint: disable=E1101
# pylint: disable=E1101
# pylint: disable=W0718
# pylint: disable=W0612
# flake8: noqa
import re
import pdfplumber as pdfp
from rich import print


def convert_to_date(input_list):
    # Mapping month names to their numerical representation
    month_mapping = {
        'January': '01',
        'February': '02',
        'March': '03',
        'April': '04',
        'May': '05',
        'June': '06',
        'July': '07',
        'August': '08',
        'September': '09',
        'October': '10',
        'November': '11',
        'December': '12'
    }

    # Extract day, month, and year from the input list
    day, month, year = input_list

    # Convert month name to numerical representation
    month_number = month_mapping.get(month)

    # Format the date string
    formatted_date = f"{day.rstrip('.')}/{month_number}/{year}"

    return formatted_date


def detect_reference_pattern(input_string):
    pattern = r'\d{2}-\d{4}'
    matches = re.findall(pattern, input_string)
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


def extract_tables_fontana(path) -> dict:
    """ Extracts information from Fontana Hotels pdf"""
    pdf = pdfp.open(path)
    first_page = pdf.pages[0]
    first_page_text = first_page.extract_text().split('\n')
    for element in first_page_text:
        if 'Order No.' in element:
            element = element.split(' ')
            order = element[2]

        if 'Document Date' in element:
            element = element.split(' ')
            date = element[2:5]
            date = convert_to_date(date)

    all_text = []
    for page in pdf.pages:
        text = page.extract_text()
        all_text.append(text)

    all_text = '\n'.join(all_text)
    all_text_list = all_text.split('\n')

    index_iterable_items = []
    for i, item in enumerate(all_text_list):
        digits_index = detect_reference_pattern(item)
        if digits_index:
            index_iterable_items.append(i)

    # find missing indexes
    missing_indexes = find_missing_numbers(index_iterable_items)

    # filter items in text list
    filtered_items = filter_items(index_iterable_items, all_text_list)

    # empty list
    data = []

    for key, value in filtered_items.items():
        if 'UNIT / BOT' in value:
            value = value.replace('UNIT / BOT', 'Un')
        value_list = value.split(' ')
        value_list = value_list[1:-3]
        if value_list[-1] == 'Yes':
            value_list.pop(-1)
        price = float(value_list.pop(-1))
        unit = value_list.pop(-1)
        if unit == 'KILOGRAM':
            unit = 'Kg'
        quantity = float(value_list.pop(-1))
        product = (' '.join(value_list))
        for missing_index in missing_indexes:
            if missing_index == key+1:
                missing_item = all_text_list[missing_index].split(' ')
                product = product + ' ' + missing_item[0]

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
