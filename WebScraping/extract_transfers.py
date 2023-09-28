# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 00:31:34 2023

@author: pedro
"""

from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup as bs
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from collections import OrderedDict
from selenium.common.exceptions import NoSuchElementException, TimeoutException

#Definindo a função extract

def extract_transfer_data(browser, URL):
    try:
        
        browser.get(URL)
        html = browser.page_source
        soup = bs(html, 'html.parser')
        time.sleep(2)
        
        try:

            iframes = browser.find_elements(By.XPATH,"/html/body/div[3]/iframe")
            if len(iframes) > 0:
                browser.switch_to.frame(iframes[0])
                browser.find_element(By.XPATH,'/html/body/div/div[2]/div[3]/div[3]/button').click()
                browser.switch_to.default_content()
                
        except NoSuchElementException:
            print("Iframe or button not found.")
            
        time.sleep(2)    
        club_names = soup.find_all("div", {"class": "box"})[1] 
        tabelas = soup.find_all("div", {"class": "responsive-table"})
    
        # Encontrar todas as ocorrências de 'title' dentro da tag
        club_names_list = club_names.find_all(attrs={"title": True})
    
        # Extrair os nomes dos times dos atributos 'title' e criar uma lista
        names_list = list(OrderedDict.fromkeys([tag["title"] for tag in club_names_list]))
    
        # Criar uma lista vazia para armazenar os dados dos jogadores
        player_data = []
    
        # Iterar através das tabelas e dos nomes dos times
        for i in range(0, len(tabelas), 2):
            tabela_entrada = tabelas[i]
            tabela_saida = tabelas[i+1]
            time_nome = names_list[i // 2]
            
            # Tabela de Entrada
            rows_entrada = tabela_entrada.find_all("tr")
            for row in rows_entrada:
                columns = row.find_all("td")
                if columns:
                    nome_jogador_elem = columns[0].find("a")
                    if nome_jogador_elem:
                        nome_jogador = nome_jogador_elem.text.strip()
                    else:
                        nome_jogador = columns[0].text.strip()
                    
                    idade = columns[1].text.strip()
                    nacionalidade = columns[2].find("img")["title"]
                    posicao = columns[3].text.strip()
                    valor_mercado = columns[5].text.strip()
                    origem_clube = columns[6].find("img")["title"]
                    quantia_paga = columns[8].text.strip()
                    
                    player_data.append([time_nome, nome_jogador, idade, nacionalidade, posicao, valor_mercado, origem_clube, quantia_paga, "Entrada"])
            
            # Tabela de Saída
            rows_saida = tabela_saida.find_all("tr")
            for row in rows_saida:
                columns = row.find_all("td")
                if columns and "transfer-zusatzinfo-box" not in row.get("class", []):
                    nome_jogador_elem = columns[0].find("a")
                    if nome_jogador_elem:
                        nome_jogador = nome_jogador_elem.text.strip()
                    else:
                        nome_jogador = columns[0].text.strip()
                    
                    idade = columns[1].text.strip()
                    nacionalidade = columns[2].find("img")["title"]
                    posicao = columns[3].text.strip()
                    valor_mercado = columns[5].text.strip()
                    origem_clube = columns[6].find("img")["title"]
                    quantia_paga = columns[8].text.strip()
                    
                    player_data.append([time_nome, nome_jogador, idade, nacionalidade, posicao, valor_mercado, origem_clube, quantia_paga, "Saída"])
                    
                    columns = ["Time", "Nome", "Idade", "Nacionalidade", "Posição", "Valor de Mercado", "Origem", "Quantia Paga", "Tipo Transferência"]
        df = pd.DataFrame(player_data, columns=columns)

    except TimeoutException:
        print(f"Timeout reached for URL: {URL}")
    except Exception as e:
        print(f"Ocorreu um erro: {str(e)}")
        df = None
    return df

def extract_league_data(browser, country,base_url, years):
    """Extract data for a given league across multiple years."""
    dataframes = {}
    for year in years:
        full_url = base_url.format(year)
        df = extract_transfer_data(browser, full_url)
        if df is not None:
            df['Liga'] = country
            df['Ano'] = str(year)
            dataframes[f'df_{country}_{year}'] = df
        else:
            print(f"Falha na extração de dados da liga {country} no ano {year}.")
        
    return dataframes

#Definindo função convert

def convert_to_actual_value(value_str):
    # Se o valor não contém "€" ou tem "Valor de empréstimo:", retorne o valor original
    if "€" not in value_str or "Valor de empréstimo:" in value_str:
        return value_str
    
    # Limpa a string removendo espaços
    value_str = value_str.strip()

    # Se a string representa "custo zero" ou "Empréstimo", retorna 0 ou mantém "Empréstimo" respectivamente
    if value_str == "custo zero":
        return 0.0
    elif value_str == "Empréstimo":
        return value_str
    
    # Substitui a vírgula por ponto
    value_str = value_str.replace(",", ".")

    # Se contém "mi", multiplica por 1 milhão; se contém "mil", multiplica por 1 mil
    multiplier = 1
    if "mi. €" in value_str:
        multiplier = 1_000_000
        value_str = value_str.replace("mi. €", "")
    elif "mil €" in value_str:
        multiplier = 1_000
        value_str = value_str.replace("mil €", "")
        
    # Converte a string restante para float e multiplica pelo multiplicador
    try:
        return float(value_str) * multiplier
    except ValueError:
        return None

    
# Define URLs for each league
league_urls = {
    'Premier-League': 'https://www.transfermarkt.com.br/premier-league/transfers/wettbewerb/GB1/plus/?saison_id={}&s_w=&leihe=1&intern=0&intern=1',
    'La-Liga': 'https://www.transfermarkt.com.br/laliga/transfers/wettbewerb/ES1/plus/?saison_id={}&s_w=&leihe=1&intern=0&intern=1',
    'Bundesliga': 'https://www.transfermarkt.com.br/bundesliga/transfers/wettbewerb/L1/plus/?saison_id={}&s_w=&leihe=1&intern=0&intern=1',
    'Serie-A': 'https://www.transfermarkt.com.br/serie-a/transfers/wettbewerb/IT1/plus/?saison_id={}&s_w=&leihe=3&intern=0&intern=1',
    'Ligue-1': 'https://www.transfermarkt.com.br/ligue-1/transfers/wettbewerb/FR1/plus/?saison_id={}&s_w=&leihe=1&intern=0&intern=1'
}

# Iniciar o navegador uma vez aqui
browser = webdriver.Chrome()
browser.maximize_window()

years_sample = [2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015, 
                2014, 2013, 2012, 2011, 2010, 2009, 2008, 2007, 2006,
                2005, 2004, 2003, 2002, 2001, 2000, 1999]

dfs_sample_FR = extract_league_data(browser,'Ligue-1',league_urls['Ligue-1'], years_sample)
dfs_sample_ES = extract_league_data(browser,'La-Liga',league_urls['La-Liga'], years_sample)
dfs_sample_AL = extract_league_data(browser,'Bundesliga',league_urls['Bundesliga'], years_sample)
dfs_sample_IT = extract_league_data(browser,'Serie-A',league_urls['Serie-A'], years_sample)
dfs_sample_PL = extract_league_data(browser,'Premier-League',league_urls['Premier-League'], years_sample)

# Fechar o navegador após concluir todas as extrações
browser.quit()

# Salvando todas as ligas em único dicionário para facilitar a iteração 
all_leagues = {
    'Premier-League': dfs_sample_PL,
    'La-Liga': dfs_sample_ES,
    'Bundesliga': dfs_sample_AL,
    'Serie-A': dfs_sample_IT,
    'Ligue-1': dfs_sample_FR
}

# Create an empty list to store all dataframes
all_dfs = []

# Iterate over each league
for league, dfs in all_leagues.items():
    # Iterate over each year/dataframe
    for key, df in dfs.items():
        
        # Applying the conversion function to the columns 'Valor de Mercado' and 'Quantia Paga'
        df['Valor de Mercado'] = df['Valor de Mercado'].apply(convert_to_actual_value)
        df['Quantia Paga'] = df['Quantia Paga'].apply(convert_to_actual_value)
        
        # Append the dataframe to the list
        all_dfs.append(df)

# Concatenate all dataframes vertically
final_df = pd.concat(all_dfs, ignore_index=True)

# Save the combined dataframe to an Excel file in a single sheet
with pd.ExcelWriter('transfer_data.xlsx') as writer:
    final_df.to_excel(writer, sheet_name='All Transfers', index=False)