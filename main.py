""" Main function """

# pylint: disable=E0401
# pylint: disable=W0622
# pylint: disable=W0718
# pylint: disable=C0411
# pylint: disable=abstract-class-instantiated
import os
import pandas as pd
import time
import shutil
from datetime import datetime
from functions.read_documents import read_pdf, read_pdf_network
from functions.read_documents import read_excel, convert_to_pdf
from functions.gmail_interactions import get_messsages_gmail
from functions.gmail_interactions import get_attachments
from functions.gmail_interactions import send_email
from functions.google_access import google_authentication, create_worksheet
from functions.google_access import upload_to_google, read_from_google
from dotenv import load_dotenv
load_dotenv('keys.env')


def activate_extraction(
    boolean,
    email,
        password, last_email, email_folder, email_address, files_path, logger):
    """This function activates the extraction of files when set to True"""
    if boolean:
        # get messages
        msgs = get_messsages_gmail(
            email,
            password,
            last_email,
            email_folder,
            email_address)

        # get .pdfs from messages
        logger.info('Gmail extraction started...')
        get_attachments(msgs, files_path, logger)
    else:
        pass


def get_all_data(
        files, networks_functions, codes_sheet_id,
        clients_sheet_id, files_path, rejected_path, logger) -> list:
    """ This function iterates over the files """
    list_of_data_dict = []
    # iterate over the files

    for filename in files:
        if '.html' in filename:
            convert_to_pdf(f"{files_path}/{filename}")

    # google authentication
    google_client = google_authentication('credentials.json')
    sheet_product_codes = google_client.open_by_key(codes_sheet_id)
    sheet_clients_codes = google_client.open_by_key(clients_sheet_id)

    # load a dataframe of clients and products from Google
    df_clients = read_from_google(sheet_clients_codes)
    df_codes = read_from_google(sheet_product_codes)

    # make a list of all .pdf items extracted
    new_filenames = os.listdir(files_path)
    for filename in new_filenames:
        try:  # if it reads
            if '.xlsx' in filename:
                data = read_excel(f"{files_path}/{filename}")
            else:
                text = read_pdf(f"{files_path}/{filename}")

                data = read_pdf_network(
                    text,
                    networks_functions,
                    df_clients,
                    logger,
                    file_path=f"{files_path}/{filename}")

            # create a dictionary to map products to codes
            product_to_code = dict(
                zip(df_codes['product'], df_codes['code']))

            # in case the code is None, tries to match with the list of codes
            if data['data'][0]['código'] is None:
                new_data = []
                for filename in data['data']:
                    for key in list(product_to_code.keys()):
                        if (filename['produto'].upper() == key.upper())\
                         or (filename['produto'] == key):
                            filename['código'] = product_to_code[key]
                        else:
                            pass

                    new_data.append(filename['código'])

                # replace new codes in data['data']
                for i, item in enumerate(data['data']):
                    item['código'] = new_data[i]

            list_of_data_dict.append(data)

        except Exception as error:
            if 'object is not subscriptable' in str(error):
                logger.error(f"{str(error)}: {filename}")
                shutil.copy2(
                    f"{files_path}/{filename}",
                    f"{rejected_path}/{filename}")
            else:
                logger.error(f"{str(error)}: {filename}")

    return list_of_data_dict


def create_networks_lists(
        list_of_dictionaries, networks_lists, input_dates, logger) -> dict:
    """This function iterates over a list of dictionaries
    and saves the data for each network in another dictionary, where the
    key is the networks's name and the value is a list of dictionaries"""

    dates_list = []
    for element in list_of_dictionaries:
        for key, value in element.items():
            if key == 'date':
                if len(value.split('/')[0]) == 1:
                    list_date = value.split('/')
                    list_date[0] = '0' + value.split('/')[0]
                    element['date'] = '/'.join(list_date)
                    dates_list.append('/'.join(list_date))
                else:
                    dates_list.append(value)

    # Use the sorted function with the custom key
    dates_list = list(set(dates_list))
    dates_list.sort(key=lambda date: datetime.strptime(date, "%d/%m/%Y"))
    input_dates = [input_date.split('-') for input_date in input_dates]
    new_input_list = []
    for element_input_date in input_dates:
        element_input_date[0], element_input_date[-1] = \
            element_input_date[-1], element_input_date[0]
        new_input_list.append(element_input_date)
    new_input_list = ['/'.join(input_date) for input_date in new_input_list]

    logger.info(dates_list)
    logger.info(new_input_list)

    # iterate over the list of dictionaries and create add the data
    # to the networks dictionary
    for dictionary in list_of_dictionaries:
        for input_date in new_input_list:
            # if (dictionary['date'] == dates_list[-1])\
            #         or (dictionary['date'] == dates_list[-2]):
            # if (dictionary['date'] == dates_list[-2]):
            if dictionary['date'] == input_date:
                logger.info(dictionary)
                df = pd.DataFrame(dictionary['data'])
                res = {
                    'date': dictionary['date'],
                    'client': dictionary['client_num'],
                    'order': dictionary['order'],
                    'data': df}

                networks_lists[dictionary['network']].append(res)

    return networks_lists


