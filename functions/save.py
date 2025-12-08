import os
import csv
import shutil
import pandas as pd
from rich import print


def salvar_dados_da_pagina_atual_em_csv(numero_da_pagina, dados):
    """
    Salva os dados coletados da página atual em formato CSV para uso posterior.

    Args:
        numero_da_pagina: O número da página atual. Usado para sequenciar os arquivos.
        dados: Lista com os dados coletados na página.
    """
    os.makedirs("dados_csv", exist_ok=True)
    with open(f'dados_csv/pagina{numero_da_pagina}.csv', 'w', encoding="utf-8", newline='') as csv_file:
        # fieldnames = ['emp_name', 'dept', 'birth_month']
        fieldnames = [
            "processo"
            , "tipo_de_recurso"
            , "ministro_relator"
            , "orgao_julgador"
            , "data_do_julgamento"
            , "data_da_publicacao_fonte"
            , "tese_juridica"
            , "url_do_acordao"
            , "ementa"
            , "acordao"
            # , "notas"
            # , "referencia_legislativa"
            # , "jurisprudencia_citada"
        ]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        print(f"Salvando resultado da página atual. (dados_csv/pagina{numero_da_pagina}.csv)")
        writer.writeheader()
        for linha in dados:
            writer.writerow(linha)


def juntar_dados_de_cada_pagina():
    """
    Junta os dados de cada página (contidos em arquivos `.csv`).
    """
    print("juntando os dados de todas as páginas.")

    # Assuming your CSV files are in a folder named 'csv_files'
    csv_folder_path = 'dados_csv'
    all_files = [os.path.join(csv_folder_path, f) for f in os.listdir(csv_folder_path) if f.endswith('.csv')]

    # Read each CSV into a DataFrame and store in a list
    df_list = []
    for file in all_files:
        df_list.append(pd.read_csv(file))

    # Concatenate all DataFrames in the list
    combined_df = pd.concat(df_list, ignore_index=True)

    # Save the combined DataFrame to a new CSV file
    combined_df.to_csv('combined_output.csv', index=False)

    # Deleta os arquivos intermediários de dados
    folder_path = "dados_csv"
    if os.path.exists(folder_path):
        try:
            shutil.rmtree(folder_path)
            print(f"Folder '{folder_path}' and its contents deleted successfully.")
        except OSError as e:
            print(f"Error: {folder_path} : {e.strerror}")
    else:
        print(f"Folder '{folder_path}' does not exist.")
