""" This script serves to make configurations"""

import os
from functions.network_extraction.extract_hotel_group import \
    extract_from_hotel_group
from functions.network_extraction.extract_jupiter_hotel import \
    extract_from_jupyter_hotel
from functions.network_extraction.extract_onyria import \
    extract_tables_onyria
# from functions.extract_emerald_hotel import extract_from_emerald_hotel
from functions.network_extraction.extract_astore import \
    extract_from_astore_shop
from functions.network_extraction.extract_mourastock import \
    extract_from_mourastock
from functions.network_extraction.extract_fontana import \
    extract_tables_fontana
from functions.network_extraction.extract_aziparque_n_more import \
    extract_from_aziparque_n_more
from functions.network_extraction.extract_emerald_hotel import \
    extract_from_emerald_hotel
from functions.network_extraction.extract_portobay import \
    extract_from_portobay

# dictionaries for the google sheets
DICTIONARY_GOOGLE_SHEETS = {
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

# list of networks
NETWORKS_LISTS = {
    'ASTORE SHOP': [],
    'NH HOTEL GROUP': [],
    'JUPITER HOTEL': [],
    'FONTANA HOTELS': [],
    'EMERALD': [],
    'ONYRIA': [],
    'MOURASTOCK': [],
    'AZIPARQUE': [],
    'PORTO BAY': [],
    'HOTELEIRA DE SETE RIOS': []}

# networks functions
NETWORKS_FUNCTIONS = {
    'ASTORE SHOP': extract_from_astore_shop,
    'NH HOTEL GROUP': extract_from_hotel_group,
    'JUPITER HOTEL': extract_from_jupyter_hotel,
    'EMERALD': extract_from_emerald_hotel,
    'ONYRIA': extract_tables_onyria,
    'FONTANA HOTELS': extract_tables_fontana,
    'MOURASTOCK': extract_from_mourastock,
    'AZIPARQUE': extract_from_aziparque_n_more,
    'HOTELEIRA DE SETE RIOS': extract_from_aziparque_n_more,
    'PORTO BAY': extract_from_portobay
}
