# Avaliação Prática - Jurimetria no STJ

## Pré-requisitos

Este script usa [uv](https://docs.astral.sh/uv/) como gerenciador de dependências.
Seguir a documentação de como [Instalar](https://docs.astral.sh/uv/getting-started/installation/) este programa para poder rodar o script.

## Instalando as dependências do projeto

```sh
uv pip install --requirements requirements.txt
```

## Instalando os navegadores necessários

```sh
uv run playwright install
uv run playwright install-deps
```

## Rodando o script

```sh
uv run python script.py
```
