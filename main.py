from functions.load import    salvar_dados_da_pagina_atual_em_csv\
                            , juntar_dados_de_cada_pagina\
                            , juntar_dados_de_cada_aba

from functions.extract import paginar\
                            , preencher_formulario\
                            , le_pagina\
                            , pegar_documentos\
                            , find_1st_el_on_page\
                            , get_nome_aba_atual\

from functions.transform import last_word_from_text\
                            ,   get_text

import datetime
import time
import math
import re
from icecream import ic
from rich import print
from playwright.sync_api import sync_playwright
import playwright
from bs4 import BeautifulSoup

from rich.traceback import install
from rich.console import Console

console = Console()
# install(show_locals=True) # toggle
install(show_locals=False) # toggle


DT_NOW = datetime.datetime.now()
DEBUG: bool = False
# DEBUG: bool = True # toggle
TIMEOUT: int = 90000
URL: str = 'https://processo.stj.jus.br/SCON/'
DOCS_PER_PAGE = 50

# Termos de pesquisa
CRITERIO_DE_PESQUISA_CONTEUDO: str = 'juros e mora e fazenda pública e correção e monetária'
DATA_DE_JULGAMENTO_INICIAL_CONTEUDO: str = '01/10/2020'
DATA_DE_JULGAMENTO_FINAL_CONTEUDO: str = '01/10/2025'


def processa_aba_atual(page: playwright.sync_api._generated.Page):
    page.wait_for_load_state("networkidle", timeout=TIMEOUT)
    wait_for_page_to_change_document_number(page)
    page.wait_for_load_state("networkidle", timeout=TIMEOUT)

    nome_aba_atual = get_nome_aba_atual(page)
    n_de_paginas = get_number_of_pages_to_traverse(page)

    for n_pag_atual in range(1, n_de_paginas + 1):
        page.wait_for_load_state("networkidle", timeout=TIMEOUT)
        print(f"coletando dados da página { n_pag_atual } de { n_de_paginas }")

        n_docs\
            = find_1st_el_on_page(page,
                                attributes={ "class": "clsNumDocumento" })
        n_docs = get_text(n_docs)

        page.wait_for_load_state("networkidle", timeout=TIMEOUT)
        dados, header = le_pagina(page)
        salvar_dados_da_pagina_atual_em_csv(
            n_pag_atual,
            dados,
            header,
            aba=nome_aba_atual,
            script_start_datetime=DT_NOW
        )

        # ic(n_pag_atual == n_de_paginas)
        if n_pag_atual == n_de_paginas:
            break
        paginar(page)
        page.wait_for_load_state("networkidle", timeout=TIMEOUT)

    juntar_dados_de_cada_pagina(
        aba=nome_aba_atual,
        script_start_datetime=DT_NOW
    )
    ...


def wait_for_page_to_change_tab(page: playwright.sync_api._generated.Page,
                                aba: str):
    page.wait_for_load_state("networkidle", timeout=TIMEOUT)

    page.locator("#qtdDocsPagina").select_option("50")

    with console.status(f"Mudando para a aba: {aba}"):
        while True:
            # TODO check against the remaining number of documents in the last page
            time.sleep(1)

            first_doc = pegar_documentos(page)[0]
            # soup = BeautifulSoup(first_doc, 'lxml')

            attrs = { "class": "clsNumDocumento" }
            text_1st_doc = first_doc.find("div", attrs).text

            if "Documento 1 de " in text_1st_doc:
                break
            ...
        ...
    ...


def wait_for_page_to_change_document_number(page: playwright.sync_api._generated.Page):
    page.wait_for_load_state("networkidle", timeout=TIMEOUT)

    page.locator("#qtdDocsPagina").select_option("50")

    with console.status(
        "Mudando o número de [cyan]Docs/Pág[/] de [cyan]10[/] para [cyan]50[/]"):
        while True:
            # TODO check against the remaining number of documents in the last page
            time.sleep(1)

            n_docs_ult_pag = get_number_of_docs_in_last_page(page)
            n_docs_pag_atual = len(pegar_documentos(page))

            if n_docs_pag_atual == DOCS_PER_PAGE or n_docs_pag_atual == n_docs_ult_pag:
                break
            ...
        ...
    ...


