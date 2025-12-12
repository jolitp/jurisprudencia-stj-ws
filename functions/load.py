import os
import pandas as pd
from rich import print
from icecream import ic


def append_to_timestamp_file(n_pagina: int,
                            start: float,
                            end: float,
                            delta: float,
                            aba: str = "aba_undefined",
                            script_start_datetime=None
                            ):
    ic()

    dir_str = "__execucoes__/no_date"
    if script_start_datetime:
        dir_str = f"__execucoes__/{script_start_datetime.strftime("%Y_%m_%d_-_%H_%M_%S")}"
    os.makedirs(f'{dir_str}/{aba}', exist_ok=True)
    with open(f"{dir_str}/timestamps.txt", "a") as f:
        f.write(f"Página {n_pagina}: {start} -> {end} = {delta}\n")


def salvar_dados_da_pagina_atual_em_csv(numero_da_pagina: int,
                                        dados: list[dict],
                                        header: list,
                                        aba: str = "aba_undefined",
                                        script_start_datetime=None):
    """
    Salva os dados coletados da página atual em formato CSV para uso posterior.

    Args:
        numero_da_pagina: O número da página atual. Usado para sequenciar os arquivos.
        dados: Lista com os dados coletados na página.
        header: lista de strings com os nomes das colunas
        aba: nome da aba relativa ao arquivo sendo salvo
        script_start_datetime: objeto datetime com a adata e hora de início do script

    """
    ic()

    dir_str = "__execucoes__/no_date"
    if script_start_datetime:
        dir_str = f"__execucoes__/{script_start_datetime.strftime("%Y_%m_%d_-_%H_%M_%S")}"
    os.makedirs(dir_str, exist_ok=True)
    df = pd.DataFrame(dados, columns=header)
    df.sort_values(by=['Índice'])

    print(f"Dados da página {numero_da_pagina}")
    print(f"Colunas encontradas nesta página:\n {list(df.columns)}")

    os.makedirs(f'{dir_str}/{aba}/csv/', exist_ok=True)
    path = f'{dir_str}/{aba}/csv/pagina_{numero_da_pagina}.csv'
    df.to_csv(path, index=False)


def juntar_dados_de_cada_pagina(aba: str = "acordaos_1",
                                script_start_datetime=None):
    """
    Junta os dados de cada página (contidos em arquivos `.csv`).
    """
    ic()

    print("juntando os dados de todas as páginas.")

    # TODO: acomodar arquivos de abas diferentes em pastas diverentes ao juntar dados
    dir_str = "__execucoes__/no_date"
    if script_start_datetime:
        dir_str = f"__execucoes__/{script_start_datetime.strftime("%Y_%m_%d_-_%H_%M_%S")}"
    csv_path = f'{dir_str}/{aba}/csv'
    csv_filename = f"{aba} output.csv"
    final_csv_folder_path = f"{dir_str}/csv"
    os.makedirs(final_csv_folder_path, exist_ok=True)
    all_parcial_csv = [os.path.join(csv_path, f) for f in os.listdir(csv_path) if f.endswith('.csv')]
    all_files = all_parcial_csv

    df_list = []
    for file in all_files:
        df_list.append(pd.read_csv(file))

    combined_df = pd.concat(df_list, ignore_index=True)
    combined_df.sort_values(by=['Índice'])
    combined_df.to_csv(f'{dir_str}/csv/{csv_filename}', index=False)


# def juntar_dados_de_cada_aba(script_start_datetime=None):
#     """
#     Junta os dados de cada página (contidos em arquivos `.csv`).
#     """
#     print("juntando os dados de todas as páginas.")

#     # TODO: acomodar arquivos de abas diferentes em pastas diverentes ao juntar dados
#     # Assuming your CSV files are in a folder named 'csv_files'
#     dir_str = "__execucoes__/no_date"
#     if script_start_datetime:
#         dir_str = f"__execucoes__/{script_start_datetime.strftime("%Y_%m_%d_-_%H_%M_%S")}"
#     csv_path = f'{dir_str}/csv'
#     final_csv_folder_path = f"{dir_str}/csv"
#     os.makedirs(final_csv_folder_path, exist_ok=True)
#     all_acordaos_1 = [os.path.join(csv_path, f) for f in os.listdir(csv_path) if f.endswith('.csv')]
#     # all_files = [os.path.join(csv_folder_path, f) for f in os.listdir(csv_folder_path) if f.endswith('.csv')]
#     all_files = all_acordaos_1

#     # Read each CSV into a DataFrame and store in a list
#     df_list = []
#     for file in all_files:
#         df_list.append(pd.read_csv(file))

#     # Concatenate all DataFrames in the list
#     combined_df = pd.concat(df_list, ignore_index=True)
#     combined_df.sort_values(by=['Índice'])

#     # Save the combined DataFrame to a new CSV file
#     combined_df.to_csv(f'{dir_str}/csv/__output__.csv', index=False)

