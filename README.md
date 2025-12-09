# Avaliação Prática - Jurimetria no STJ

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

## Ativando o ambiente virtual

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

```sh
uv sync --extra dev
```
