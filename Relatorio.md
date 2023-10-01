# 1- Introdução

O presente trabalho é um MVP que tem como tema central o mercado de transferência das cinco principais ligas de futebol europeu: Premier League (Inglaterra), La Liga (Espanha), Serie A TIM (Itália), Ligue 1 (França) e Bundesliga (Alemanha).

O desafio principal do projeto era criar um pipeline de dados utilizando tecnologia em nuvem, passando pelas etapas de busca, coleta, modelagem, carga e análise dos dados. 

Todos os requisitos e objetivos propostos foram cumpridos e serão exibidos e explicados passo a passo neste documento. 

## Objetivo e Perguntas
O objetivo do trabalho foi explorar e analisar a relação entre diversas características dos jogadores e dos jogos (tais como idade, liga, temporada, gols, assistências, entre outros) com os valores de transferência associados a cada jogador. Ao longo do projeto, embora tenhamos começado com algumas perguntas-chave, novos questionamentos e insights surgiram.

**Perguntas Iniciais**:

1- Impacto da Idade: De que forma a idade dos jogadores influencia seus valores de transferência?

2- Influência da Liga: Há uma relação evidente entre a liga em que o jogador atua e seu valor de transferência? Como essa relação se perpetua ao longo dos anos?

3- Variação por Posição: Os valores de transferência variam conforme a posição do jogador?

4- Performance e Valorização: Qual é o impacto das métricas de desempenho (como gols, assistências, partidas jogadas e comportamento disciplinar) nos valores de transferência?

5- Tendências Temporais: Existem tendências notáveis no mercado de transferências ao longo do tempo? Por exemplo, há um aumento nos valores durante eventos como a Copa do Mundo?

# 2- Busca e coleta:

A fim de atender o objetivo do trabalho e responder às perguntas levantadas, foi necessário buscar bases de dados consistentes e confiáveis que tratassem do assunto. Assim, o trabalho utilizou duas bases de dados principais:

**1- Base de dados do mercado de transferências** ([www.transfermkt.com](https://www.transfermarkt.com.br/)): 

Através do site transfermkt, coletamos os dados de todas as transferências (entradas e saídas) de todos os clubes das 5 principais divisões europeias entre os anos de 1999 e 2023. Através dessa base de dados, foi possível obter dados descritivos de fluxo de entrada e saída de jogadores das ligas e dos clubes, e também os valores de cada transferência.

![transfermkt](https://github.com/pbrandao26/EngenhariaDeDados-MVP-2023/assets/145406479/1a84c6ab-e3a8-4245-8ff5-4c7054f19477)

O site transfermkt é uma fonte de dados conhecida mundialmente pela consistência dos dados relacionados ao mercado de transferência do futebol. Entretanto, ele não apresenta uma base de dados tão sólida quando o assunto é dados de performance. Sendo assim, buscamos uma segunda fonte de dados relevante.

**2- Base de dados de desempenho dos jogadores** (https://fbref.com/pt/):

No site fbref, coletamos todas as principais estatísticas de desempenho dos jogadores que passaram por todos os clubes das 5 principais divisões europeias entre os anos de 1999 e 2023. Através dessa base de dados, foi possível obter as métricas de desempenho e performance dos jogadores.

![fbref](https://github.com/pbrandao26/EngenhariaDeDados-MVP-2023/assets/145406479/55ca18a4-c56b-4043-b105-243b1c36134e)

## Coleta dos dados:

Como as bases de dados escolhidas não possuem APIs para obtenção automática, foi necessário criar um robô de scraping para realizar a raspagem de dados das webpages. Foram construídos dois scripts de Python, um para cada base de dados, usando majoritariamente as bibliotecas pandas, bs4 e selenium, para se obter os dados em formato tabular.

Os scripts foram construídos em um ambiente local, na minha própria máquina, e encontram-se disponíveis no diretório [WebScraping](/EngenhariaDeDados-MVP-2023/WebScraping) aqui neste repositório.

Os dados foram armazenados em um arquivo .xslx e posteriormente convertidos para .tsv, também através de um script em Python que se encontra no mesmo diretório dos outros dois mencionados.

Os scripts também fazem alguns tratamentos preliminares que serviram como pré-processamento dos dados antes de jogá-los para a nuvem. Porém, como o intuito era realizar as transformações durante a etapa de ETL, dentro do ambiente de nuvem, essas transformações foram as mais básicas possíveis, como por exemplo: remoção de cabeçalhos repetidos, remoção de colunas multiníveis, formatação de valores monetários, entre outros.

# 3 - Modelagem:
A modelagem escolhida para solucionar o problema em questão e responder às perguntas foi a modelagem estrela. Busquei criar uma estrutura com 3 tabelas de dimensão, sendo elas: dimensão jogador, dimensão liga/ano e dimensão time, e duas tabelas fato, tabela fato transferencias e tabela fato desempenho. 

A opção por essa modelagem é devida ao fato de que a modelagem estrela é especialmente eficaz para lidar com sistemas de suporte à decisão e análises complexas, como as que estavam previstas para este projeto. No contexto do projeto, ao analisar transferências e desempenhos de jogadores, era fundamental ter uma estrutura que permitisse cruzar facilmente diferentes dimensões, como jogadores, ligas e times, com as métricas quantitativas de performance e transferências.
