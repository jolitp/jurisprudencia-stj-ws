from .save import  salvar_dados_da_pagina_atual_em_csv
from .extract import paginar, preencher_formulario, le_pagina #, le_pagina_de_arquivo

import time
import math
from icecream import ic
from bs4 import BeautifulSoup
from rich import print


def run(playwright, constants):
    """
    roda o navegador usando Playwright

    Args:
        playwright: instância do Playwright
    """
    TIMEOUT = constants["TIMEOUT"]
    # user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    # realistic_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"

    browser = playwright.firefox.launch(
        #args=['--start-maximized'],
        headless=False, # toggle
        # headless=True, # toggle
    )
    context = browser.new_context(
        # record_video_dir = "videos/"
        # viewport={"width": 1920, "height": 1080},
        # user_agent=realistic_user_agent
    )
    page = context.new_page()
    page.goto(constants["URL"])

    preencher_formulario(page,
        CRITERIO_DE_PESQUISA_CONTEUDO = constants["CRITERIO_DE_PESQUISA_CONTEUDO"],
        DATA_DE_JULGAMENTO_INICIAL_CONTEUDO = constants["DATA_DE_JULGAMENTO_INICIAL_CONTEUDO"],
        DATA_DE_JULGAMENTO_FINAL_CONTEUDO = constants["DATA_DE_JULGAMENTO_FINAL_CONTEUDO"],
    )

    # aba_decisoes_monocraticas = soup.find("div", { "id": "campoDTXT"})
    # aba_decisoes_monocraticas_xpath = "html body div.container-fluid.p-0 section.conteudo.container-xxl div#corpopaginajurisprudencia.px-0.px-sm-1.px-md-2.px-xl-4.container-xxl div.navegacaoDocumento div.barraOutrasBasesWrapper.d-print-none div.barraOutrasBases div#campoDTXT.tabBase a"
    # page.locator(aba_decisoes_monocraticas_xpath).click()
    page.wait_for_load_state("networkidle", timeout=TIMEOUT)

    # muda o número de documentos por página de 10 para 50
    print("Mudando o número de [cyan]Documentos/Página[/] de [cyan]10[/] para [cyan]50[/]")
    page.locator("#qtdDocsPagina").select_option("50")
    time.sleep(15) # HACK wait_for_load_state("networkidle") não funciona ao clicar na caixa
    page.wait_for_load_state("networkidle", timeout=TIMEOUT)
    print("50 documentos por página a partir de agora")

    html_content = page.content()
    soup = BeautifulSoup(html_content, 'lxml')
    numero_de_documentos = soup.find("div", { "class": "clsNumDocumento" }).get_text().strip().split(" ")[-1]
    numero_de_documentos = int(numero_de_documentos)
    numero_de_paginas = math.ceil(numero_de_documentos / 50)

    for numero_da_pagina_atual in range(1, numero_de_paginas + 1):
        page.wait_for_load_state("networkidle", timeout=TIMEOUT)
        print(f"coletando dados da página número {numero_da_pagina_atual}")

        # BUG: quando já existem arquivos csv parciais,
        # o script conta a partir do próximo arquivo não existente.
        # Mas não navega para a página certa.

        # arquivo_csv_atual = f'dados_csv/pagina{numero_da_pagina_atual}.csv'

        # if os.path.exists(arquivo_csv_atual):
        #     print(f"Ignorando. [yellow]{arquivo_csv_atual}[/] já existe.")
        #     continue

        page.wait_for_load_state("networkidle", timeout=TIMEOUT)
        html_content = page.content()
        soup = BeautifulSoup(html_content, 'lxml')

        numero_de_documentos = soup.find("div", { "class": "clsNumDocumento" }).get_text().strip()
        ic(numero_de_documentos)

        page.wait_for_load_state("networkidle", timeout=TIMEOUT)
        html_content = page.content()
        soup = BeautifulSoup(html_content, 'lxml')
        dados = le_pagina(soup)
        salvar_dados_da_pagina_atual_em_csv(numero_da_pagina_atual, dados)
        page.wait_for_load_state("networkidle", timeout=TIMEOUT)

        if numero_da_pagina_atual == numero_de_paginas:
            break
        paginar(page)
        page.wait_for_load_state("networkidle", timeout=TIMEOUT)

    page.wait_for_load_state("networkidle", timeout=TIMEOUT)
    browser.close()
