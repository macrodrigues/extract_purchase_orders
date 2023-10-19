""" Group of functions to perform data processing on the pdfs of the
NH Hotel Group
"""
# pylint: disable=E1101
# pylint: disable=W0718
import re


def find_eight_consecutive_numbers(text):
    """This function finds 8 consecutive numbers, which will
    correspond to code of the product"""
    # This regex pattern matches exactly 6 consecutive digits
    pattern = r'\d{8}'
    matches = re.findall(pattern, text)
    return matches


def find_date(text):
    """ In duplicate rows, it can be that the date is glued to another value,
    we detect it using a regex function"""
    pattern = r'\d{2}/\d{2}/\d{4}'
    matches = re.findall(pattern, text)
    return matches


def extract_from_hotel_group(text):
    """ Extracts information from the HOTEL GROUP PO pdf"""
    # converts the string to a list of strings separated by '\n'
    list_text = text.split('\n')

    # iteration to find the indexes that contain the valuable information
    index_iterable_items = []
    for i, item in enumerate(list_text):
        digits_index = find_eight_consecutive_numbers(item)
        if digits_index:
            index_iterable_items.append(i)

    # in these pdfs, the first three are not important
    filt_list_of_indexes = index_iterable_items[3:]

    # filter items in text
    for index, filt_item in enumerate(
            [list_text[i] for i in filt_list_of_indexes]):
        try:
            code = find_eight_consecutive_numbers(filt_item)[0]
            filt_item_list = filt_item.replace(code, '').split(' ')
            try:
                total = float(filt_item_list[-1].replace(',', '.'))
                reference = filt_item_list.pop(1)
                unit = filt_item_list.pop(-2)
                price = filt_item_list.pop(-2)
                quantity = filt_item_list.pop(-2)
                date = filt_item_list.pop(-2)
                product = ' '.join(filt_item_list[2:-1])

            # this happens when one is not organized the same way
            # usually a value that is in two rows
            except Exception as error:
                print(error)
                duplicate_row = list_text[filt_list_of_indexes[index]+1]
                duplicate_row = ''.join([filt_item, duplicate_row])
                duplicate_row_list = duplicate_row.split(' ')
                duplicate_row_list = [item for item in duplicate_row_list
                                      if item != '']
                total = float(duplicate_row_list[-1].replace(',', '.'))
                reference = duplicate_row_list.pop(1)
                unit = duplicate_row_list.pop(-2)
                price = duplicate_row_list.pop(-2)
                quantity = duplicate_row_list.pop(-2)
                for element in duplicate_row_list:
                    date = find_date(element)
                    if date:
                        date = date[0]
                        duplicate_row_list = [
                            element.replace(date, '') if date
                            in element else element for element
                            in duplicate_row_list]
                    else:
                        pass

                product = ' '.join(duplicate_row_list[2:-1])

            return {
                'código': code,
                'produto': product,
                'referência': reference,
                'unidade': unit,
                'preço': price,
                'quantidade': quantity,
                'total': total
                }

        except Exception as error:
            print(error)
