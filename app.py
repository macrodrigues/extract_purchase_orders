""" Script to launch the Graphic User Interface"""

import os
import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox
import csv
from tkinter.scrolledtext import ScrolledText
from config import NETWORKS_LISTS, NETWORKS_FUNCTIONS
from main import launch_extraction
import datetime
from functions.logging import gen_logger
from functions.google_access import google_authentication
from dotenv import load_dotenv
load_dotenv('keys.env')

# set up variables
PATH = os.getcwd()
EMAIL = os.getenv('inter_email')
PASSWORD = os.getenv('inter_password')
EMAIL_FOLDER = "Encomendas"
EMAIL_ADDRESS = 'All'
LAST_EMAIL = -1
FILES_FOLDER = os.path.join(PATH, "ficheiros_extraidos")
FILES_REJECTED = os.path.join(PATH, "ficheiros_rejeitados")
OUTPUTS_FOLDER = os.path.join(PATH, "resultados")
CODES_ID = os.getenv('codes_products_id')
CLIENTS_ID = os.getenv('codes_clients_id')
LOGGER = gen_logger(PATH)


class Fonts:
    """ Class to define the fonts to used in the application"""
    def __init__(self):
        self.font0 = tkFont.Font(
            size=25, weight='bold', underline=0)
        self.font1 = tkFont.Font(
            size=10, slant='italic')
        self.font2 = tkFont.Font(
            size=11, weight='bold')
        self.font3 = tkFont.Font(
            size=8, weight='bold')
        self.font4 = tkFont.Font(
            size=10)


