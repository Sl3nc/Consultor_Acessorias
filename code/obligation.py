import pandas as pd

class Obrigacao:
    """
    Classe responsável por armazenar e manipular as obrigações de uma empresa,
    bem como suas informações básicas (nome e CNPJ).
    """
    def __init__(self, interesses: list) -> None:
        """
        Inicializa a Obrigacao com os interesses (tipos de obrigações) a serem acompanhados.
        """
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
        """
        Adiciona o status das obrigações conforme os dados extraídos do sistema.
        """
        for interesse, lista in self.interesses.items():
            lista.append('Pendente')
            for key, situacao in dict_obriacoes.items():
                # print(f'\nkey - {key}')
                # print(f'interesse - {interesse}\n')
                if interesse in key:
                    if 'Ent.' in situacao:
                        lista.pop()
                        lista.append(f'Enviado: {situacao[25:33]}')
                    break

    def add_empresa(self, infos_emp: list[str]):
        """
        Adiciona informações da empresa (nome e CNPJ) à Obrigacao.
        """
        for index, listas in enumerate(self.infos_empresa.values()):
            listas.append(infos_emp[index])

    def result(self):
        """
        Retorna um DataFrame pandas com as informações da empresa e obrigações.
        """
        return pd.DataFrame(self.infos_empresa | self.interesses)