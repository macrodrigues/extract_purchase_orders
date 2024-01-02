""" Script containing the Google interaction functions.

One for authentication, one for reading and one for uploading.

"""
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials


def google_authentication(credentials) -> object:
    """ This function gives authentication to the Google Account.

    Scopes defines the permissions to Googe Sheets and Google Drive.
    Than, using gspread, it authorizes the authentication and
    opens the the worksheet to work with.

    """
    # Authenticate with Google Sheets using the JSON key file
    scope = ['https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive']

    creds = Credentials.from_service_account_file(
        credentials, scopes=scope)

    client = gspread.authorize(creds)

    return client


def create_worksheet(client, sheet_id, worksheet_index, worksheet_name):
    """Creates a new worksheet"""
    # Open the Google Sheet by id
    sheet = client.open_by_key(sheet_id)

    # create worksheet
    sheet.add_worksheet(worksheet_name, rows=100, cols=10)

    worksheet = sheet.get_worksheet(worksheet_index)

    return worksheet


def read_from_google(sheet) -> pd.DataFrame:
    """ This function reads the data from the Google Sheet. """

    ws = sheet.worksheet('codes')
    df_previous = pd.DataFrame(data=ws.get_all_records())
    return df_previous


def upload_to_google(df, sheet):
    """ This function uploads the data to a google sheet.

    It takes the worksheet object created in google_authentication(), and
    writes data from a dataframe to it.

    """

    # Convert the DataFrame to a list of lists
    data = df.values.tolist()

    # Clear existing data and update the Google Sheet with new data
    sheet.clear()

    # Convert the DataFrame headers to a list and insert as the first row
    header_row = df.columns.tolist()
    sheet.insert_rows([header_row], row=1)

    # insert the full data
    sheet.insert_rows(data, row=2)
