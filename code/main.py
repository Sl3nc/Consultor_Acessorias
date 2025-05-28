from pathlib import Path
import os
import sys
import traceback
from unidecode import unidecode
from time import sleep
from datetime import datetime, date

import pandas as pd
from pandas.errors import ParserError
from openpyxl import Workbook, load_workbook
from openpyxl.cell.text import InlineFont
from openpyxl.cell.rich_text import TextBlock, CellRichText
from openpyxl.utils import get_column_letter

from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PySide6.QtWidgets import (
    QMainWindow, QApplication, QWidget, QLabel, QVBoxLayout,QPushButton, QLineEdit
)
from PySide6.QtGui import QPixmap, QIcon, QMovie
from PySide6.QtCore import QThread, QObject, Signal, QSize, QDate
from src.window_acessorias import Ui_MainWindow

from tkinter.messagebox import askyesno, showerror, showinfo
from tkinter.filedialog import askopenfilename, asksaveasfilename
from wellington import Wellington
from matriz import Matriz

import json
from dotenv import load_dotenv

from locale import setlocale, LC_ALL

setlocale(LC_ALL, 'pt_BR.UTF-8')

load_dotenv(Path(__file__).parent / 'src' / 'env' / '.env')

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Classe principal da interface gráfica, responsável por gerenciar as interações do usuário, progresso e execução das tarefas.
    """
    MAX_PROGRESS = 100

    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)
        self.matriz = Matriz()

        self.setWindowIcon(QIcon(
            (Path(__file__).parent /'src'/'imgs'/'acessorias_icon.ico').__str__()))
        self.logo.setPixmap(QPixmap(
            (Path(__file__).parent /'src'/'imgs'/'acessorias_hori.png').__str__()))
        icon = QIcon()
        icon.addFile(
            (Path(__file__).parent /'src'/'imgs'/'upload-icon.png').__str__(),QSize(),
            QIcon.Mode.Normal,
            QIcon.State.Off
        )
        self.pushButton_upload.setIcon(icon)
        self.movie = QMovie(
            (Path(__file__).parent /'src'/'imgs'/'load.gif').__str__()
        )
        self.load_movie.setMovie(self.movie)
        data_atual = datetime.now()
        self.dateEdit_competencia.setDate(
            QDate(data_atual.year, data_atual.month - 1, data_atual.day)
        )

        self.pushButton_upload.clicked.connect(self.inserir_arquivo)
        self.pushButton_enviar.clicked.connect(self.ler_matriz)

    def inserir_arquivo(self):
        """
        Ação do botão para inserir o arquivo da matriz.
        """
        resp = self.matriz.inserir()

        if resp != None:
            self.pushButton_upload.setText(resp)
            self.pushButton_upload.setIcon(QPixmap(''))

    def ler_matriz(self):
        """
        Inicia a leitura da matriz de empresas em uma thread separada.
        """
        if self.matriz.envio_invalido():
            raise Exception('Favor anexar seu relatório de processos')
         
        self.load_title.setText('Carregando empresas da matriz...')
        self.progressBar.hide()
        self.exec_load(True)

        self._thread = QThread()

        self.matriz.moveToThread(self._thread)
        self._thread.started.connect(self.matriz.ler)
        self.matriz.fim.connect(self._thread.quit)
        self.matriz.fim.connect(self._thread.deleteLater)
        self.matriz.fim.connect(self.hard_work)
        self._thread.finished.connect(self.matriz.deleteLater)
        self.matriz.qnt_empresas.connect(self.set_progress)

        self._thread.start()  

    #TODO HARD_WORK
    def hard_work(self, itens_matriz: dict):
        """
        Inicia o processamento das empresas e obrigações em uma thread separada.
        """
        try:
            self.load_title.setText('Pesquisando empresas...')
            self.progressBar.show()

            # for key, value in itens_matriz.items():
            #     print(f'{key} - {value}')

            self.wellington = Wellington(
                itens_matriz, self.dateEdit_competencia.text()
            )
            self._thread = QThread()

            self.wellington.moveToThread(self._thread)
            self._thread.started.connect(self.wellington.trabalhar)
            self.wellington.fim.connect(self._thread.quit)
            self.wellington.fim.connect(self._thread.deleteLater)
            self.wellington.fim.connect(self.encerramento)
            self._thread.finished.connect(self.wellington.deleteLater)
            self.wellington.progress.connect(self.add_progress)

            self._thread.start()  

        except ParserError:
            self.exec_load(False)
            showerror(title='Aviso', message= 'Erro ao ler o arquivo, certifique-se de ter inserido o arquivo correto')
        except Exception as err:
            self.exec_load(False)
            traceback.print_exc()
            showerror('Aviso', err)

    def encerramento(self):
        """
        Finaliza o processamento e exibe mensagem de sucesso.
        """
        self.exec_load(False)
        self.statusbar.showMessage(
            f'Execução com êxito às {datetime.now().strftime('%H:%M:%S')}', 10)
        
    def set_progress(self, valor):
        """
        Define o coeficiente de progresso para a barra de progresso.
        """
        self.coeficiente_progresso = self.MAX_PROGRESS / valor

    def add_progress(self, valor):
        """
        Atualiza o valor da barra de progresso.
        """
        self.progressBar.setValue(self.coeficiente_progresso * valor)

    def exec_load(self, action: bool):
        """
        Controla a exibição da animação de carregamento.
        """
        if action == True:
            self.movie.start()
            self.stackedWidget.setCurrentIndex(1)
        else:
            self.movie.stop()
            self.stackedWidget.setCurrentIndex(0)

if __name__ == '__main__':
    """
    Ponto de entrada da aplicação. Inicializa a interface gráfica.
    """
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()