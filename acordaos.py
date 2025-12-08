from functions.save import juntar_dados_de_cada_pagina
from functions.run import run

from playwright.sync_api import sync_playwright
from rich.traceback import install

DEBUG = False
DEBUG = True # toggle
TIMEOUT = 90000
URL = 'https://processo.stj.jus.br/SCON/'

# Termos de pesquisa
CRITERIO_DE_PESQUISA_CONTEUDO = 'juros e mora e fazenda pública e correção e monetária'
DATA_DE_JULGAMENTO_INICIAL_CONTEUDO = '01/10/2020'
DATA_DE_JULGAMENTO_FINAL_CONTEUDO = '01/10/2025'


if __name__ == '__main__':
    install(show_locals=False)
    print("Início da execução do Script")

    with sync_playwright() as playwright:
        constants = {
            "TIMEOUT": TIMEOUT,
            "URL": URL,
            "CRITERIO_DE_PESQUISA_CONTEUDO": CRITERIO_DE_PESQUISA_CONTEUDO,
            "DATA_DE_JULGAMENTO_INICIAL_CONTEUDO": DATA_DE_JULGAMENTO_INICIAL_CONTEUDO,
            "DATA_DE_JULGAMENTO_FINAL_CONTEUDO": DATA_DE_JULGAMENTO_FINAL_CONTEUDO,
        }
        run(playwright, constants=constants)

    # le_pagina_de_arquivo()

    juntar_dados_de_cada_pagina()
