""" Main function """

# pylint: disable=E0401
# pylint: disable=W0622
import os
from rich import print
from read_pdf import read_pdf, read_based_on_string

items = os.listdir('data')

for item in items:
    text = read_pdf(f"data/{item}")
    # text = read_pdf(f"files/JUPYTER_HOTEL/01.pdf")
    try:
        data = read_based_on_string(text)
        print(data)
    except Exception as error:
        print(error)
