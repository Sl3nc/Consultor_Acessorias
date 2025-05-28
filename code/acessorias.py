from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver

from pathlib import Path
from time import sleep

class Acessorias:
    """
    Classe responsável por interagir com o sistema web Acessorias.com via Selenium,
    realizando login, pesquisa de entregas e extração de dados das empresas.
    """
    CHROME_DRIVER_PATH = Path(__file__).parent/'src'/'driver'/'chromedriver.exe'
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

        self.browser = self.make_chrome_browser(hide=True)
        self.browser.get(self.URL_MAIN)
        pass

    def make_chrome_browser(self,*options: str, hide: bool) -> webdriver.Chrome:
        """
        Inicializa o navegador Chrome com as opções fornecidas.
        """
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
        """
        Realiza login no sistema Acessorias.com.
        """
        self.browser.find_element(By.NAME, self.INPUT_EMAIL).send_keys(usuario)
        self.browser.find_element(By.NAME, self.INPUT_PASSWORD).send_keys(senha)

        self.browser.find_element(By.CSS_SELECTOR, self.BTN_ENTRAR).click()

    def pesquisar_entrega(self, num_empresa: str):
        """
        Pesquisa as entregas de uma empresa pelo número de domínio.
        """
        if self.browser.current_url != self.URL_ENTREGAS:
            self.browser.get(self.URL_ENTREGAS)

        for input in [self.BTN_PESQUISA_ENTREGAS]:
            self.browser.find_element(By.ID, input).clear()
            self.browser.find_element(By.ID, input)\
            .send_keys(str(num_empresa))

        self.browser.find_element(By.ID, self.BTN_FILTRAR).click()
        sleep(3)

        return self.extrair_dados(
            self.browser.find_element(By.ID, self.TABELA_ENTREGAS)
        )

    def set_competencia(self, competencia: str):
        """
        Define a competência (período) para filtrar as entregas.
        """
        self.browser.get(self.URL_ENTREGAS)

        for input in [self.COMPE_DE, self.COMPE_PARA]:
            self.browser.find_element(By.ID, input).clear()
            self.browser.find_element(By.ID, input)\
            .send_keys(competencia)

    def extrair_dados(self, tabela: WebElement):
        """
        Extrai os dados de entregas da tabela HTML.
        """
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
        """
        Pesquisa e retorna informações da empresa (nome e CNPJ).
        """
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
                'Num. domínio: '+ str(num_empresa)
            ]


    def close(self):
        """
        Fecha o navegador.
        """
        self.browser.close()