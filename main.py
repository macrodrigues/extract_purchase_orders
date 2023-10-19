""" Main function """

# pylint: disable=E0401
# pylint: disable=W0622
from rich import print
from read_pdf import read_pdf, read_based_on_string

text = read_pdf('files/NH_HOTEL_GROUP/06.pdf')

data = read_based_on_string(text)

print(data)
