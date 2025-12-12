# Web Scraping de Jurisprudências no site do STJ

Este script baixa automaticamente acórdãos e decisões monocráticas do STJ:

[https://processo.stj.jus.br/SCON/](https://processo.stj.jus.br/SCON/)

Todos os comandos demonstrados nesta página devem ser usados na pasta contendo o script.

## Como usar este script

Existe um arquivo chamado `pesquisa.json` na pasta raiz do projeto. Editar o conteúdo deste arquivo para mudar a pesquisa desejada.

### Buscar Acórdãos da 1ª aba

```sh
uv run main.py a 1
```

### Buscar Acórdãos da 2ª aba

```sh
uv run main.py a 2
```

### Buscar Decisões Monocráticas

```sh
uv run main.py d m
```

Para decisões monocráticas, que tendem a ser numerosas, limitar a pesquisa para datas próximas.

O site em questão atrasa cada navegação de página, tornando o script inviável, e até não terminável em buscas com mais de centenas de resultados. O limite está por volta de 1000 resultados.

### Ativando o modo Debug

```sh
uv run main.py a 1 --debug
```

```sh
uv run main.py a 2 --debug
```

```sh
uv run main.py d m --debug
```

## Pré-requisitos

Este script usa [uv](https://docs.astral.sh/uv/) como gerenciador de dependências.
Seguir a documentação de como [Instalar](https://docs.astral.sh/uv/getting-started/installation/) este programa para poder rodar o script.

## Instalando as dependências do projeto

```sh
uv sync
```

## Instalando os navegadores necessários

```sh
uv run playwright install
uv run playwright install-deps
```

## Ativando o ambiente virtual (opcional)

Pode resolver problemas específicos de execução. Como instalar os navegadores no lugar correto

### Linux, WSL (Windows Subsystem for Linux) e Git Bash

```sh
source .venv/bin/activate
```

### Windows (Powershell)

```sh
.venv\Scripts\activate
```

## Rodando o script

```sh
uv run python script.py
```

## Instalando dependências de desenvolvimento

Necessário para rodar testes com Pytest. Não é necessário ser feito pelo usuário do script.

```sh
uv sync --extra dev
```
