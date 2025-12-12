import json

DEBUG: bool = False
# DEBUG: bool = True # toggle
TIMEOUT: int = 120_000 # 120 sec
URL: str = 'https://processo.stj.jus.br/SCON/'
DOCS_PER_PAGE = 50

# Termos de pesquisa
#pesquisa modelo 1 (deles)
# CRITERIO_DE_PESQUISA_CONTEUDO: str = 'juros e mora e fazenda pública e correção e monetária'
# DATA_DE_JULGAMENTO_INICIAL_CONTEUDO: str = '01/10/2020'
# DATA_DE_JULGAMENTO_FINAL_CONTEUDO: str = '01/10/2025'

#pesquisa modelo 2 (minha)
PESQUISA: str = 'pericia'
DATA_DE_JULGAMENTO_INICIAL: str = '01/10/2025'
DATA_DE_JULGAMENTO_FINAL: str = '09/10/2025'

PESQUISA: str = ''
DATA_DE_JULGAMENTO_INICIAL: str = ''
DATA_DE_JULGAMENTO_FINAL: str = ''

#pesquisa modelo 2 (minha) (from json)
file = open("pesquisa.json", "r")
from_file = json.load(file)
PESQUISA: str = from_file["PESQUISA"]
DATA_DE_JULGAMENTO_INICIAL: str = from_file["DATA_DE_JULGAMENTO_INICIAL"]
DATA_DE_JULGAMENTO_FINAL: str = from_file["DATA_DE_JULGAMENTO_FINAL"]


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
