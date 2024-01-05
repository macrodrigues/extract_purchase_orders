""" This script owns several functions to interact with gmail or send emails
with SMTP """

# pylint: disable=E1101
# pylint: disable=E1101
# pylint: disable=W0718
# pylint: disable=W0612
# pylint: disable=W0621
# flake8: noqa

import email
from email.header import decode_header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
import smtplib
import imaplib


def get_messsages_gmail(
        user_email,
        user_password,
        last_email=-1,
        email_folder='INBOX',
        from_email="All"):
    """This function extracts the messages objects from a gmail account"""

    # connect to gmail
    gmail = imaplib.IMAP4_SSL("imap.gmail.com")

    # sign in with your credentials
    gmail.login(user_email, user_password)

    # select the folder
    gmail.select(email_folder)

    if from_email == 'All':
        resp, items = gmail.search(None, from_email)
    else:
        resp, items = gmail.search(None, f"(FROM {from_email})")

    items = items[0].split()
    msgs = []
    for num in items[:last_email]:
        typ, message_parts = gmail.fetch(num, '(RFC822)')
        msgs.append(message_parts)

    return msgs


def get_attachments(msgs, data_folder, logger):
    """This function extracts the pdf and html files"""
    for msg_raw in msgs:
        if isinstance(msg_raw[0], tuple):
            msg = email.message_from_string(str(msg_raw[0][1], 'utf-8'))
            for part in msg.walk():
                print(part.get_filename())
                # Check if the part is an attachment
                logger.info(part.get_filename())
                if part.get('Content-Disposition') \
                        is not None and part.get_filename() is not None:
                    # Check if the filename contains the target string
                    error_file_strings = [
                        'Ordem_de_Compra',
                        'NH_MARINA_PORTIM',
                        'Pedido_Compra']
                    for error_str in error_file_strings:
                        if error_str in part.get_filename():
                            decoded_subject = decode_header(
                                part.get_filename())
                            decoded_subject_str = \
                                decoded_subject[0][0].decode(
                                    decoded_subject[0][1] or 'utf-8')
                            file_path = os.path.join(
                                data_folder,
                                decoded_subject_str)
                            logger.info("New path: %s", file_path)
                            # Save the file
                            with open(file_path, 'wb') as file:
                                file.write(part.get_payload(decode=True))

                if part.get_content_maintype() == 'multipart':
                    continue

                try:
                    if (".pdf" in part.get_filename())\
                            or (".PDF" in part.get_filename()
                                or ".xlsx" in part.get_filename()):
                        filename = part.get_filename()
                        file_path = os.path.join(data_folder, filename)

                        # Save the file
                        with open(file_path, 'wb') as file:
                            file.write(part.get_payload(decode=True))

                except Exception as error:
                    logger.error(str(error))
                    if "Invalid argument: " in str(error):
                        try:
                            filename = part.get_filename()
                            filename = filename.split(' - Gerado')[0] + '.pdf'
                            file_path = os.path.join(data_folder, filename)
                            # Save the file
                            with open(file_path, 'wb') as file:
                                file.write(part.get_payload(decode=True))
                        except Exception as error:
                            logger.error(str(error))



def send_email(results_folder, to_email, email, password, boolean):
    """ This function uses SMTP to send an email with all the txt
    attachments"""

    if boolean:
        message = MIMEMultipart()
        message["To"] = to_email
        message["From"] = email
        message["Subject"] = 'RESUMO E FICHEIROS PARA O SAGE'

        # list files
        file_list = os.listdir(results_folder)

        # iterate through the list and delete each file
        for filename in file_list:
            attachment = MIMEApplication(
                open(f"{results_folder}/{filename}", 'rb').read())
            attachment.add_header(
                'Content-Disposition',
                'attachment',
                filename=filename)
            message.attach(attachment)

        body = \
            "Em enexo os ficheiros .txt extraidos hoje:\n\n" \
            + '\n\n'.join(file_list) + "\n\n"

        message_text = MIMEText(body, 'plain')

        message.attach(message_text)

        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo('Gmail')
        server.starttls()
        server.login(email, password)
        server.sendmail(
            email,
            to_email,
            message.as_string())

        server.quit()
