from .config import constants as C
from .config.parsing import search_config
from .transform import last_word_from_text

import playwright.sync_api._generated
# from rich.console import Console
# from rich.table import Table
from bs4 import BeautifulSoup
import bs4
import math
from rich import print
# from icecream import ic


#region    get_nome_aba_atual
def get_nome_aba_atual(page: playwright.sync_api._generated.Page):
    html_content = page.content()
    soup = BeautifulSoup(html_content, 'lxml')
    aba_name: str = soup.find("div", { "class": "barraOutrasBases" })\
                        .find("div", { "class": "ativo" })\
                        .text
    return aba_name
    ...
#endregion get_nome_aba_atual


#region
def get_aba_atual(page: playwright.sync_api._generated.Page):
    # html_content = page.content()
    # soup = BeautifulSoup(html_content, 'lxml')
    # aba_el = soup.find("div", { "class": "barraOutrasBases" })\
        # .find("div", { "class": "ativo" })
    # page.find("")
    # proxima_aba_selector = "a.iconeProximaPagina"
    # page.locator(proxima_pagina_selector).first.click()
    aba_el = page.locator(".barraOutrasBases > .ativo")
    return aba_el
    ...
#endregion


def get_number_of_docs_in_last_page(
        page: playwright.sync_api._generated.Page,
    ):
    n_de_paginas = get_number_of_pages_to_traverse(page)
    el_attrs = { "class": "clsNumDocumento" }
    n_doc_el = find_1st_el_on_page(page, attributes=el_attrs)
    n_docs = int(last_word_from_text(n_doc_el))

    if n_de_paginas == 1:
        n_docs_until_last_page = n_docs
    else:
        n_docs_until_last_page = (n_de_paginas -1) * C.DOCS_PER_PAGE
    n_docs_ultima_pagina = n_docs - n_docs_until_last_page

    return n_docs_ultima_pagina


def get_number_of_pages_to_traverse(
        page: playwright.sync_api._generated.Page,
    ):
    page.wait_for_load_state("networkidle", timeout=C.TIMEOUT)

    el_attrs = { "class": "clsNumDocumento" }
    n_doc_el = find_1st_el_on_page(page, attributes=el_attrs)
    n_docs = int(last_word_from_text(n_doc_el))
    n_de_paginas = math.ceil(n_docs / C.DOCS_PER_PAGE)

    return n_de_paginas


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


#region    find 1st element on page
def find_1st_el_on_page(page: playwright.sync_api._generated.Page,
                        element_tag: str = "div",
                        attributes: dict = {}):
    html_content = page.content()
    soup = BeautifulSoup(html_content, 'lxml')
    return soup.find(element_tag, attributes)
#endregion find 1st element on page


#region    find all elements on page
def find_all_elements_on_page(page: playwright.sync_api._generated.Page,
                            element_tag: str = "div",
                            element_attributes: dict = {}):
    html_content = page.content()
    soup = BeautifulSoup(html_content, 'lxml')
    return soup.find_all(element_tag, element_attributes)
#endregion find all elements on page


#region    paginar
def paginar(page: playwright.sync_api._generated.Page):
    """
    Navega para a próxima página.

    Args:
        page: Objeto de página do Playwright.
    """
    print("Navegando para a próxima página.")

    # proxima_pagina_xpath = "xpath=/html/body/div[1]/section[2]/div[2]/div[4]/div[2]/div[1]/div[3]/form/div/div[2]/a[1]"
    proxima_pagina_selector = "a.iconeProximaPagina"
    page.locator(proxima_pagina_selector).first.click()
    pass
#endregion paginar


#region    preencher formulario
def preencher_formulario(page: playwright.sync_api._generated.Page,
                        # CRITERIO_DE_PESQUISA_CONTEUDO: str,
                        # DATA_DE_JULGAMENTO_INICIAL_CONTEUDO: str,
                        # DATA_DE_JULGAMENTO_FINAL_CONTEUDO: str
                        ):
    """
    Preenche o formulário inicial da pesquisa.

    Args:
        page: Objeto de página do Playwright.
    """
    # TODO receber dict com termos de pesquisa
    print("Preenchendo [blue]formulário[/] da página de pesquisa com os seguints campos:")
    print(f"  [blue]conteudo[/]: {C.CRITERIO_DE_PESQUISA_CONTEUDO}")
    print(f"  [blue]data de julgamento inicial[/]: {C.DATA_DE_JULGAMENTO_INICIAL_CONTEUDO}")
    print(f"  [blue]data de julgamento final[/]: {C.DATA_DE_JULGAMENTO_FINAL_CONTEUDO}")

    criterio_de_pesquisa_xpath = search_config["criterio_de_pesquisa_xpath"]
    pesquisa_avancada_xpath = search_config["pesquisa_avancada_xpath"]
    data_de_julgamento_inicial_xpath = search_config["data_de_julgamento_inicial_xpath"]
    data_de_julgamento_final_xpath = search_config["data_de_julgamento_final_xpath"]
    botao_buscar_xpath = search_config["botao_buscar_xpath"]

    page.locator(criterio_de_pesquisa_xpath).fill(C.CRITERIO_DE_PESQUISA_CONTEUDO)
    page.locator(pesquisa_avancada_xpath).click()
    page.locator(data_de_julgamento_inicial_xpath).fill(C.DATA_DE_JULGAMENTO_INICIAL_CONTEUDO)
    page.locator(data_de_julgamento_final_xpath).fill(C.DATA_DE_JULGAMENTO_FINAL_CONTEUDO)
    page.locator(criterio_de_pesquisa_xpath).click()
    page.locator(botao_buscar_xpath).click()
