from rich.console import Console
from rich.table import Table
from bs4 import BeautifulSoup
from rich import print

#region paginar
def paginar(page):
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


#region preencher formulario
def preencher_formulario(page,
                        CRITERIO_DE_PESQUISA_CONTEUDO,
                        DATA_DE_JULGAMENTO_INICIAL_CONTEUDO,
                        DATA_DE_JULGAMENTO_FINAL_CONTEUDO
                        ):
    """
    Preenche o formulário inicial da pesquisa.

    Args:
        page: Objeto de página do Playwright.
    """
    print("Preenchendo formulário da página de pesquisa.")

    criterio_de_pesquisa_xpath = '//*[@id="pesquisaLivre"]'
    pesquisa_avancada_xpath = '//*[@id="idMostrarPesquisaAvancada"]'
    data_de_julgamento_inicial_xpath = '//*[@id="dtde1"]'
    data_de_julgamento_final_xpath = '//*[@id="dtde2"]'
    botao_buscar_xpath = 'xpath=/html/body/div[1]/section[2]/div[3]/form[1]/div[2]/div[2]/div[2]/div[1]/div/button'

    # seleção de checkbox Orgãos Julgadores desnecessária
    # pois estes campos funcionam como filtro, e está sendo pedido para selecionar TODOS
    # Isso vai contra o propósito de aplicar um FILTRO

    page.locator(criterio_de_pesquisa_xpath).fill(CRITERIO_DE_PESQUISA_CONTEUDO)
    page.locator(pesquisa_avancada_xpath).click()
    page.locator(data_de_julgamento_inicial_xpath).fill(DATA_DE_JULGAMENTO_INICIAL_CONTEUDO)
    page.locator(data_de_julgamento_final_xpath).fill(DATA_DE_JULGAMENTO_FINAL_CONTEUDO)
    page.locator(criterio_de_pesquisa_xpath).click()
    page.locator(botao_buscar_xpath).click()
#endregion preencher formulario


#region pegar documentos
def pegar_documentos(soup):
    """
    Encontra (usando BeautifulSoup) todos os documentos contidos na página atual.

    Args:
        soup: Objeto BeautifulSoup usado anteriormente.
    """
    documento = soup.find_all("div", {"class": "documento"})
    # print(documento)
    return documento
#endregion pegar documentos


