""" This function instantiates the .pdf object """
# pylint: disable=E0401
# pylint: disable=E1101
# pylint: disable=W0718
# pylint: disable=W0612
import PyPDF2
import pdfkit
import pandas as pd


def read_excel(file_path):
    """ this function reads the excel files"""
    df = pd.read_excel(file_path, engine='xlrd')
    print(df)


def read_pdf(file_path) -> str:
    """This uses PyPDF to read the content from a pdf file"""

    # creating a pdf file object
    pdf_object = open(file_path, 'rb')

    # creating a pdf reader object
    pdf_reader = PyPDF2.PdfReader(pdf_object, strict=True)

    # count pages
    count = len(pdf_reader.pages)

    # extract content from several pages
    output = ''
    for i in range(count):
        page = pdf_reader.pages[i]
        output += page.extract_text()

    return str(output)


def convert_to_pdf(file_path):
    """ This function converts html to pdf"""
    new_filepath = str(file_path).replace('.html', '.pdf')
    pdfkit.from_file(
        file_path,
        new_filepath,
        options={"enable-local-file-access": True})


def read_pdf_network(
        str_raw, networks, clients_dataset, logger, file_path) -> dict:
    """ Each string has a key string to trigger one of
    the following functions"""

    for index, row in clients_dataset.iterrows():
        if row.client in str_raw:
            try:
                if row.network == 'ONYRIA':
                    res = networks[row.network](file_path)
                    res['client'] = row.client
                    res['client_num'] = row.number
                    res['network'] = row.network
                    return res
                if row.network == 'FONTANA HOTELS':
                    res = networks[row.network](file_path)
                    res['client'] = row.client
                    res['client_num'] = row.number
                    res['network'] = row.network
                    return res

                if row.network == 'MOURASTOCK':
                    res = networks[row.network](file_path)
                    res['client'] = row.client
                    res['client_num'] = row.number
                    res['network'] = row.network
                    return res

                if row.network == 'ASTORE SHOP':
                    res = networks[row.network](file_path)
                    res['client'] = row.client
                    res['client_num'] = row.number
                    res['network'] = row.network
                    return res

                if row.network == 'AZIPARQUE':
                    res = networks[row.network](file_path)
                    res['client'] = row.client
                    res['client_num'] = row.number
                    res['network'] = row.network
                    return res

                if row.network == 'HOTELEIRA DE SETE RIOS':
                    res = networks[row.network](file_path)
                    res['client'] = row.client
                    res['client_num'] = row.number
                    res['network'] = row.network
                    return res

                if row.network == 'PORTO BAY':
                    res = networks[row.network](file_path)
                    res['client'] = row.client
                    res['client_num'] = row.number
                    res['network'] = row.network
                    return res

                else:
                    res = networks[row.network](str_raw)
                    res['client'] = row.client
                    res['client_num'] = row.number
                    res['network'] = row.network
                    return res

            except Exception as error:
                logger.error(str(error))
