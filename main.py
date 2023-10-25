""" Main function """

# pylint: disable=E0401
# pylint: disable=W0622
# pylint: disable=C0411
import os
import pandas as pd
from rich import print
from read_pdf import read_pdf, read_based_on_string
from extract_gmail import get_messsages_gmail, get_pdf_attachments
from dotenv import load_dotenv
load_dotenv('keys.env')

EMAIL = os.getenv('my_email')
PASSWORD = os.getenv('my_password')
OUTPUT_FOLDER = 'data'

if __name__ == '__main__':
    # get messages
    msgs = get_messsages_gmail(
        EMAIL,
        PASSWORD,
        "Intercunhados",
        "All")

    # get .pdfs from messages
    get_pdf_attachments(msgs, OUTPUT_FOLDER)

    # make a list of all .pdf items extracted
    items = os.listdir(OUTPUT_FOLDER)

    for item in items:
        text = read_pdf(f"{OUTPUT_FOLDER}/{item}")
        try:
            data = read_based_on_string(text)

            # Load the DataFrames
            df_codes = pd.read_csv('lista_codigos.csv')

            # Create a dictionary to map products to codes
            product_to_code = dict(zip(df_codes['product'], df_codes['code']))

            if data['dados'][0]['código'] is None:
                new_data = []
                for item in data['dados']:
                    for key in list(product_to_code.keys()):
                        if item['produto'].upper() == key.upper():
                            item['código'] = product_to_code[key]
                        else:
                            pass

                    new_data.append(item['código'])

                # replace them in data['dados'].
                for i, item in enumerate(data['dados']):
                    item['código'] = new_data[i]

            # Iterate through your data and create Excel files
            for item in data:
                client_name = item['client']

                # Create an Excel writer for the client
                excel_writer = pd.ExcelWriter(f'{client_name}.xlsx', engine='xlsxwriter')

                for data_item in item['data']:
                    date = data_item['year']
                    df = pd.DataFrame([data_item])

                    # Write the DataFrame to a worksheet with the corresponding date as the name
                    df.to_excel(excel_writer, sheet_name=str(date), index=False)

                # Save the Excel file
                excel_writer.save()

        except Exception as error:
            print(error)
