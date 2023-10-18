import email, getpass, imaplib, os, re
from tqdm import tqdm

user = 'marcoacavaco.rodrigues@gmail.com'
password = "ghor tydw ggpn oayl"
imap = 'imap.gmail.com'

# connect to gmail
gmail = imaplib.IMAP4_SSL(imap)

# sign in with your credentials
gmail.login(user, password)

# get inbox no matter the language
inbox = str(gmail.list()[1][1])\
    .replace('"', '').replace('b', '')\
    .replace("'", '').split(' / ')[1]

# select the folder
gmail.select(inbox)

resp, items = gmail.search(None, '(FROM "no-reply@accounts.google.com")')
items = items[0].split()

msgs = []
for num in tqdm(items):
    typ, data = gmail.fetch(num, '(RFC822)')
    msgs.append(data)

for msg_raw in msgs:
    if type(msg_raw[0]) is tuple:
        msg = email.message_from_string(str(msg_raw[0][1], 'utf-8'))
        email_subject = msg['subject']
        try:
            email_subject = email.header.decode_header(email_subject)[0][0]\
                .decode('utf-8')
        except Exception as error:
            print(error)
            pass

        print(email_subject)

# encoded_string = "=?UTF-8?Q?Alerta_de_seguran=C3=A7a?="
# decoded_string = email.header.decode_header(encoded_string)[0][0].decode('utf-8')
# print(decoded_string)



    # print(msg)

# # Function to get the list of emails under this label
# def get_emails(result_bytes):
#     msgs = [] # all the email data are pushed inside an array
#     for num in result_bytes[0].split():
#         typ, data = gmail.fetch(num, '(RFC822)')
#         msgs.append(data)

#     return msgs
