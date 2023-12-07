import pdfplumber as pdfp
import re
from rich import print


def find_five_consecutive_numbers(text):
    """This function finds 11 consecutive numbers, which will
    correspond to code of the product"""
    # This regex pattern matches exactly 6 consecutive digits
    pattern = r'\b\d{5}\b'
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


def extract_from_portobay(path) -> dict:
    """ Extracts information from Aziparque and morepdf"""
    pdf = pdfp.open(path)
    first_page = pdf.pages[0]
    first_page_text = first_page.extract_text().split('\n')
    for item in first_page_text:
        if "Pedido Nº" in item:
            order = item.split('Nº')[-1].strip()
        if "Rua do Progresso" in item:
            date = item.split(' ')[0].strip()
            date = date.replace('.', '/')

    all_text = []
    for page in pdf.pages:
        text = page.extract_text()
        all_text.append(text)

    all_text = '\n'.join(all_text)
    all_text_list = all_text.split('\n')

    index_iterable_items = []
    for i, item in enumerate(all_text_list):
        digits_index = find_five_consecutive_numbers(item)
        if digits_index:
            index_iterable_items.append(i)

    # append to data list
    data = []

    # filter items in text list
    filtered_items = filter_items(index_iterable_items, all_text_list)

    for key, value in filtered_items.items():
        filt_list = value.split(' ')
        filt_list = filt_list[2:]
        filt_list.pop(-1)
        price = filt_list.pop(-1)
        price = float(price.replace(',','.'))
        unit = filt_list.pop(-1)
        quantity = filt_list.pop(-1)
        quantity = float(quantity.replace(',', '.'))
        product = ' '.join(filt_list)
        data.append(
                {
                    'código': None,
                    'produto': product,
                    'quantidade': quantity,
                    'unidade': unit,
                    'preço': price,
                    'total': price*quantity})

    return {
        'order': order,
        'date': date,
        'data': data}