#region pegar dados do documento
def pegar_dados_do_documento(documento):
    """
    Coleta os dados relevantes de um documento específico.

    Args:
        documento: Elemento contendo apenas 1 (um) documento.
    """
    # imprimir_tabela = DEBUG
    imprimir_tabela = False

    # Os metadados tipicos a serem extraidos incluem, mas nao se limitam a:

    # - Numero do Processo/Registro
    # processo = documento.find("div", string="Processo")
    processo = documento.find("div", { "class": "col clsIdentificacaoDocumento" })
    # print(processo.find_next_sibling().get_text())
    if processo:
        processo = processo.get_text().strip().split(" ")[1].strip()
    else:
        processo = ""

    # - [?] Tipo de Recurso (e.g., RESP)
    # pegar a primeira palavra do header (azul)
    tipo_de_recurso = documento.find("div", { "class": "col clsIdentificacaoDocumento" })
    if tipo_de_recurso:
        tipo_de_recurso = tipo_de_recurso.get_text().strip().split(" ")[0]
    else:
        tipo_de_recurso = ""

    # - Ministro Relator
    ministro_relator = documento.find("div", string="Relator")
    if ministro_relator:
        ministro_relator = ministro_relator.find_next_sibling().get_text().strip()
    else:
        ministro_relator = ""

    # - Orgao Julgador
    orgao_julgador = documento.find("div", string="Órgão Julgador")
    if orgao_julgador:
        orgao_julgador = orgao_julgador.find_next_sibling().get_text().strip()
    else:
        orgao_julgador = ""

    # - Data do Julgamento
    data_do_julgamento = documento.find("div", string="Data do Julgamento")
    if data_do_julgamento:
        data_do_julgamento = data_do_julgamento.find_next_sibling().get_text().strip()
    else:
        data_do_julgamento = ""

    # - Data da Publicacdo/Fonte
    data_da_publicacao_fonte = documento.find("div", string="Data da Publicação/Fonte")
    if data_da_publicacao_fonte:
        data_da_publicacao_fonte = data_da_publicacao_fonte.find_next_sibling()\
                                                            .get_text()\
                                                            .strip()\
                                                            .replace("DJEN ", "")
    else:
        data_da_publicacao_fonte = ""


    # rows = documento.find_all("div", { "class": "row" })
    # tese_juridica = rows[3].find("div", { "class": "docTexto"})
    # if tese_juridica:
    #     tese_juridica = tese_juridica.get_text().strip()
    # else:
    #     tese_juridica = ""

    # - URL especifica do acérdao (para referéncia futura)
    url_base = "https://processo.stj.jus.br"
    url_do_documento = documento.find("a", { "aria-label": "Exibir o inteiro teor do acórdão." })

    if url_do_documento:
        url_do_documento = url_do_documento.get('href')\
                                .replace("javascript:inteiro_teor('", "")\
                                .replace("')", "")
    else:
        url_do_documento = None

    if url_do_documento:
        url_do_acordao = url_base + url_do_documento
    else:
        url_do_acordao = ""



    # OUTROS CAMPOS
    # - Ementa
    ementa = documento.find("div", string="Ementa")
    if ementa:
        ementa = ementa.find_next_sibling().get_text().strip()
    else:
        ementa = ""

    # - Acórdão
    acordao = documento.find("div", string="Acórdão")
    if acordao:
        acordao = acordao.find_next_sibling().get_text().strip()
    else:
        acordao = ""



    # próximos dados sendo difíceis de apontar para o elemnto correto. Ignorados.
    #
    # # - Notas
    # # notas = documento.find("div", string="Notas").find_next_sibling().get_text().strip()
    # # notas = rows[6].find("div", { "class": "docTexto"})
    # notas = documento.find("div", string=re.compile("Notas"))
    # print(notas)
    # # if notas:
    # #     notas = notas.find_next_sibling().get_text().strip()
    # # else:
    # #     notas = "asdf"
    #
    # # - Referência Legislativa
    # # referencia_legislativa = rows[7].find("div", { "class": "docTexto"})
    # referencia_legislativa  = documento.find("div", string="Legislativa")
    # if referencia_legislativa:
    #     referencia_legislativa = referencia_legislativa.find_next_sibling().get_text().strip()
    # else:
    #     referencia_legislativa = ""
    #
    # # - Jurisprudência Citada
    # # jurisprudencia_citada = rows[8].find("div", { "class": "docTexto"})
    # jurisprudencia_citada = documento.find("div", string="Jurisprudência")
    # if jurisprudencia_citada:
    #     jurisprudencia_citada = jurisprudencia_citada.find_next_sibling().get_text().strip()
    # else:
    #     jurisprudencia_citada = ""

    data = {
        "processo": processo,
        "tipo_de_recurso": tipo_de_recurso,
        "ministro_relator": ministro_relator,
        "orgao_julgador": orgao_julgador,
        "data_do_julgamento": data_do_julgamento,
        "data_da_publicacao_fonte": data_da_publicacao_fonte,
        # "tese_juridica": tese_juridica,
        "url_do_acordao": url_do_acordao,
        "ementa": ementa,
        "acordao": acordao,
        # "notas": notas,
        # "referencia_legislativa": referencia_legislativa,
        # "jurisprudencia_citada": jurisprudencia_citada,
    }

    if imprimir_tabela:
        table = Table(title="Dados", row_styles=["blue", "bright_blue"])
        table.add_column("Nome", justify="left")
        table.add_column("Valor", justify="right")

        table.add_row("processo", processo)
        table.add_row("tipo_de_recurso", tipo_de_recurso)
        table.add_row("ministro_relator", ministro_relator)
        table.add_row("orgao_julgador", orgao_julgador)
        table.add_row("data_do_julgamento", data_do_julgamento)
        table.add_row("data_da_publicacao_fonte", data_da_publicacao_fonte)
        # table.add_row("tese_juridica", tese_juridica[0:80] + " (...) ")
        table.add_row("url_do_acordao", url_do_acordao)
        table.add_row("ementa", ementa[0:80] + " (...) ")
        table.add_row("acordao", acordao[0:80] + " (...) ")
        # table.add_row("notas", notas[0:99])
        # table.add_row("referencia_legislativa", referencia_legislativa[0:99])
        # table.add_row("jurisprudencia_citada", jurisprudencia_citada[0:99])

        console = Console()
        console.print(table)

    return data
#endregion pegar dados do documento


#region le pagina
def le_pagina(soup):
    """
    Lê a página atual

    Args:
        html_content: Conteúdo em HTML retirado da página.
        page: Objeto de página do Playwright.
    """

    documentos = pegar_documentos(soup)
    # print("documentos size: ", len(documentos))

    todos_dados_desta_pagina = []
    for documento in documentos:
        dados = pegar_dados_do_documento(documento)
        todos_dados_desta_pagina.append(dados)
    # print(todos_dados_desta_pagina)

    return todos_dados_desta_pagina
#endregion le pagina


#region le pagina de arquivo
def le_pagina_de_arquivo(file):
    """
    Lê a página atual salva em arquivo HTML.
    Desnecessária neste momento (serviu o propósito de pular as etapas de preenchimento do formulário)
    """
    try:
        # with open('resultados-1a-pagina.html', 'r', encoding='utf-8') as f:
        with open(file, 'r', encoding='utf-8') as f:
            html_content = f.read()
            #print(html_content)
            return html_content

            soup = BeautifulSoup(html_content, 'lxml') # Using lxml parser (faster)
            # Or: soup = BeautifulSoup(html_content, 'html.parser') # Using Python's built-in parser

            documentos = pegar_documentos(soup, None)
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

