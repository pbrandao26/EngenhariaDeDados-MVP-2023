# -*- coding: utf-8 -*-
"""
Created on Sun Sep 10 21:43:21 2023

@author: pedro
"""

import openpyxl
import os

def xlsx_to_tsv(xlsx_file, save_directory):
    # Carregar a planilha
    wb = openpyxl.load_workbook(xlsx_file)
    ws = wb.active

    # Definir o nome e o caminho do arquivo .tsv
    tsv_filename = os.path.basename(xlsx_file).replace('.xlsx', '.tsv')
    tsv_file = os.path.join(save_directory, tsv_filename)

    # Escrever os dados no arquivo .tsv
    with open(tsv_file, 'w', encoding='utf-8') as f:
        for row in ws.iter_rows():
            f.write('\t'.join([str(cell.value) if cell.value is not None else '' for cell in row]))
            f.write('\n')

    print(f"Arquivo .tsv salvo em {tsv_file}")

xlsx_to_tsv('C:\\Users\\pedro\\.spyder-py3\\transfer_data.xlsx' , 'C:\\Users\\pedro\\OneDrive\\Área de Trabalho\\MVP_Futebol')
xlsx_to_tsv('C:\\Users\\pedro\\.spyder-py3\\Allplayers_stats.xlsx' , 'C:\\Users\\pedro\\OneDrive\\Área de Trabalho\\MVP_Futebol')