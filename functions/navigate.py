from .config import constants as C

from .extract import  pegar_documentos\
                    , get_info_on_tabs\
                    , get_number_of_docs_in_last_page\
                    , get_total_number_of_documents\
                    , pegar_documentos

from .transform import last_word_from_text

from icecream import ic
import time

from rich import print
import playwright
# from bs4 import BeautifulSoup
# from rich.console import Console
# import rich
# from rich.console import Console

# console = Console()


# def check_if_next_tab_have_documents(
#     page: playwright.sync_api._generated.Page,
# ):
#     ic()

#     page.wait_for_load_state("networkidle", timeout=C.TIMEOUT)

#     tab_info = get_info_on_tabs(page)
#     next_tab_doc_num = tab_info['Next']['Name']

#     if "Acórdãos 1".lower() in next_tab_doc_num.lower():
#         next_tab_doc_num = next_tab_doc_num.replace("Acórdãos 1 (", "")\
#                                             .replace(")", "")
#         next_tab_doc_num = int(next_tab_doc_num)
#     elif "Acórdãos 2".lower() in next_tab_doc_num.lower():
#         next_tab_doc_num = next_tab_doc_num.replace("Acórdãos 2 (", "")\
#                                             .replace(")", "")
#         next_tab_doc_num = int(next_tab_doc_num)
#     elif "Decisões Monocráticas".lower() in next_tab_doc_num.lower():
#         next_tab_doc_num = next_tab_doc_num.replace("Decisões Monocráticas", "")\
#                                             .replace(")", "")
#         next_tab_doc_num = int(next_tab_doc_num)

#     if next_tab_doc_num == 0:
#         return False
#     else:
#         return True


# def check_if_current_tab_have_documents(
#     page: playwright.sync_api._generated.Page,
# ):
#     ic()

#     page.wait_for_load_state("networkidle", timeout=C.TIMEOUT)

#     tab_info = get_info_on_tabs(page)
#     current_tab_doc_num = tab_info['Current']['Name']

#     if "Acórdãos 1".lower() in current_tab_doc_num.lower():
#         current_tab_doc_num = current_tab_doc_num.replace("Acórdãos 1 (", "")\
#                                             .replace(")", "")
#         current_tab_doc_num = int(current_tab_doc_num)
#     elif "Acórdãos 2".lower() in current_tab_doc_num.lower():
#         current_tab_doc_num = current_tab_doc_num.replace("Acórdãos 2 (", "")\
#                                             .replace(")", "")
#         current_tab_doc_num = int(current_tab_doc_num)
#     elif "Decisões Monocráticas".lower() in current_tab_doc_num.lower():
#         current_tab_doc_num = current_tab_doc_num.replace("Decisões Monocráticas", "")\
#                                             .replace(")", "")
#         current_tab_doc_num = int(current_tab_doc_num)

#     if current_tab_doc_num == 0:
#         return False
#     else:
#         return True


def check_if_tabs_have_documents(
    page: playwright.sync_api._generated.Page,
):
    ic()

    page.wait_for_load_state("networkidle", timeout=C.TIMEOUT)

    tab_info = get_info_on_tabs(page)

    acordaos_1_tab_doc_num = tab_info['acordaos_1']['name']
    acordaos_2_tab_doc_num = tab_info['acordaos_2']['name']
    decisoes_monocraticas_tab_doc_num = tab_info['decisoes_monocraticas']['name']

    acordaos_1_tab_doc_num = acordaos_1_tab_doc_num.replace("Acórdãos 1 (", "")\
                                                    .replace(")", "")\
                                                    .replace(".", "")
    acordaos_1_tab_doc_num = int(acordaos_1_tab_doc_num)

    acordaos_2_tab_doc_num = acordaos_2_tab_doc_num.replace("Acórdãos 2 (", "")\
                                                .replace(")", "")\
                                                .replace(".", "")
    acordaos_2_tab_doc_num = int(acordaos_2_tab_doc_num)

    decisoes_monocraticas_tab_doc_num = \
        decisoes_monocraticas_tab_doc_num.replace("Decisões Monocráticas (", "")\
                                        .replace(")", "")\
                                        .replace(".", "")
    decisoes_monocraticas_tab_doc_num = int(decisoes_monocraticas_tab_doc_num)

    # ic(locals())
    # ic(acordaos_1_tab_doc_num)
    # ic(acordaos_2_tab_doc_num)
    # ic(decisoes_monocraticas_tab_doc_num)


    result = {
        "acordaos_1": False if acordaos_1_tab_doc_num == 0 else True,
        "acordaos_2": False if acordaos_2_tab_doc_num == 0 else True,
        "decisoes_monocraticas": False if decisoes_monocraticas_tab_doc_num == 0 else True,
    }

    return result


