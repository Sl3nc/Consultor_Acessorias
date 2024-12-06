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

import json
from dotenv import load_dotenv

from locale import setlocale, LC_ALL

setlocale(LC_ALL, 'pt_BR.UTF-8')

load_dotenv(Path(__file__).parent / 'src' / 'env' / '.env')

def resource_path(relative_path):
    base_path = getattr(
        sys,
        '_MEIPASS',
        os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class Obrigacao:
    def __init__(self, interesses: list) -> None:
        self.interesses = {key: list() for key in interesses}

        self.infos_empresa = {
            'Nome': list(),
            'CNPJ': list()
        }

        # self.obrigacao = {
        #     'GUIA FGTS DIGITAL': list(),
        #     'Pro labore': list(),
        #     'RESUMO FOLHA DE PAGAMENTO': list(),
        #     'BOLETO - HONORÁRIO CONTÁBIL': list(),
        # }
        pass

    def add_dados(self, dict_obriacoes: dict[str,str]):
        for interesse, lista in self.interesses.items():
            lista.append('Pendente')
            for key, situacao in dict_obriacoes.items():
                # print(f'\nkey - {key}')
                # print(f'interesse - {interesse}\n')
                if interesse in key:
                    if 'Ent.' in situacao:
                        lista.pop()
                        lista.append(f'Enviado: {situacao[situacao.find('/',8) - 2:8]}')
                    break

    def add_empresa(self, infos_emp: list[str]):
        for index, listas in enumerate(self.infos_empresa.values()):
            listas.append(infos_emp[index])

    def result(self):
        return pd.DataFrame(self.infos_empresa | self.interesses)

class Matriz(QObject):
    fim = Signal(dict)
    qnt_empresas = Signal(int)

    def __init__(self) -> None:
        super().__init__()
        self.tipos_validos = 'lsx'
        self.caminho = None
        self.planilha_excecoes = ['PORCENTAGEM', 'PERCENTUAIS']
        pass

    def inserir(self) -> str | None:
        try:
            caminho = askopenfilename()
            if caminho == '':
                return None
            self.caminho = self.__validar_entrada(caminho)
            return self.caminho[self.caminho.rfind('/') +1:]

        except PermissionError:
            showerror(title='Aviso', message= 'O arquivo selecionado apresenta-se em aberto em outra janela, favor fecha-la')
            return None

        except FileExistsError:
            showerror(title='Aviso', message= 'O arquivo selecionado já apresenta uma versão sem acento, favor usar tal versão ou apagar uma delas')
            return None

        except Exception as error:
            showerror(title='Aviso', message= error)
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

    def ler(self) -> dict[str,list[str]]:
        result = {}
        nomes_planilha = load_workbook(self.caminho).sheetnames
        for i in self.planilha_excecoes:
            if i in nomes_planilha:
                nomes_planilha.remove(i)
        self.qnt_empresas.emit(len(nomes_planilha))

        for nome in nomes_planilha:
            result[nome] = [int(i) for i in pd.read_excel(self.caminho, usecols='A', header= None, sheet_name= nome).dropna().iloc[:, 0]]

        self.fim.emit(result)

class Relatorio:
    TITULO = 'Relatório'

    def __init__(self) -> None:
        self.linha_cabecalho = 2
        self.linha_conteudo = 3
        self.espacos_tabela = [50,20,20,10,30,30]
        pass

    def nomear(self) -> str:
        nome_arq = asksaveasfilename(title='Favor nomear o arquivo que será salvo', filetypes=((".xlsx","*.xlsx"),))

        if nome_arq == '':
            if askyesno(title='Aviso', message= 'Deseja cancelar esta operação?') == True:
                raise Exception ('Operação cancelada!')
            else:
                return self.nomear()
            
        return nome_arq  + '.xlsx' 
    
    def alterar(self, data: dict[str, Obrigacao]) -> None:
        wb = Workbook()
        del wb['Sheet']
        for key, obrigacao in data.items():
            df = obrigacao.result()
            if df.empty == False:
                ws = wb.create_sheet(key)
                self.width_ws(ws)

                self.fill_cabecalho(df, ws)
                self.fill_conteudo(df, ws)

        nome_arq = self.nomear()
        wb.save(nome_arq)
        
        showinfo(title='Aviso', message='Abrindo o arquivo gerado!')
        os.startfile(nome_arq)

    def fill_conteudo(self, conteudo: pd.DataFrame, ws):
        for index_linha, row in conteudo.iterrows():
            for index_coluna, valor in enumerate(row, 1):
                ws.cell(index_linha + self.linha_conteudo, index_coluna).value = valor

    def fill_cabecalho(self, conteudo: pd.DataFrame, ws):
        for index_coluna, column in enumerate(conteudo.columns, 1):
            ws.cell(self.linha_cabecalho, index_coluna).value = CellRichText(
                TextBlock(InlineFont(b=True), column)
            )

    def width_ws(self, ws):
        for index, valor in enumerate(self.espacos_tabela, 1):
            ws.column_dimensions[get_column_letter(index)].width = valor

class Acessorias:
    CHROME_DRIVER_PATH = resource_path('src\\driver\\chromedriver.exe')
    URL_MAIN = 'https://app.acessorias.com/sysmain.php'
    URL_ENTREGAS = 'https://app.acessorias.com/sysmain.php?m=3'
    URL_EMPRESA = 'https://app.acessorias.com/sysmain.php?m=4'

    INPUT_EMAIL = 'mailAC'
    INPUT_PASSWORD= 'passAC'
    BTN_ENTRAR = '#site-corpo > section.secao.secao-login > div > form > div.botoes > button'

    BTN_PESQUISA_ENTREGAS = 'searchEmp'
    BTN_PESQUISA_EMP = 'searchString'
    BTN_FILTRAR = 'btFilter'
    TABELA_ENTREGAS = 'divRelEntregas'

    COMPE_DE = 'EntCompDe'
    COMPE_PARA = 'EntCompAte'
    
    POSIC_NOME_EMP = '#divEmpZ_{0} > div.col-sm-5.col-xs-12.no-padding.aImage > span'

    POSIC_CNPJ_EMP = '#divEmpZ_{0} > div.col-sm-7.col-xs-12.no-padding.aImage > div:nth-child(1)'

    def __init__(self) -> None:
        self.class_status_entrega = "col-sm-3.col-xs-12.no-padding"
        self.class_nome_entrega = 'neg.brown'

        self.browser = self.make_chrome_browser(hide=False)
        self.browser.get(self.URL_MAIN)
        pass

    def make_chrome_browser(self,*options: str, hide: bool) -> webdriver.Chrome:
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

    def pesquisar_entrega(self, num_empresa: str):
        if self.browser.current_url != self.URL_ENTREGAS:
            self.browser.get(self.URL_ENTREGAS)

        for input in [self.BTN_PESQUISA_ENTREGAS]:
            self.browser.find_element(By.ID, input).clear()
            self.browser.find_element(By.ID, input)\
            .send_keys(num_empresa)

        self.browser.find_element(By.ID, self.BTN_FILTRAR).click()
        sleep(3)

        return self.extrair_dados(
            self.browser.find_element(By.ID, self.TABELA_ENTREGAS)
        )

    def set_competencia(self, competencia: str):
        self.browser.get(self.URL_ENTREGAS)

        for input in [self.COMPE_DE, self.COMPE_PARA]:
            self.browser.find_element(By.ID, input).clear()
            self.browser.find_element(By.ID, input)\
            .send_keys(competencia)

    def extrair_dados(self, tabela: WebElement):
        result = {}

        nome_competencia = [
            x.text for x in tabela.find_elements(By.CLASS_NAME, self.class_nome_entrega)
        ]
        status = [
            x.text for x in tabela.find_elements(By.CLASS_NAME, self.class_status_entrega)
        ]
        count = 0
        for i in range(0, len(nome_competencia), 2):
            juncao = f'{nome_competencia[i]} {nome_competencia[i + 1]}'
            result[juncao] = status[count]
            count = count + 1
        
        return result

    def pesquisar_empresa(self, num_empresa: str):
        try:
            if self.browser.current_url != self.URL_EMPRESA:
                self.browser.get(self.URL_EMPRESA)

            self.browser.find_element(By.ID, self.BTN_PESQUISA_EMP).clear()

            self.browser.find_element(By.ID, self.BTN_PESQUISA_EMP)\
                .send_keys(num_empresa)

            self.browser.find_element(By.ID, self.BTN_FILTRAR).click()
            sleep(3)

            nome_emp = self.browser.find_element(By.CSS_SELECTOR, self.POSIC_NOME_EMP.format(num_empresa)).text

            cnpj_emp = self.browser.find_element(By.CSS_SELECTOR, self.POSIC_CNPJ_EMP.format(num_empresa)).text

            return [
                nome_emp[:nome_emp.rfind('[') - 1],
                cnpj_emp[:18]
            ]
        except:
            return [
                'Empresa não encontrada',
                'Num. domínio: '+ num_empresa
            ]


    def close(self):
        self.browser.close()

#TODO WELLINGTON
class Wellington(QObject):
    progress = Signal(int)
    fim = Signal()

    def __init__(self, itens_matriz: dict[str,list[str]], competencia: str) -> None:
        super().__init__()
        self.info_matriz = itens_matriz
        self.competencia = competencia

        self.obrigacoes = {
            'SO PRO LABORE': Obrigacao(
                ['RESUMO FOLHA DE PAGAMENTO','DARF DCTFWEB','RECIBO DCTFWEB','ESOCIAL']
            ),
            'FOLHA SIMPLES': Obrigacao(
                ['RESUMO FOLHA DE PAGAMENTO','DARF','RECIBO DCTFWEB','ESOCIAL','GUIA FGTS DIGITAL','RELATORIO FGTS DIGITAL']
            ),
            'FOLHA COM MOVIMENTO': Obrigacao(
                ['RESUMO FOLHA DE PAGAMENTO','DARF','RECIBO DCTFWEB','ESOCIAL','GUIA FGTS DIGITAL','RELATORIO FGTS DIGITAL']
            ),
            'SEM MOVIMENTO': Obrigacao(['DARF DCTFWEB','RECIBO DCTFWEB','ESOCIAL']),
            # 'SO DCTF': Obrigacao([''])
        }

        self.credenciais = [
            os.getenv("LOGIN",""),
            os.getenv("SENHA",""),
        ]

        pass

    #TODO TRABALHAR
    def trabalhar(self) -> pd.DataFrame:
        try:
            acessorias = Acessorias()
            acessorias.login(self.credenciais[0], self.credenciais[1])
            sleep(5)

            #Implementar procura pela obrigação e adição de dados ao mesmo
            count = 0
            acessorias.set_competencia(self.competencia)
            for categoria_matriz, list_num in self.info_matriz.items():
                for categoria_obri, obrigacao in self.obrigacoes.items():
                    if categoria_matriz == categoria_obri:
                        for num in list_num:
                            obrigacao.add_dados(acessorias.pesquisar_entrega(str(num)))
                            obrigacao.add_empresa(acessorias.pesquisar_empresa(str(num)))
                        break
                count = count + 1
                self.progress.emit(count)

            Relatorio().alterar(self.obrigacoes)
            self.fim.emit()
        except Exception:
            traceback.print_exc()
            acessorias.close()
            
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
        data_atual = datetime.now()
        self.dateEdit_competencia.setDate(
            QDate(data_atual.year, data_atual.month - 1, data_atual.day)
        )

        self.pushButton_upload.clicked.connect(self.inserir_arquivo)
        self.pushButton_enviar.clicked.connect(self.ler_matriz)

    def inserir_arquivo(self):
        resp = self.matriz.inserir()

        if resp != None:
            self.pushButton_upload.setText(resp)
            self.pushButton_upload.setIcon(QPixmap(''))

    def ler_matriz(self):
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
        self.exec_load(False)
        self.statusbar.showMessage(
            f'Execução com êxito às {datetime.now().strftime('%H:%M:%S')}', 10)
        
    def set_progress(self, valor):
        self.coeficiente_progresso = self.MAX_PROGRESS / valor

    def add_progress(self, valor):
        self.progressBar.setValue(self.coeficiente_progresso * valor)

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