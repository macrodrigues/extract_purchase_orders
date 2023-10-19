""" This function instantiates the .pdf object """
# pylint: disable=E0401
# pylint: disable=E1101
import PyPDF2

def read_pdf(file_path):
    # creating a pdf file object
    pdfFileObj = open(file_path,'rb')

    # creating a pdf reader object
    pdfReader = PyPDF2.PdfReader(pdfFileObj)

    # creating a page object
    pageObj = pdfReader.pages[0]

    return pageObj.extract_text()

def read_based_on_string(str_file):
    # jupyter lisboa hotel
    if 'JUPITER LISBOA HOTEL':
        pass
    # NH hotels
    if '-HOTELS.COM':
        pass