#endregion preencher formulario


#region    pegar documentos
def pegar_documentos(page: playwright.sync_api._generated.Page):
    """
    Encontra (usando BeautifulSoup) todos os documentos contidos na página atual.

    Args:
        page: page do playwright
    """
    # html_content = page.content()
    # soup = BeautifulSoup(html_content, 'lxml')
    # documento = soup.find_all("div", {"class": "documento"})
    el_attrs = {"class": "documento"}
    documentos = find_all_elements_on_page(page, element_attributes=el_attrs)
    return documentos
    # return documento
#endregion pegar documentos


#region    pegar dados do documento (new)
def pegar_dados_do_documento(doc: bs4.element.Tag,
                            aba: str = "acordaos 1"):
    """
    Coleta os dados relevantes de um documento específico.

    Args:
        doc: Elemento contendo apenas 1 (um) documento.
    """
    sections = doc.find_all("div", attrs={ "class": "paragrafoBRS" })

    sections_dict = {}

    # get numero do documento (index)
    n_doc_el = doc.find("div", { "class": "clsNumDocumento" })
    numero_documento = n_doc_el.text.split()[1]
    sections_dict["Índice"] = numero_documento

    # get aba
    sections_dict["Aba"] = aba

    for section in sections:
        section_name_el = section.find("div",
                                        attrs={ "class": "docTitulo" },
                                        recursive=False
                                    )
        section_name = list(section_name_el.stripped_strings)
        if type(section_name) is list:
            section_name = section_name[0]
            if "\n" in section_name or "  " in section_name:
                section_name = " ".join(section_name.split())
        if "Relator" in section_name:
            section_name = "Relator/Relatora"

        section_value_el = section.find("div", attrs={ "class": "docTexto" })
        section_value = list(section_value_el.stripped_strings)
        if type(section_value) is list:
            section_value = " ".join(section_value)
            if "\n" in section_value or "  " in section_value:
                section_value = " ".join(section_value.split())
        elif type(section_value) is str:
            if "\n" in section_value or "  " in section_value:
                section_value = " ".join(section_value.split())

        sections_dict[str(section_name)] = section_value
        ...

    # get pdf link
    # NOTE em decisoes democraticas abre uma nova janela e o link é este:
    # processo.stj.jus.br/processo/pesquisa/?num_registro=202502557087
    attrs = { "data-bs-original-title": "Exibir o inteiro teor do acórdão."}
    pdf_dl_btn = doc.find("a", attrs=attrs)
    url_base = "https://processo.stj.jus.br"
    href = url_base + pdf_dl_btn.get("href").replace("javascript:inteiro_teor('", "")\
                                .replace("')", "")
    sections_dict["PDF Link"] = href

    # get recurso repetitivo link (tema)
    attrs = { "class": "barraDocRepetitivo" }
    recurso_repetitivo_el = doc.find("div", attrs=attrs)
    sections_dict["Link Recurso Repetitivo"] = ""
    if recurso_repetitivo_el is not None:
        recurso_repetitivo_link_el = recurso_repetitivo_el.find("a")
        sections_dict["Link Recurso Repetitivo"] = recurso_repetitivo_link_el.get("href")
        ...

    return sections_dict
#endregion pegar dados do documento (new)


#region    le pagina
def le_pagina(page: playwright.sync_api._generated.Page,
            aba: str = "acordaos_1"
            ):
    """
    Lê a página atual, retornando os dados.

    Args:
        page: Objeto de página do Playwright.
    """

    documentos = pegar_documentos(page)

    header = []
    todos_dados_desta_pagina = []
    for documento in documentos:
        dados = pegar_dados_do_documento(documento, aba)
        todos_dados_desta_pagina.append(dados)
        header = dados.keys()

    return (todos_dados_desta_pagina, header)
#endregion le pagina


#region    le pagina de arquivo
def le_pagina_de_arquivo(file: str):
    """
    Lê a página atual salva em arquivo HTML.
    Desnecessária neste momento (serviu o propósito de pular as etapas de preenchimento do formulário)
    """
    try:
        # with open('resultados-1a-pagina.html', 'r', encoding='utf-8') as f:
        with open(file, 'r', encoding='utf-8') as f:
            html_content = f.read()
            #print(html_content)
            # TODO separar essa função
            return html_content # para teste

            documentos = pegar_documentos(html_content, None)
            # inspect(documentos)
            # print("documentos size: ", len(documentos))
            todos_dados_desta_pagina = []

            # dado = pegar_dados_do_documento(documentos[0])
            for documento in documentos:
                dados = pegar_dados_do_documento(documento)
                todos_dados_desta_pagina.append(dados)
            # print(todos_dados_desta_pagina)

    except FileNotFoundError:
        print("Error: The specified file was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
#endregion le pagina de arquivo