def get_info_on_tabs(page: playwright.sync_api._generated.Page):
    aba_ativa = None
    proxima_aba = None
    nome_aba_ativa = None
    nome_proxima_aba = None

    # aba_sumulas = page.locator("id=campoSUMU")

    # IDs
    # id_aba_sumulas = "campoSUMU"
    id_aba_acordaos_1 = "campoACOR"
    id_aba_acordaos_2 = "campoBAEN"
    id_aba_decisoes_monocraticas = "campoDTXT"

    html_content = page.content()
    # ic(html_content)
    soup = BeautifulSoup(html_content, 'lxml')

    nome_aba_acordaos_1 = soup.find("div", { "id": id_aba_acordaos_1 })\
        .text
    nome_aba_acordaos_2 = soup.find("div", { "id": id_aba_acordaos_2 })\
        .text
    nome_aba_decisoes_monocraticas = soup.find("div", { "id": id_aba_decisoes_monocraticas })\
        .text

    # Abas (page locators)
    aba_acordaos_1 = page.locator(f"id={id_aba_acordaos_1}")
    aba_acordaos_2 = page.locator(f"id={id_aba_acordaos_2}")
    aba_decisoes_monocraticas = page.locator(f"id={id_aba_decisoes_monocraticas}")

    # Abas (bs4)
    bs_aba_acordaos_1 = find_1st_el_on_page(page, "div",
                                            attributes={"id": id_aba_acordaos_1})
    bs_aba_acordaos_2 = find_1st_el_on_page(page, "div",
                                            attributes={"id": id_aba_acordaos_2})
    bs_aba_decisoes_monocraticas = find_1st_el_on_page(page, "div",
                                            attributes={"id": id_aba_decisoes_monocraticas})

    # CSS classes
    acordaos_1_classes = bs_aba_acordaos_1.get("class")
    acordaos_2_classes = bs_aba_acordaos_2.get("class")
    decisoes_monocraticas_classes = bs_aba_decisoes_monocraticas.get("class")

    if "ativo" in acordaos_1_classes:
        aba_ativa = aba_acordaos_1
        nome_aba_ativa = nome_aba_acordaos_1

        proxima_aba = aba_acordaos_2
        nome_proxima_aba = nome_aba_acordaos_2

    if "ativo" in acordaos_2_classes:
        aba_ativa = aba_acordaos_2
        nome_aba_ativa = nome_aba_acordaos_2

        proxima_aba = aba_decisoes_monocraticas
        nome_proxima_aba = nome_aba_decisoes_monocraticas

    if "ativo" in decisoes_monocraticas_classes:
        aba_ativa = aba_decisoes_monocraticas
        nome_aba_ativa = nome_aba_decisoes_monocraticas

        proxima_aba = None
        nome_proxima_aba = None

    # ic(aba_ativa)
    # ic(proxima_aba)

    result = {
        "Current": {
            "Locator": aba_ativa,
            "Name": nome_aba_ativa,
        },
        "Next": {
            "Locator": proxima_aba,
            "Name": nome_proxima_aba,
        }
    }
    return result
    ...


def muda_para_proxima_aba(page: playwright.sync_api._generated.Page):
    page.wait_for_load_state("networkidle", timeout=TIMEOUT)

    abas = get_info_on_tabs(page)
    proxima_aba = abas["Next"]["Locator"]
    nome_proxima_aba = abas["Next"]["Name"]

    print(f"Mudando para próxima aba: [blue]{nome_proxima_aba}[/]")
    proxima_aba.click()

    wait_for_page_to_change_tab(page, nome_proxima_aba)
    ...


def get_number_of_docs_in_last_page(page: playwright.sync_api._generated.Page):
    n_de_paginas = get_number_of_pages_to_traverse(page)
    el_attrs = { "class": "clsNumDocumento" }
    n_doc_el = find_1st_el_on_page(page, attributes=el_attrs)
    n_docs = int(last_word_from_text(n_doc_el))

    if n_de_paginas == 1:
        n_docs_until_last_page = n_docs
    else:
        n_docs_until_last_page = (n_de_paginas -1) * DOCS_PER_PAGE
    n_docs_ultima_pagina = n_docs - n_docs_until_last_page

    return n_docs_ultima_pagina


def get_number_of_pages_to_traverse(page: playwright.sync_api._generated.Page):
    page.wait_for_load_state("networkidle", timeout=TIMEOUT)

    el_attrs = { "class": "clsNumDocumento" }
    n_doc_el = find_1st_el_on_page(page, attributes=el_attrs)
    n_docs = int(last_word_from_text(n_doc_el))
    n_de_paginas = math.ceil(n_docs / DOCS_PER_PAGE)

    return n_de_paginas


def run(pw: playwright.sync_api._generated.Playwright):
    """
    roda o navegador usando Playwright

    Args:
        playwright: instância do Playwright
    """
    browser = pw.firefox.launch(
        headless=False, # toggle
        # headless=True, # toggle
    )
    context = browser.new_context(viewport={"width": 960, "height": 1080})
    page = context.new_page()

    print(f"Navegando para a URL: {URL}")
    page.goto(URL)

    preencher_formulario(page,
        CRITERIO_DE_PESQUISA_CONTEUDO = CRITERIO_DE_PESQUISA_CONTEUDO,
        DATA_DE_JULGAMENTO_INICIAL_CONTEUDO = DATA_DE_JULGAMENTO_INICIAL_CONTEUDO,
        DATA_DE_JULGAMENTO_FINAL_CONTEUDO = DATA_DE_JULGAMENTO_FINAL_CONTEUDO,
    )

    # Aba Acórdãos 1
    # muda o número de documentos por página de 10 para 50
    processa_aba_atual(page)

    # Aba Acórdãos 2
    muda_para_proxima_aba(page)
    processa_aba_atual(page)

    # Aba Decisões Monocráticas
    muda_para_proxima_aba(page)
    processa_aba_atual(page)

    juntar_dados_de_cada_aba(DT_NOW)

    browser.close()


if __name__ == '__main__':
    ic.configureOutput(includeContext=True)
    print("Início da execução do Script")

    with sync_playwright() as pw:
        run(pw)
