from pathlib import Path
import os
import sys
import traceback
from unidecode import unidecode

import pandas as pd
from pandas.errors import ParserError
from openpyxl import load_workbook
from openpyxl.cell.text import InlineFont
from openpyxl.cell.rich_text import TextBlock, CellRichText

from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PySide6.QtWidgets import (
    QMainWindow, QApplication, QWidget, QLabel, QVBoxLayout,QPushButton, QLineEdit
)
from PySide6.QtGui import QPixmap, QIcon, QMovie
from PySide6.QtCore import QThread, QObject, Signal, QSize
from src.window_acessorias import Ui_MainWindow

from tkinter import messagebox
from tkinter.filedialog import askopenfilename

def resource_path(relative_path):
    base_path = getattr(
        sys,
        '_MEIPASS',
        os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class Matriz:
    def __init__(self) -> None:
        self.tipos_validos = 'lsx'
        self.caminho = ''
        self.COL_TEXT = 12
        pass

    def inserir(self, button: QPushButton) -> None:
        try:
            self.caminho = askopenfilename()
            if self.caminho == '':
                return
            self.__validar_entrada()
            with open(self.caminho, 'r+'):
                ...
            button.setText(self.caminho[self.caminho.rfind('/') +1:])
            button.setIcon(QPixmap(''))

        except PermissionError:
            messagebox.showerror(title='Aviso', message= 'O arquivo selecionado apresenta-se em aberto em outra janela, favor fecha-la')
        except FileExistsError:
            messagebox.showerror(title='Aviso', message= 'O arquivo selecionado já apresenta uma versão sem acento, favor usar tal versão ou apagar uma delas')
        except Exception as error:
            messagebox.showerror(title='Aviso', message= error)

    def __validar_entrada(self) -> str:
        if self.caminho == '':
            return None
        self.__tipo()
        caminho_uni = unidecode(self.caminho)
        if self.caminho != caminho_uni:
            self.caminho = self.__renomear(caminho_uni)

    def __tipo(self) -> bool:
        if self.caminho[len(self.caminho) -3 :] != self.tipos_validos:
            ultima_barra = self.caminho.rfind('/')
            raise Exception(
                f'Formato inválido do arquivo: {self.caminho[ultima_barra+1:]}')
        return True

    def __renomear(self, caminho) -> str:
        os.renames(self.caminho, caminho)
        return caminho
    
    def envio_invalido(self) -> bool:
        return True if len(self.caminho) == 0 else False

    def ler(self) -> list:
        return pd.read_excel(self.caminho, usecols='E').dropna().values.tolist()

    def alterar(self, conteudo) -> None:
        #TODO Alterar
        wb = load_workbook(self.caminho)
        ws = wb[self.NOME_SHEET]
        for index, lista_movimentos in enumerate(conteudo.values(), 2):
            #print(f'{index} - {lista_movimentos}')
            if lista_movimentos == ['']:
                continue

            if ws.cell(index, self.COL_TEXT).value == None:
                ws.cell(index, self.COL_TEXT, '')

            s = ' **'.join(str(movimento) for movimento in lista_movimentos\
                if movimento[:11] not in str(ws.cell(index, self.COL_TEXT).value))

            ws.cell(index, self.COL_TEXT).value = CellRichText(
                [TextBlock(InlineFont(b=True), s), ws.cell(index, self.COL_TEXT).value]
            )

        wb.save(self.caminho)
          
    def abrir(self) -> None:
        messagebox.showinfo(title='Aviso', message='Abrindo o arquivo gerado!')
        os.startfile(self.caminho)

class Acessorias:
    CHROME_DRIVER_PATH = resource_path('src\\drivers\\chromedriver.exe')

    def make_chrome_browser(self,*options: str, hide = True) -> webdriver.Chrome:
        chrome_options = webdriver.ChromeOptions()

        if options is not None:
            for option in options:
                chrome_options.add_argument(option)

        chrome_service = Service(
            executable_path=str(self.CHROME_DRIVER_PATH),
        )

        browser = webdriver.Chrome(
            service=chrome_service,
            options=chrome_options
        )

        if hide == True:
            browser.set_window_position(-10000,0)

        return browser




class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)

        self.setWindowIcon((QIcon(
            resource_path('src\\imgs\\acessorias_icon.ico'))))
        self.logo.setPixmap(QPixmap(
            resource_path('src\\imgs\\acessorias_hori.png')))
        icon = QIcon()
        icon.addFile(resource_path("src\\imgs\\upload-icon.png"), QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_upload.setIcon(icon)
        self.movie = QMovie(resource_path("src\\imgs\\load.gif"))
        self.load_movie.setMovie(self.movie)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()