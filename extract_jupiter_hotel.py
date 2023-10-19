# importing required modules
# pylint: disable=E1101
import PyPDF2
import re


def find_six_consecutive_numbers(text):
    """This function finds 6 consecutive numbers, which will
    correspond to code of the product"""
    # This regex pattern matches exactly 6 consecutive digits
    pattern = r'\b\d{6}\b'
    matches = re.findall(pattern, text)
    return matches


def detect_weight(text):
    """This function uses a regex expression to detect weight
    according to different units"""
    # This regex pattern detects the weight
    patterns = [
        r'[\d\s,]+?(?= ?KG)',  # KG
        r'[\d\s,]+?(?= ?GF5)',  # GF5
        r'[\d\s,]+?(?= ?UN)']  # UN
    matches = [re.findall(pattern, text) for pattern in patterns]
    res = [item for match in matches for item in match]
    return ''.join(res).strip()


def find_tax(text):
    """This uses a regex expression to find the tax letter"""
    pattern = r' [A-Z] '
    matches = re.findall(pattern, text)
    return matches[0]


def detect_discounts(text):
    """this detects the discount item using a regex function"""
    pattern = r'0,00 ?0,00'
    matches = re.findall(pattern, text)
    return matches[0]


def glued_values(text):
    """there are some entries that are joined (glued)
    this function triggers after a an exception and uses a regex expression
    to find a number next to a comma"""
    # Matches a single digit followed by a comma
    pattern = r'\d,'
    matches = re.findall(pattern, text)
    return matches


def find_missing_numbers(indexes):
    """When iterating, some products have the continuation of the product's
    name in the next line. I use this function do find the missing number index
    to later use it to grab the extra information of the product"""
    missing_numbers = []
    for i in range(1, len(indexes)):
        if indexes[i] != indexes[i - 1] + 1:
            for missing in range(indexes[i - 1] + 1, indexes[i]):
                missing_numbers.append(missing)
    return missing_numbers


# creating a pdf file object
pdfFileObj = open(
    'files/20231013103648_EF_A2023_2988_2023_50_1_638327902080208927.pdf',
    'rb')

# creating a pdf reader object
pdfReader = PyPDF2.PdfReader(pdfFileObj)

# creating a page object
pageObj = pdfReader.pages[0]

text = pageObj.extract_text()

if 'JUPITER LISBOA HOTEL' in text:
    list_text = text.split('\n')
    last_index = 0
    index_iterable_items = []
    for i, item in enumerate(list_text):
        if find_six_consecutive_numbers(item[:6]):
            # make sure to not take index to further way from the main ones
            if i <= last_index + 2:
                last_index = i
                index_iterable_items.append(i)

    # find missing indexes
    missing_indexes = find_missing_numbers(index_iterable_items)
    filtered_items = [list_text[i] for i in index_iterable_items]
    for index, filt_item in enumerate(filtered_items):
        code = filt_item[:6]
        filt_item = filt_item.replace(code, '')
        total = detect_weight(filt_item)
        # filt_item = filt_item.replace(total, '').lstrip()
        discount = detect_discounts(filt_item)
        filt_item = filt_item.replace(discount, '- ').lstrip()
        filt_item = filt_item.split('-')
        tax = find_tax(filt_item[1])
        product = filt_item[1].replace(tax, '')
        filt_item = filt_item[0].split(' ')
        filt_item = [item for item in filt_item if item != '']
        try:
            for value in filt_item:
                total = filt_item[0]
                unit = filt_item[1]
                quantity = filt_item[2]
                price = filt_item[3]
        except Exception as error:
            print(error)
            list_of_units = ['KG', 'UN', 'GF5']
            for i in list_of_units:
                if i in value:
                    unit = i
                    value = value.split(i)
                    total = value[0]
                    glued = glued_values(value[1])
                    quantity = value[1].split(glued[1])[0]
                    price = value[1].replace(quantity, '')

        # Add string from missing index
        for missing_index in missing_indexes:
            if missing_index == index + 1:
                product = product + ' ' + list_text[missing_index]

        res = {
            'Código': code,
            'Designação': product,
            'Unidade': unit,
            'Impostos': tax,
            'Preço unitário': float(price.replace(',', '.')),
            'Quantidade': float(quantity.replace(',', '.')),
            'Total': float(price.replace(',', '.'))*float(quantity.replace(',', '.'))
        }

        print(res)
        print('\n')

# closing the pdf file object
pdfFileObj.close()