def format_and_upload(dictionary_list, network, logger):
    """ This function groups the the dataframes per client and order
    and then uploads them into google sheets.
    Worksheets are organized by network"""

    dictionary_sheets = {
        'ASTORE SHOP': os.getenv('id_astore'),
        'NH HOTEL GROUP': os.getenv('id_nh_group_hotel'),
        'JUPITER HOTEL': os.getenv('id_jupiter_hotel'),
        'ONYRIA': os.getenv('id_onyria'),
        'EMERALD': os.getenv('id_emerald_hotel'),
        'MOURASTOCK': os.getenv('id_mourastock'),
        'AZIPARQUE': os.getenv('id_aziparque'),
        'PORTO BAY': os.getenv('id_portobay'),
        'HOTELEIRA DE SETE RIOS': os.getenv('id_sete_rios'),
        'FONTANA HOTELS': os.getenv('id_fontana')}

    try:
        formatted_data = {}
        for element in dictionary_list:
            formatted_key = f"{element['order']} | {element['client']}"
            formatted_data[formatted_key] = element['data']

        # check for existing worksheets
        google_client = google_authentication('credentials.json')
        sheet = google_client.open_by_key(dictionary_sheets[network])

        # delete current worksheets
        for worksheet in list(sheet.worksheets())[1:]:
            id = str(worksheet).split('id:')[1].replace('>', '')
            sheet.del_worksheet_by_id(id)

        # list worksheets
        n_worksheets = len(sheet.worksheets())

        # add worksheets with dates and clients
        dates_n_clients = list(formatted_data.keys())
        logger.info('Upload Google Sheets Starts!')
        logger.info(network)
        for i, date_client in enumerate(dates_n_clients):
            try:
                logger.info(date_client)
                logger.info('waiting...')  # to overcome quotas
                time.sleep(5)
                worksheet = create_worksheet(
                    google_client,
                    dictionary_sheets[network],
                    i+n_worksheets,
                    date_client)

                # upload to google sheet
                upload_to_google(
                    formatted_data[date_client],
                    worksheet)
            except Exception as error:
                logger.error(str(error))
                time.sleep(60)
                continue

        return formatted_data

    except Exception as error:
        logger.error(str(error))


def make_totals_sheet(networks_dictionary):
    """This function takes the the networks dictionary,
    and concatenates all entries in order to visualize the total data"""
    totals = []
    for network in list(networks_dictionary.keys()):
        for element in networks_dictionary[network]:
            df = element['data']
            df['data'] = element['date']
            totals.append(df)

    total = pd.concat(totals, axis=0, ignore_index=True)

    total['data'] = pd.to_datetime(total['data'])
    total['unit'] = total['unidade']
    total['unidade'] = total['unit'].apply(lambda x: 1 if x == 'Un' else 0)
    total['litros'] = total['unit'].apply(lambda x: 1 if x == 'L' else 0)
    total['kilogramas'] = total['unit'].apply(lambda x: 1 if x == 'Kg' else 0)
    total = total[total['data'] == total['data'].max()]
    total = total[
        ['código',
         'unidade',
         'litros',
         'kilogramas',
         'quantidade',
         'preço',
         'total']]

    total = total.groupby('código').sum()
    total.reset_index(inplace=True)

    # make google client
    google_client = google_authentication('credentials.json')
    sheet = google_client.open_by_key(os.getenv('id_total'))

    # get existing worksheet
    worksheet = sheet.get_worksheet(0)

    # clear existing information
    worksheet.clear()

    # upload to google sheet
    upload_to_google(
        total,
        worksheet)

    return total


def delete_files(files_folder, output_folder, boolean=True):
    """This function deletes all content in the folder if sets to True """

    if boolean:
        # delete files
        file_list = os.listdir(files_folder)
        output_list = os.listdir(output_folder)

        # iterate through the list and delete each file
        for filename in file_list:
            file_path = os.path.join(files_folder, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

        # iterate through the list and delete each file
        for filename in output_list:
            file_path = os.path.join(output_folder, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)


def save_as_txt(data_filtered, path):
    """This function receives the data filtered and creates txt files for every
    day and client."""
    filt_dictionary = {k: v for d in data_filtered for k, v in d.items()}

    for filt_key, filt_value in filt_dictionary.items():
        filt_key = filt_key.replace(' | ', '_').replace('/', '_')
        filt_value.drop(
            ['produto', 'total', 'unidade'], axis=1, inplace=True)
        filt_value.to_csv(
            f"{path}/resultados/{filt_key}.txt",
            header=None,
            index=None,
            mode='a',
            sep=';')


def launch_extraction(
    extraction_activated,
    main_path,
    networks_lists,
    networks_functions,
    email,
    password,
    last_email,
    email_folder,
    email_address,
    files_path,
    rejected_path,
        codes_id, clients_id, input_dates, logger):

    """ Function with the extraction steps """
    # This function activates the extraction of files when set to True
    activate_extraction(
        extraction_activated,
        email,
        password,
        last_email,
        email_folder, email_address, files_path, logger)

    # make a list of all .pdf and .xlsx items extracted
    filenames = os.listdir(files_path)

    # this function gets all the dictionaries in the variable "data_dicts"
    data_dicts = get_all_data(
        filenames, networks_functions,
        codes_id, clients_id, files_path, rejected_path, logger)

    # concatenate dates and organize data by network lists
    networks_data_list = create_networks_lists(
        data_dicts, networks_lists, input_dates, logger)

    # format and upload to Google Sheets
    filtered_all = []
    for key in list(networks_data_list.keys()):
        filtered_dictionaries_per_network = format_and_upload(
            networks_data_list[key], key, logger)
        filtered_all.append(filtered_dictionaries_per_network)

    # save data as txt files
    save_as_txt(filtered_all, main_path)
