from PySide6.QtCore import Signal, QObject
from acessorias import Acessorias
from obligation import Obrigacao
from traceback import print_exc
from resume import Relatorio
from time import sleep
from os import getenv
import pandas as pd

class Wellington(QObject):
    """
    Classe que coordena o processamento das empresas, realizando a extração dos dados de obrigações e geração do relatório final.
    """
    progress = Signal(int)
    fim = Signal()

    def __init__(self, itens_matriz: dict[str,list[int]], competencia: str) -> None:
        super().__init__()
        self.info_matriz = itens_matriz
        self.competencia = competencia

        self.obrigacoes = {
            'DOMESTICO': Obrigacao(
                ['Recibo de Pagamento de Salário','GUIA E-SOCIAL - EMPREGADOR','FOLHA DE PONTO']
            ),
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
        }

        self.credenciais = [
            getenv("LOGIN",""),
            getenv("SENHA",""),
        ]

        pass

    def trabalhar(self) -> pd.DataFrame:
        """
        Executa o fluxo principal: login, pesquisa de obrigações, coleta de dados e geração do relatório.
        """
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

                            count = count + 1
                            self.progress.emit(count)
                        break

            acessorias.close()
            Relatorio().alterar(self.obrigacoes)
            self.fim.emit()
        except Exception:
            print_exc()
            acessorias.close()