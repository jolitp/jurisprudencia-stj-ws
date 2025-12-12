
DEBUG: bool = False
# DEBUG: bool = True # toggle
TIMEOUT: int = 90000
URL: str = 'https://processo.stj.jus.br/SCON/'
DOCS_PER_PAGE = 50

# Termos de pesquisa
CRITERIO_DE_PESQUISA_CONTEUDO: str = 'juros e mora e fazenda pública e correção e monetária'
DATA_DE_JULGAMENTO_INICIAL_CONTEUDO: str = '01/10/2020'
DATA_DE_JULGAMENTO_FINAL_CONTEUDO: str = '01/10/2025'

ACCEPTED_VALUES_ACORDAOS_1 = [
    "a 1",
    "acordaos 1",
    "acórdãos 1",
]
ACCEPTED_VALUES_ACORDAOS_2 = [
    "a 2",
    "acordaos 2",
    "acórdãos 2",
]
ACCEPTED_VALUES_DECISOES_MONOCRATICAS = [
    "d m",
    "decisoes monocraticas",
    "decisões monocráticas",
]

# CLI CONFIGURATION
ACCEPTED_ARGUMENTS = ACCEPTED_VALUES_ACORDAOS_1\
                    + ACCEPTED_VALUES_ACORDAOS_2\
                    + ACCEPTED_VALUES_DECISOES_MONOCRATICAS
