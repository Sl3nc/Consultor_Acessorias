from pathlib import Path
import os
import sys
import traceback
from unidecode import unidecode
from time import sleep

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
from selenium.webdriver.common.keys import Keys
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

import json
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / 'src' / 'env' / '.env')

def resource_path(relative_path):
    base_path = getattr(
        sys,
        '_MEIPASS',
        os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class Matriz:
    def __init__(self) -> None:
        self.tipos_validos = 'lsx'
        self.caminho = None
        self.COL_TEXT = 12
        pass

    def inserir(self) -> str | None:
        try:
            caminho = askopenfilename()
            if caminho == '':
                return None
            self.caminho = self.__validar_entrada(caminho)
            return self.caminho[self.caminho.rfind('/') +1:]

        except PermissionError:
            messagebox.showerror(title='Aviso', message= 'O arquivo selecionado apresenta-se em aberto em outra janela, favor fecha-la')
            return None

        except FileExistsError:
            messagebox.showerror(title='Aviso', message= 'O arquivo selecionado já apresenta uma versão sem acento, favor usar tal versão ou apagar uma delas')
            return None

        except Exception as error:
            messagebox.showerror(title='Aviso', message= error)
            return None

    def __validar_entrada(self, caminho: str) -> str:
        if caminho[len(caminho) -3 :] != self.tipos_validos:
            ultima_barra = caminho.rfind('/')
            raise Exception(
                f'Formato inválido do arquivo: {caminho[ultima_barra+1:]}'
            )
        
        caminho_uni = unidecode(caminho)
        if caminho != caminho_uni:
            caminho = self.__renomear(caminho_uni)

        return caminho

    def __renomear(self, caminho, caminho_uni) -> str:
        os.renames(caminho, caminho_uni)
        return caminho
    
    def envio_invalido(self) -> bool:
        return True if self.caminho == None else False

    def ler(self) -> list:
        return pd.read_excel(self.caminho, usecols='A', header= None)\
            .iloc[:,0]

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
    CHROME_DRIVER_PATH = resource_path('src\\driver\\chromedriver.exe')
    URL_MAIN = 'https://app.acessorias.com/sysmain.php'
    URL_ENTREGAS = 'https://app.acessorias.com/sysmain.php?m=3'
    URL_EMPRESA = 'https://app.acessorias.com/sysmain.php?m=4'

    INPUT_EMAIL = 'mailAC'
    INPUT_PASSWORD= 'passAC'
    BTN_ENTRAR = '#site-corpo > section.secao.secao-login > div > form > div.botoes > button'

    BTN_PESQUISA = 'searchEmp'
    BTN_FILTRAR = 'btFilter'
    TABELA_ENTREGAS = 'divRelEntregas'

    def __init__(self, obrigacoes) -> None:
        self.obrigacoes_desejadas = [i for i in obrigacoes]

        self.class_status_entrega = "col-sm-3.col-xs-12.no-padding"
        self.class_nome_entrega = 'neg.brown'

        self.browser = self.make_chrome_browser(hide=False)
        self.browser.get(self.URL_MAIN)
        pass

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
    
    def login(self, usuario: str, senha: str):
        self.browser.find_element(By.NAME, self.INPUT_EMAIL).send_keys(usuario)
        self.browser.find_element(By.NAME, self.INPUT_PASSWORD).send_keys(senha)

        self.browser.find_element(By.CSS_SELECTOR, self.BTN_ENTRAR).click()


    def pesquisar_entrega(self, num_empresa):
        if self.browser.current_url != self.URL_ENTREGAS:
            self.browser.get(self.URL_ENTREGAS)

        self.browser.find_element(By.ID, self.BTN_PESQUISA).clear()

        self.browser.find_element(By.ID, self.BTN_PESQUISA)\
            .send_keys(str(num_empresa))
        
        sleep(3)

        self.browser.find_element(By.ID, self.BTN_FILTRAR).click()

        sleep(3)

        return self.extrair_dados(
            self.browser.find_element(By.ID, self.TABELA_ENTREGAS)
        )

    def extrair_dados(self, tabela: WebElement):
        result = {}

        nome_competencia = [
            x.text for x in tabela.find_elements(By.CLASS_NAME, self.class_nome_entrega)
        ]
        # print(f'{nome_competencia}\n\n')
        status = [
            x.text for x in tabela.find_elements(By.CLASS_NAME, self.class_status_entrega)
        ]
        # print(f'{status}\n\n')
        count = 0
        for i in range(0, len(nome_competencia), 2):
            juncao = f'{nome_competencia[i]} {nome_competencia[i + 1]}'
            result[juncao] = status[count]
            count = count + 1
        
        # print(result)
        return result

    def pesquisar_empresa(self, num_empresa):
        ...

    def close(self):
        self.browser.close()

class Wellington(QObject):
    valor = Signal(str)
    progress = Signal(int)
    fim = Signal()

    def __init__(self, info_matriz: list[str], competencia: str) -> None:
        super().__init__()
        self.info_matriz = info_matriz
        self.competencia = competencia

        self.infos_empresa = {
            'Nome': list(),
            'CNPJ': list()
        }

        self.obrigacao = {
            'FGTS': list(),
            'PROLABORE': list(),
            'Resumo de tributos': list(),
            'Domestico': list(),
        }

        self.credenciais = [
            os.getenv("LOGIN",""),
            os.getenv("SENHA",""),
        ]
        pass

    #TODO TRABALHAR
    def trabalhar(self) -> pd.DataFrame:
        try:
            acessorias = Acessorias(self.obrigacao.keys())
            acessorias.login(self.credenciais[0], self.credenciais[1])
            sleep(5)

            # for method, dict_values in {
            # acessorias.pesquisar_entrega: self.obrigacao.values(), 
            # acessorias.pesquisar_empresa: self.infos_empresa.values()
            # }.items():
            #     for num in self.info_matriz:
            #         resp = method(num)
            #         for index, listas in enumerate(dict_values):
            #             listas.append(resp[index])

            for num in self.info_matriz:
                resp = acessorias.pesquisar_entrega(num)
                for index, listas in enumerate(self.obrigacao.values()):
                    listas.append(resp[index])

            for num in self.info_matriz:
                resp = acessorias.pesquisar_empresa(num)
                for index, listas in enumerate(self.infos_empresa.values()):
                    listas.append(resp[index])

            return pd.DataFrame(
                self.infos_empresa,
                self.obrigacao
            )
        except Exception:
            traceback.print_exc()
            sleep(20)
            acessorias.close()

    def filtro_obrigacoes(self, lista_obriacoes):
        ...

class MainWindow(QMainWindow, Ui_MainWindow):
    MAX_PROGRESS = 100

    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)

        self.matriz = Matriz()

        self.setWindowIcon((QIcon(
            resource_path('src\\imgs\\acessorias_icon.ico'))))
        self.logo.setPixmap(QPixmap(
            resource_path('src\\imgs\\acessorias_hori.png')))
        icon = QIcon()
        icon.addFile(resource_path("src\\imgs\\upload-icon.png"), QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_upload.setIcon(icon)
        self.movie = QMovie(resource_path("src\\imgs\\load.gif"))
        self.load_movie.setMovie(self.movie)

        self.pushButton_upload.clicked.connect(self.inserir_arquivo)
        self.pushButton_enviar.clicked.connect(self.hard_work)

    def inserir_arquivo(self):
        resp = self.matriz.inserir()

        if resp != None:
            self.pushButton_upload.setText(resp)
            self.pushButton_upload.setIcon(QPixmap(''))

    #TODO HARD_WORK
    def hard_work(self):
        try:
            if self.matriz.envio_invalido():
                raise Exception('Favor anexar seu relatório de processos')
            
            nums_empresas = self.matriz.ler()
            self.max_progress_bar = self.MAX_PROGRESS / len(nums_empresas)

            self.exec_load(True)
            self.wellington = Wellington(
                nums_empresas, self.dateEdit_competencia.text()
            )
            self._thread = QThread()

            self.wellington.moveToThread(self._thread)
            self._thread.started.connect(self.wellington.trabalhar)
            self.wellington.fim.connect(self._thread.quit)
            self.wellington.fim.connect(self._thread.deleteLater)
            self.wellington.fim.connect(self.encerramento)
            self._thread.finished.connect(self.wellington.deleteLater)
            self.wellington.progress.connect(self.to_progress)

            self._thread.start()  

        except ParserError:
            self.exec_load(False)
            messagebox.showerror(title='Aviso', message= 'Erro ao ler o arquivo, certifique-se de ter inserido o arquivo correto')
        except Exception as err:
            self.exec_load(False)
            traceback.print_exc()
            messagebox.showerror('Aviso', err)

    def encerramento(self, result):
        #TODO encerramento
        
            
        self.matriz.alterar(result)
        self.matriz.abrir()

        self.exec_load(False)
        self.pushButton.setDisabled(False)

    def to_progress(self, valor):
        self.progressBar.setValue(self.max_progress_bar * valor)

    def exec_load(self, action: bool):
        if action == True:
            self.movie.start()
            self.stackedWidget.setCurrentIndex(1)
        else:
            self.movie.stop()
            self.stackedWidget.setCurrentIndex(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()