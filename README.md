# EngenhariaDeDados-MVP-2023
Repositório destinado aos meus arquivos do MVP de Engenharia de Dados, da pós de Data Science &amp; Analyticis pela PUC-Rio. 

# 1 - Objetivo e Perguntas
Tema Central: A dinâmica do mercado de transferências das cinco principais ligas de futebol europeu: Premiere League, La Liga, Serie A TIM, Ligue 1 e Bunesliga.

Objetivo: Explorar e analisar a relação entre diversas características dos jogadores e dos jogos (tais como idade, liga, temporada, gols, assistências, entre outros) com os valores de transferência associados a cada jogador. Ao longo do projeto, embora tenhamos começado com algumas perguntas-chave, novos questionamentos e insights surgiram..

Perguntas Iniciais:

1- Impacto da Idade: De que forma a idade dos jogadores influencia seus valores de transferência?

2- Influência da Liga: Há uma relação evidente entre a liga em que o jogador atua e seu valor de transferência? Como essa relação se perpetua ao longo dos anos?

3- Variação por Posição: Os valores de transferência variam conforme a posição do jogador?

4- Performance e Valorização: Qual é o impacto das métricas de desempenho (como gols, assistências, partidas jogadas e comportamento disciplinar) nos valores de transferência?

5- Tendências Temporais: Existem tendências notáveis no mercado de transferências ao longo do tempo? Por exemplo, há um aumento nos valores durante eventos como a Copa do Mundo?

# 2 - Detalhamento e coleta:
O trabalho utiliza duas bases de dados principais:

1- Base de dados do mercado de transferências ([www.transfermkt.com](https://www.transfermarkt.com.br/)): 

No site transfermkt coletamos os dados de todas as transferêncas (entradas e saídas) de todos os clubes das 5 principais divisões europeias entre os anos de 1999 e 2023. Através dessa base de dados foi possível obter dados descritivos de fluxo de entrada e saída de jogadores das ligas e dos clubes, e também os valores de cada transferência.

2- Base de dados de desempenho dos jogadores (https://fbref.com/pt/):

No site fbref coletamos todas as principais estatisticas de desempenho dos jogadores que passaram por todos os clubes das 5 principais divisões europeias entre os anos de 1999 e 2023. Através dessa base de dados foi possível obter as métricas de desempenho e performance dos jogadores.

- Coleta:

A coleta dos dados presentes nos sites expostos foi realizada através de um script de webscraping, usando majoritariamente as bibliotecas pandas, bs4 e selenium. Os dados foram armazenados em um arquivo .xslx e posteriormente convertido para .tsv, também através de um script em python. Os scripts se encontram na pasta <> presente neste repositório.
