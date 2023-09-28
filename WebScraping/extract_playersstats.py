# -*- coding: utf-8 -*-
"""
Created on Sun Sep 10 18:31:49 2023

@author: pedro
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

# Função para obter o DataFrame de uma URL específica
def get_dataframe_from_url(url):
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table_container = soup.find('div', id='div_stats_standard')
    table = table_container.find('table', id='stats_standard')
    df = pd.read_html(str(table))[0]

    # Removendo o multi nivel
    df.columns = df.columns.droplevel(0)
    
    # Removendo cabeçalhos repetidos
    df = df[df['Rk'] != 'Rk']
    
    # Processando a coluna Age
    df['Age'] = df['Age'].str.split('-').str[0]
    
    # Processando a coluna Nation
    df['Nation'] = df['Nation'].str.split().str[-1]
    
    # Processando o DataFrame
    df.set_index('Rk', inplace=True)
    df.drop(columns=['Matches'], inplace=True)
    return df

def rename_duplicated_columns(df):
    cols = pd.Series(df.columns)
    for dup in cols[cols.duplicated()].unique(): 
        cols[cols[cols == dup].index.values.tolist()] = [dup + '_' + str(i) if i != 0 else dup for i in range(sum(cols == dup))]
    df.columns = cols

# Lista de temporadas
seasons = ['1999-2000','2000-2001','2001-2002','2002-2003','2003-2004',
           '2004-2005','2005-2006','2006-2007','2007-2008','2008-2009',
           '2009-2010','2010-2011','2011-2012','2012-2013','2013-2014',
           '2014-2015','2015-2016','2016-2017','2017-2018', 
           '2018-2019','2019-2020','2020-2021','2021-2022', 
           '2022-2023','2023']


# Dicionário com os códigos das ligas e seus nomes
leagues = {
    '9': 'Premier-League',
    '20': 'Bundesliga',
    '12': 'La-Liga',
    '11': 'Serie-A',
    '13': 'Ligue-1'
}

# Inicializando o driver do Selenium
driver = webdriver.Chrome()

# Dicionário para armazenar dataframes por liga e ano
dfs_dict = {league: {} for league in leagues.values()}

# Create an empty list to store all dataframes
all_dfs = []

# Iterando sobre cada temporada e liga
for season in seasons:
    for code, league in leagues.items():
        # Construindo a URL de acordo com a temporada e a liga
        if season == '2023':
            url = f"https://fbref.com/en/comps/{code}/stats/{league}-Stats"
        else:
            url = f"https://fbref.com/en/comps/{code}/{season}/stats/{season}-{league}-Stats"
        print(f"Obtendo dados de {league} da temporada {season}...")

        # Obtenha o DataFrame da URL
        df = get_dataframe_from_url(url)
        df['Liga'] = league
        if season == '2023':
            df['Ano'] = season
        else:
            df['Ano'] = season.split('-')[0]
            
        # Adicionar o dataframe ao dicionário
        dfs_dict[league][season] = df
        
        all_dfs.append(df)
        
# Fechando o navegador
driver.close()

for season in seasons:
    for code, league in leagues.items():
        rename_duplicated_columns(dfs_dict[league][season]) 

# Concatenate all dataframes vertically
final_df = pd.concat(all_dfs, ignore_index=True)


# Save the combined dataframe to an Excel file in a single sheet
with pd.ExcelWriter('Allplayers_stats.xlsx') as writer:
    final_df.to_excel(writer, sheet_name='All Transfers', index=False)
    
print("Processo concluído!")
