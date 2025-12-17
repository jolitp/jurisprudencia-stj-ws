import functions.config.constants as C

from functions.navigate import  wait_for_page_to_change_document_number\
                            ,   muda_para_proxima_aba\
                            ,   paginar\
                            ,   check_if_tabs_have_documents

from functions.extract import get_info_on_tabs\
                            , preencher_formulario\
                            , le_pagina\
                            , find_1st_el_on_page\
                            , get_nome_aba_atual\
                            , get_number_of_pages_to_traverse

from functions.load import salvar_dados_da_pagina_atual_em_csv\
                        ,  juntar_dados_de_cada_pagina\
                        ,  append_to_timestamp_file

from functions.transform import get_text

import time
import datetime
import typer
from icecream import ic

from rich import print
from playwright.sync_api import sync_playwright
import playwright

# from rich.traceback import install
# import pretty_errors
from rich.console import Console

from icecream import install as icecream_install
icecream_install()

console = Console()
# ic.configureOutput(includeContext=True)

# app = typer.Typer(pretty_exceptions_enable=False)
app = typer.Typer(pretty_exceptions_show_locals=False)


# import pretty_errors

DT_NOW = datetime.datetime.now()


def processa_aba_atual(
    page: playwright.sync_api._generated.Page,
    ):
    ic()

    page.wait_for_load_state("networkidle", timeout=C.TIMEOUT)
    wait_for_page_to_change_document_number(page, console)
    page.wait_for_load_state("networkidle", timeout=C.TIMEOUT)

    nome_aba_atual = get_nome_aba_atual(page)
    n_de_paginas = get_number_of_pages_to_traverse(page)

    start = DT_NOW.timestamp
    end = DT_NOW.timestamp
    delta = 0
    for n_pag_atual in range(1, n_de_paginas + 1):
        start = datetime.datetime.now().timestamp()
        page.wait_for_load_state("networkidle", timeout=C.TIMEOUT)
        print(f"coletando dados da página { n_pag_atual } de { n_de_paginas }")

        aba = get_info_on_tabs(page)["Current"]["Name"]
        n_docs\
            = find_1st_el_on_page(page,
                                attributes={ "class": "clsNumDocumento" })
        n_docs = get_text(n_docs)

        page.wait_for_load_state("networkidle", timeout=C.TIMEOUT)
        dados, header = le_pagina(page, aba=aba)
        salvar_dados_da_pagina_atual_em_csv(
            n_pag_atual,
            dados,
            header,
            aba=nome_aba_atual,
            script_start_datetime=DT_NOW
        )

        if n_pag_atual == n_de_paginas:
            break
        paginar(page, n_pag_atual)

        page.wait_for_load_state("networkidle", timeout=C.TIMEOUT)

        end = datetime.datetime.now().timestamp()
        delta = int(end - start)

        append_to_timestamp_file(n_pag_atual,
            start, end, delta, aba,
            script_start_datetime=DT_NOW
        )

    juntar_dados_de_cada_pagina(
        aba=nome_aba_atual,
        script_start_datetime=DT_NOW
    )


def run(pw: playwright.sync_api._generated.Playwright,
        tab: str
        ):
    """
    roda o navegador usando Playwright

    Args:
        playwright: instância do Playwright
    """
    ic()

    browser = pw.firefox.launch(
        headless=False, # toggle
        # headless=True, # toggle
    )
    context = browser.new_context(viewport={"width": 960, "height": 1080})
    page = context.new_page()

    print(f"Navegando para a URL: {C.URL}")
    page.goto(C.URL)

    preencher_formulario(page)

    tab_is_acordaos_1 = any(tab in x for x in C.ACCEPTED_VALUES_ACORDAOS_1)
    tab_is_acordaos_2 = any(tab in x for x in C.ACCEPTED_VALUES_ACORDAOS_2)
    tab_is_decisoes_m = any(tab in x for x in C.ACCEPTED_VALUES_DECISOES_MONOCRATICAS)

    tabs_docs = check_if_tabs_have_documents(page)
    if tab_is_acordaos_1:
        ic("a 1")
        if tabs_docs["acordaos_1"]:
            processa_aba_atual(page)
        else:
            print("Não há documentos na aba Acórdãos 1")
    elif tab_is_acordaos_2:
        ic("a 2")
        if tabs_docs["acordaos_2"]:
            muda_para_proxima_aba(page)
            processa_aba_atual(page)
        else:
            print("Não há documentos na aba Acórdãos 2")
    elif tab_is_decisoes_m:
        ic("d m")
        if tabs_docs["decisoes_monocraticas"]:
            page.wait_for_load_state("networkidle", timeout=C.TIMEOUT)
            # wait_for_page_to_change_document_number(page)
            nome_aba_atual = get_nome_aba_atual(page)
            # nome_aba_atual = get_info_on_tabs(page)["Current"]["Name"]

            while "Decisões Monocráticas" not in nome_aba_atual:
                nome_aba_atual = get_nome_aba_atual(page)
                # ic("Decisões Monocráticas" not in nome_aba_atual)
                # ic(nome_aba_atual)
                muda_para_proxima_aba(page)
                page.wait_for_load_state("networkidle", timeout=C.TIMEOUT)
                time.sleep(3)
            processa_aba_atual(page)
        else:
            print("Não há documentos na aba Decisões Monocráticas")

    # juntar_dados_de_cada_aba(DT_NOW)

    browser.close()


def check_arguments(tab1: str, tab2: str):
    ic()

    tab = " ".join([tab1, tab2])
    # ic(tab)
    tab_in_accepted_values = any(tab in x for x in C.ACCEPTED_ARGUMENTS)
    # ic(tab_in_accepted_values)
    return tab_in_accepted_values, tab


#region main
@app.command()
def main(
    tab1: str,
    tab2: str,
    debug: bool = False
):
    # print("debug: ", debug)
    ic.disable()
    if debug:
        ic.enable()
    ic()
    print("Início da execução do Script")

    tab_in_accepted_values, tab = check_arguments(tab1, tab2)
    if tab_in_accepted_values:
        with sync_playwright() as pw:
            run(pw, tab)
    else:
        print(f"[red]X[/] Argumentos [blue]{tab1}[/] e [blue]{tab2}[/] [red]INVALIDOS[/]")
        print("  usar as seguntes combinações para escolher a aba correta:")
        print()
        for value in C.ACCEPTED_ARGUMENTS:
            print(f"- [green]{value}[/]")


if __name__ == '__main__':
    app()
    # typer.run(main)
#endregion main