class App:
    """ This class build the tkinter GUI"""
    def __init__(self):
        self.win = tk.Tk()
        self.checkVar = tk.IntVar()
        self.selected_dates = []
        self.win.title('Intercunhados - Simplicador v0.4')
        self.canvas = tk.Canvas(
            self.win,
            width=580,
            height=640,
            bg='#E6FF6F')
        self.canvas.pack(expand=True)
        self.win.minsize(580, 640)
        self.win.maxsize(580, 640)
        self.create_main_frame()
        self.create_description()
        self.dates_frame()

    def create_main_frame(self):
        """Function to create the main frame"""
        self.main_frame = tk.Frame(self.win, bg='white')
        self.main_frame.place(
            relwidth=0.9, relheight=0.9, rely=0.05,  relx=0.05)

    def create_description(self):
        """Adds a title and description to the intro frame"""
        # a text to add to description and make the line shorter
        text_extract = "Simplificador para extrair documentos"
        self.intro_frame = tk.Frame(self.main_frame, bg='white')
        self.intro_frame.pack()
        self.label_title = tk.Label(
            self.intro_frame,
            text="Intercunhados",
            foreground='#5A8A29',
            bg='white')
        self.label_title['font'] = Fonts().font0
        self.label_title.pack(side='top', pady=10)
        self.label_intro_frame = tk.Label(
            self.intro_frame,
            bg='white',
            text=f"{text_extract} .pdf e .xlsx do email")
        self.label_intro_frame['font'] = Fonts().font1
        self.label_intro_frame.pack(side='top', pady=10)
        self.label2_intro_frame = tk.Label(
            self.intro_frame,
            text="Os resultados estão disponíveis no Google Drive."
            "\nPara aceder utilize as seguintes credencias: \n\n"
            "           • Email: intercunhadosdev@gmail.com \n"
            "           • Password: Cunhadosdevinter0548",
            bg='white',
            justify="left")
        self.label2_intro_frame['font'] = Fonts().font4
        self.label2_intro_frame.pack(pady=20, fill='both', anchor='w')

    def dates_frame(self):
        options_labels = {}
        for i in range(7):
            date_key = str(
                datetime.datetime.today().date() - datetime.timedelta(days=i))
            options_labels[date_key] = tk.IntVar()
        self.label_date = tk.Label(
            self.main_frame,
            text="Escolher data(s): ",
            bg='white',
            font=Fonts().font3)
        self.label_date.pack(pady=5)

        def get_selection():
            items_dates = {}
            for k, v in options_labels.items():
                items_dates[k] = v.get()
            list_of_dates = []
            for k, v in items_dates.items():
                if v == 1:
                    list_of_dates.append(k)
            self.selected_dates = list_of_dates

        for k, v in options_labels.items():
            self.options = tk.Checkbutton(
                self.main_frame,
                text=k,
                variable=v,
                onvalue=1,
                offvalue=0,
                command=get_selection,
                justify='right',
                bg='white')
            self.options.pack(pady=5)
        self.upload_dates_btn = tk.Button(
            self.main_frame,
            text='Ok!',
            command=self.add_dates,
            bg='#62AC3D',
            activebackground='#5A8A29',
            fg='#FFFFFF')
        self.upload_dates_btn['font'] = Fonts().font3
        self.upload_dates_btn.pack(pady=5)

    def main_page(self):
        """ This function adds the main widgets to the main page"""
        self.set_button_codes()
        self.set_scroll_codes()
        self.set_button1()
        self.loading_label = tk.Label(
            self.main_frame,
            text="Esperar entre 3 a 10 minutos...",
            bg='white',
            font=Fonts().font3)
        self.loading_label.pack_forget()
        self.complete_label = tk.Label(
            self.main_frame,
            text="Completo! Ver pasta 'resultados'",
            bg='white',
            font=Fonts().font3)
        self.complete_label.pack_forget()
        # self.set_button2()

    def set_scroll_codes(self):
        """ Creates a label followed by a scrolled widget and a button """
        self.codes_label = tk.Label(
            self.main_frame,
            text="Ver os códigos que faltam no Google Drive, adicionar aqui\n"
            "e executar de novo a extração antes de submeter no Sage.\n"
            "Adicione os códigos em falta da seguinte forma:\n\n"
            "Exemplo:\n\nE97,REBENTOS ERVILHA\nA34,SALSA FRISADA\n\n"
            "Não deixe espaços entre a virgula!",
            justify="left",
            bg='white',
            font=tkFont.Font(size=7))
        self.codes_label.pack_forget()
        self.st = ScrolledText(self.main_frame, width=34, height=5)
        self.st.pack_forget()
        self.ready_codes_btn = tk.Button(
            self.main_frame,
            text='Submeter',
            command=self.add_codes,
            bg='#62AC3D',
            activebackground='#5A8A29',
            fg='#FFFFFF')
        self.ready_codes_btn['font'] = Fonts().font3
        self.ready_codes_btn.pack_forget()

    def set_button_codes(self):
        """ Button to add missing codes to the list of codes"""
        self.button_codes = tk.Button(
            self.main_frame,
            text='Adicionar códigos em falta',
            command=self.create_codes_frame,
            bg='#62AC3D',
            activebackground='#5A8A29',
            fg='#FFFFFF')
        self.button_codes['font'] = Fonts().font3
        self.button_codes['width'] = 25
        self.button_codes.pack(pady=5)

    def set_button1(self):
        """Button to extract the documents from the gmail"""
        self.button1 = tk.Button(
            self.main_frame,
            text='Extrair documentos para Sage',
            command=self.extract_main_function,
            bg='#62AC3D',
            activebackground='#5A8A29',
            fg='#FFFFFF')
        self.button1['font'] = Fonts().font3
        self.button1['width'] = 25
        self.button1.pack(pady=5)

    def create_codes_frame(self):
        """ Adds the label, the scrolled and a button"""
        self.button1.destroy()
        self.button_codes.destroy()
        self.complete_label.pack_forget()
        self.codes_label.pack(pady=5)
        self.st.pack()
        self.ready_codes_btn.pack(pady=5)
        self.win.update()

    def add_dates(self):
        if self.selected_dates:
            self.options.destroy()
            self.label_date.destroy()
            self.upload_dates_btn.destroy()
            self.create_main_frame()
            self.create_description()
            self.main_page()
        else:
            messagebox.showerror("Erro", "Não foi selecionada nenhuma data! ")

    def add_codes(self):
        """ This function adds the missing codes to the code_list.csv"""
        input_text = self.st.get("1.0", tk.END)
        values_list = input_text.split('\n')
        values_list = [value.strip() for value in values_list]
        values_list = [value.split(',') for value in values_list]

        # add to google sheet
        google_client = google_authentication('credentials.json')
        sheet_product_codes = google_client.open_by_key(CODES_ID)
        ws = sheet_product_codes.worksheet('codes')
        ws.append_rows(values_list[:-1])

        self.create_main_frame()
        self.create_description()
        self.main_page()

    def extract_main_function(self):
        """ Extract all data, upload to Google Sheets and folder
        with txt files"""
        try:
            self.complete_label.pack_forget()
            folders = [
                FILES_FOLDER,
                FILES_REJECTED,
                OUTPUTS_FOLDER,
                os.path.join(PATH, "ficheiros_extraidos")]  # logs

            for folder in folders:
                files = os.listdir(folder)
                for file in files:
                    try:
                        os.remove(os.path.join(folder, file))
                    except Exception as error:
                        print(error)

            self.loading_label.pack(pady=5)
            self.win.update()

            print(self.selected_dates)

            launch_extraction(
                True,
                PATH,
                NETWORKS_LISTS,
                NETWORKS_FUNCTIONS,
                EMAIL,
                PASSWORD,
                LAST_EMAIL,
                EMAIL_FOLDER,
                EMAIL_ADDRESS,
                FILES_FOLDER,
                FILES_REJECTED,
                CODES_ID,
                CLIENTS_ID,
                self.selected_dates,
                LOGGER)
        except Exception as error:
            messagebox.showerror("Error", str(error))

        self.loading_label.pack_forget()
        self.complete_label.pack(pady=21)
        self.win.update()


app = App()
app.win.mainloop()