def wait_for_page_to_change_document_number(
    page: playwright.sync_api._generated.Page,
    console
    ):
    ic()

    check_if_tabs_have_documents(page)

    page.wait_for_load_state("networkidle", timeout=C.TIMEOUT)

    page.locator("#qtdDocsPagina").select_option("50")

    with console.status(
        "Mudando o número de [cyan]Docs/Pág[/] de [cyan]10[/] para [cyan]50[/]"):

        while True:
            # TODO check against the remaining number of documents in the last page
            time.sleep(1)
            ic("inside loop")

            page.wait_for_load_state("networkidle", timeout=C.TIMEOUT)
            n_docs_ult_pag = get_number_of_docs_in_last_page(page)
            n_docs_pag_atual = len(pegar_documentos(page))

            if n_docs_pag_atual == C.DOCS_PER_PAGE\
            or n_docs_pag_atual == n_docs_ult_pag\
            or n_docs_ult_pag == 0:
                break
            ...
        ...
    ...
    # page.wait_for_load_state("networkidle", timeout=C.TIMEOUT)


def muda_para_proxima_aba(page: playwright.sync_api._generated.Page):
    ic()

    page.wait_for_load_state("networkidle", timeout=C.TIMEOUT)

    abas = get_info_on_tabs(page)
    proxima_aba = abas["Next"]["Locator"]
    nome_proxima_aba = abas["Next"]["Name"]
    if proxima_aba is None:
        return

    print(f"Mudando para próxima aba: [blue]{nome_proxima_aba}[/]")
    proxima_aba.click()

    ...


#region    paginar
def paginar(page: playwright.sync_api._generated.Page,
            source_page_number: int,
            ):
    """
    Navega para a próxima página.

    Args:
        page: Objeto de página do Playwright.
    """
    ic()
    # print("="*100)
    # print("-"*100)
    # print("Navegando para a próxima página.")

    first_doc_el = pegar_documentos(page)[0]
    # ic(first_doc_el)
    num_doc_1st = first_doc_el.find("div", { "class": "clsNumDocumento" })
    # ic(num_doc_1st)
    num_doc_text = num_doc_1st.text.strip()
    ic(num_doc_text)

    first_doc = source_page_number*C.DOCS_PER_PAGE + 1
    ic(first_doc)
    last_page_doc = source_page_number*C.DOCS_PER_PAGE
    ic(last_page_doc)
    print(f"Mudando para página número {source_page_number + 1}")
    print(f"Documento {first_doc} à documento {last_page_doc}")

    total_n_docs = get_total_number_of_documents(page)
    ic(total_n_docs)

    text = f"Documento {first_doc} de {total_n_docs}"
    ic(text)
    # print(f" > Trying to find element with text: [green]{text}[/]")
    num_doc_el = page.locator(".clsNumDocumento", has_text=text)
    ic(num_doc_el)

    # print("Navegando para próxima página por javascript")
    result = page.evaluate(f"navegaForm('{first_doc}');")
    ic(result)

    count = 0
    while True:
        # print(" ", "="*50)
        # print("sleeping until element is found")
        time.sleep(1)
        count += 1
        ic(count)

        # first_doc_el = pegar_documentos(page)[0]
        first_doc_el = None
        while not first_doc_el:
            time.sleep(1)
            first_doc_el = pegar_documentos(page)

        first_doc_el = first_doc_el[0]

        # ic(first_doc_el)
        num_doc_1st = first_doc_el.find("div", { "class": "clsNumDocumento" })
        # ic(num_doc_1st)
        num_doc_text = num_doc_1st.text.strip()

        num_doc_el = page.locator(".clsNumDocumento", has_text=text, )
        # num_doc_el

        # ic(num_doc_el)
        # if num_doc_el:
        #     break
        ic(text)
        ic(num_doc_text)
        ic(text == num_doc_text)
        if text == num_doc_text:
            # print(" ", "="*50)
            break
        # print(" ", "="*50)
        ...
    # print("-"*100)
    # print("="*100)


#endregion paginar


