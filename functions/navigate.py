from .config import constants as C

from .extract import  pegar_documentos\
                    , get_info_on_tabs\
                    , get_number_of_docs_in_last_page\

import time

from rich import print
import playwright
# from rich.console import Console
# import rich
# from rich.console import Console

# console = Console()



def wait_for_page_to_change_document_number(
    page: playwright.sync_api._generated.Page,
    console
    ):
    page.wait_for_load_state("networkidle", timeout=C.TIMEOUT)

    page.locator("#qtdDocsPagina").select_option("50")

    with console.status(
        "Mudando o número de [cyan]Docs/Pág[/] de [cyan]10[/] para [cyan]50[/]"):
        while True:
            # TODO check against the remaining number of documents in the last page
            time.sleep(1)

            n_docs_ult_pag = get_number_of_docs_in_last_page(page)
            n_docs_pag_atual = len(pegar_documentos(page))

            if n_docs_pag_atual == C.DOCS_PER_PAGE or n_docs_pag_atual == n_docs_ult_pag:
                break
            ...
        ...
    ...


def muda_para_proxima_aba(page: playwright.sync_api._generated.Page):
    page.wait_for_load_state("networkidle", timeout=C.TIMEOUT)

    abas = get_info_on_tabs(page)
    proxima_aba = abas["Next"]["Locator"]
    nome_proxima_aba = abas["Next"]["Name"]
    if proxima_aba is None:
        return

    print(f"Mudando para próxima aba: [blue]{nome_proxima_aba}[/]")
    proxima_aba.click()

    ...


