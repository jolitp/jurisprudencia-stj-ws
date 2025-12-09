import pytest

from functions.extract import le_pagina_de_arquivo, pegar_documentos

def test_le_pagina_de_arquivo__is_html():
    file = "tests/busca pericia em novembro - STJ -_Jurisprudência do STJ (12_8_2025 6：14：33 PM).html"
    html = le_pagina_de_arquivo(file)
    is_html = '<!DOCTYPE html>' in html
    assert is_html


def test_le_pagina_de_arquivo__is_not_none():
    file = "tests/busca pericia em novembro - STJ -_Jurisprudência do STJ (12_8_2025 6：14：33 PM).html"
    html = le_pagina_de_arquivo(file)
    assert html is not None


def test_le_pagina_de_arquivo__has_pdf_links():
    file = "tests/busca pericia em novembro - STJ -_Jurisprudência do STJ (12_8_2025 6：14：33 PM).html"
    html = le_pagina_de_arquivo(file)
    # <a href="javascript:inteiro_teor('/SCON/GetInteiroTeorDoAcordao?num_registro=202003388788&amp;dt_publicacao=06/11/2025')" data-bs-toggle="tooltip" data-bs-placement="bottom" title="" data-bs-original-title="Exibir o inteiro teor do acórdão." aria-label="Exibir o inteiro teor do acórdão."><img src="/recursos/imagens/iconeITA.png"></a>
    assert "javascript:inteiro_teor('/SCON/GetInteiroTeorDoAcordao?num_registro=" in html \
        # and "GetInteiroTeorDoAcordao?" in html\
        # and "" in html
    ...