# Consultor Acessorias

Este projeto automatiza a consulta, extração e geração de relatórios de obrigações de empresas a partir do sistema web [Acessorias.com](https://app.acessorias.com/), utilizando interface gráfica em PySide6 e automação web com Selenium.

## Funcionalidades

- **Importação de Matriz**: Permite ao usuário importar uma planilha Excel (.xlsx) contendo a matriz de empresas a serem consultadas.
- **Consulta Automatizada**: Realiza login automático no sistema Acessorias.com e pesquisa as obrigações de cada empresa, conforme categorias definidas.
- **Extração de Dados**: Coleta informações como nome da empresa, CNPJ e status das obrigações (ex: folha de pagamento, DARF, FGTS, etc).
- **Geração de Relatório**: Gera um relatório consolidado em Excel, pronto para análise ou envio.
- **Interface Gráfica**: Interface amigável para seleção de arquivos, acompanhamento do progresso e visualização de mensagens.

## Estrutura do Projeto

- `code/index.py`: Código principal da aplicação, contendo a lógica de interface, automação e geração de relatórios.
- `src/window_acessorias.py`: Arquivo gerado pelo Qt Designer, define a interface gráfica.
- `src/driver/chromedriver.exe`: Driver do Chrome necessário para automação Selenium.
- `src/imgs/`: Imagens utilizadas na interface.
- `src/env/.env`: Arquivo de variáveis de ambiente (login e senha).

## Requisitos

- Python 3.9+
- Google Chrome instalado
- Dependências Python:
  - pandas
  - openpyxl
  - selenium
  - unidecode
  - python-dotenv
  - PySide6

Instale as dependências com:
```bash
pip install -r requirements.txt
```

## Configuração

1. **Variáveis de Ambiente**: Crie um arquivo `.env` em `src/env/` com as seguintes variáveis:
   ```
   LOGIN=seu_usuario
   SENHA=sua_senha
   ```

2. **Driver do Chrome**: Certifique-se de que o `chromedriver.exe` é compatível com a versão do seu Google Chrome.

## Como Usar

1. Execute o arquivo principal:
   ```bash
   python code/index.py
   ```
2. Na interface, clique em "Upload" para selecionar a planilha da matriz de empresas.
3. Defina a competência desejada.
4. Clique em "Enviar" para iniciar o processamento.
5. Aguarde o progresso e, ao final, o relatório será salvo e aberto automaticamente.

## Observações

- O sistema foi desenvolvido para uso interno, automatizando tarefas repetitivas de consulta e consolidação de obrigações fiscais/contábeis.
- O uso do Selenium pode ser afetado por mudanças na interface do site Acessorias.com.

## Licença

Este projeto é de uso restrito e não possui licença aberta.

