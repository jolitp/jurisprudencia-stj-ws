import pytest

from functions.extract import le_pagina_de_arquivo\
                            # , pegar_documentos\
                            # , pegar_dados_do_documento


HTML_FILE = "tests/busca pericia em novembro - STJ -_Jurisprudência do STJ (12_8_2025 6：14：33 PM).html"

@pytest.fixture
def html_from_file():
    return le_pagina_de_arquivo(HTML_FILE)


def test__le_pagina_de_arquivo__is_html(html_from_file):
    is_html = '<!DOCTYPE html>' in html_from_file
    assert is_html


def test__le_pagina_de_arquivo__is_not_none(html_from_file):
    assert html_from_file is not None


def test__le_pagina_de_arquivo__has_pdf_links(html_from_file):
    string = "javascript:inteiro_teor('/SCON/GetInteiroTeorDoAcordao?num_registro="
    assert string in html_from_file




@pytest.mark.xfail(raises=NotImplementedError)
def test__pegar_documentos():
    ...


@pytest.mark.xfail(raises=NotImplementedError)
def test__pegar_dados_do_documento__():
    ...




