import pdfplumber as pdfp
import re


def find_seven_consecutive_numbers(text):
    """This function finds 7 consecutive numbers, which will
    correspond to code of the product"""
    # This regex pattern matches exactly 6 consecutive digits
    pattern = r'\b\d{7}\b'
    matches = re.findall(pattern, text)
    return matches


def find_strings(text):
    """Uses a regex expression to find numerical values among strings."""
    pattern = r"[A-Za-z]"
    matches = re.findall(pattern, text)
    return matches


def find_date(text):
    """ Detect date using a regex function"""
    pattern = r'\d{2}/\d{2}/\d{4}'
    matches = re.findall(pattern, text)
    return matches


def extract_tables_onyria(path):
    """ Extracts information from the ONYRIA pdf"""
    pdf = pdfp.open(path)
    data = []
    units_list = ['Kg', 'L', 'Un']
    first_page = pdf.pages[0]
    first_page_text = first_page.extract_text().split('\n')
    order = first_page_text[0].split('#')[1]
    dates = []
    for element in first_page_text:
        date = find_date(element)
        if date:
            dates.append(date[0])
    date = dates[0]
    for page in pdf.pages:
        table = page.extract_table()
        for element in table:
            reference = find_seven_consecutive_numbers(element[0])
            if reference:

                element = [item for item
                           in element if item != '-']
                element = [item for item
                           in element if item != '']
                element = [item.replace('\n€', '').strip() for item
                           in element]
                element = [item.replace(' €', '').strip() for item
                           in element]
                element = element[1:]
                element = element[:-4]
                str_value = find_strings(element[1])
                if str_value:
                    element.pop(1)
                product = element[0].replace('(c)', '').strip()
                if '\n' in product:
                    product = product.split('\n')[0]
                quantity = float(element[1].replace(',', '.'))
                unit = element[2]
                price = float(element[-1].replace(',', '.'))
                if unit not in units_list:
                    unit = 'Kg'
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
