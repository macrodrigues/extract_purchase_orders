""" This function instantiates the .pdf object """
# pylint: disable=E0401
# pylint: disable=E1101
import PyPDF2
from extract_hotel_group import extract_from_hotel_group
from extract_jupiter_hotel import extract_from_jupyter_hotel
from extract_onyria import extract_from_onyria


def read_pdf(file_path) -> str:
    """This uses PyPDF to read the content from a pdf file"""
    # creating a pdf file object
    pdf_object = open(file_path, 'rb')

    # creating a pdf reader object
    pdf_reader = PyPDF2.PdfReader(pdf_object, strict=True)

    pdf_reader = pdf_reader.pages[0]

    text = pdf_reader.extract_text()

    pdf_object.close()

    return text


def read_based_on_string(str_raw) -> dict:
    """ Each string has a key string to trigger one of
    the following functions"""
    # jupyter lisboa hotel
    if 'JUPITER LISBOA HOTEL' in str_raw:
        print('here')
        return extract_from_jupyter_hotel(str_raw)
    # NH hotels
    if '-HOTELS.COM' in str_raw:
        return extract_from_hotel_group(str_raw)

    # Onyria
    if 'ESTE DOCUMENTO NÃO SERVE DE FATURA' in str_raw:
        return extract_from_onyria(str_raw)
