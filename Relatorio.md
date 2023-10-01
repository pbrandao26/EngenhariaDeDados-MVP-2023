# 1- Introdução

O presente trabalho é um MVP que tem como tema central o mercado de transferência das cinco principais ligas de futebol europeu: Premier League (Inglaterra), La Liga (Espanha), Serie A TIM (Itália), Ligue 1 (França) e Bundesliga (Alemanha).

O desafio principal do projeto era criar um pipeline de dados utilizando tecnologia em nuvem, passando pelas etapas de busca, coleta, modelagem, carga e análise dos dados.

O processo de escolha da nuvem de ocorreu iterativamente, passando por cada uma das plataformas, encontrando dificuldades e afinidades, que serão posteriormente descritas aqui, e assistindo as aulas onde os professores mostravam o funcionamento de cada nuvem. Por fim, o trabalho foi realizado na Google Cloud Plataform. 

Todos os requisitos e objetivos propostos foram cumpridos e serão exibidos e explicados passo a passo neste documento. 

## 1.1-  Objetivo e Perguntas
O objetivo do trabalho foi explorar e analisar a relação entre diversas características dos jogadores e dos jogos (tais como idade, liga, temporada, gols, assistências, entre outros) com os valores de transferência associados a cada jogador. Ao longo do projeto, embora tenhamos começado com algumas perguntas-chave, novos questionamentos e insights surgiram.

* **Perguntas Iniciais**:

   * 1- Impacto da Idade: De que forma a idade dos jogadores influencia seus valores de transferência?

   * 2- Influência da Liga: Há uma relação evidente entre a liga em que o jogador atua e seu valor de transferência? Como essa relação se perpetua ao longo dos anos?

   * 3- Variação por Posição: Os valores de transferência variam conforme a posição do jogador?

   * 4- Performance e Valorização: Qual é o impacto das métricas de desempenho (como gols, assistências, partidas jogadas e comportamento disciplinar) nos valores de transferência?

   * 5- Tendências Temporais: Existem tendências notáveis no mercado de transferências ao longo do tempo? Por exemplo, há um aumento nos valores durante eventos como a Copa do Mundo?

# 2- Busca e coleta:

A fim de atender o objetivo do trabalho e responder às perguntas levantadas, foi necessário buscar bases de dados consistentes e confiáveis que tratassem do assunto. Assim, o trabalho utilizou duas bases de dados principais:

* **Base de dados do mercado de transferências** ([www.transfermkt.com](https://www.transfermarkt.com.br/)): 

Através do site transfermkt, coletamos os dados de todas as transferências (entradas e saídas) de todos os clubes das 5 principais divisões europeias entre os anos de 1999 e 2023. Através dessa base de dados, foi possível obter dados descritivos de fluxo de entrada e saída de jogadores das ligas e dos clubes, e também os valores de cada transferência.

![transfermkt](https://github.com/pbrandao26/EngenhariaDeDados-MVP-2023/assets/145406479/1a84c6ab-e3a8-4245-8ff5-4c7054f19477)

O site transfermkt é uma fonte de dados conhecida mundialmente pela consistência dos dados relacionados ao mercado de transferência do futebol. Entretanto, ele não apresenta uma base de dados tão sólida quando o assunto é dados de performance. Sendo assim, buscamos uma segunda fonte de dados relevante.

* **Base de dados de desempenho dos jogadores** (https://fbref.com/pt/):

No site fbref, coletamos todas as principais estatísticas de desempenho dos jogadores que passaram por todos os clubes das 5 principais divisões europeias entre os anos de 1999 e 2023. Através dessa base de dados, foi possível obter as métricas de desempenho e performance dos jogadores.

![fbref](https://github.com/pbrandao26/EngenhariaDeDados-MVP-2023/assets/145406479/55ca18a4-c56b-4043-b105-243b1c36134e)

## 2.1 - Coleta dos dados:

Como as bases de dados escolhidas não possuem APIs para obtenção automática, foi necessário criar um robô de scraping para realizar a raspagem de dados das webpages. Foram construídos dois scripts de Python, um para cada base de dados, usando majoritariamente as bibliotecas pandas, bs4 e selenium, para se obter os dados em formato tabular.

Os scripts foram construídos em um ambiente local, na minha própria máquina, e encontram-se disponíveis no diretório [WebScraping](WebScraping) aqui neste repositório. 

* A imagem a seguir, exemplifica o processo para o caso de obtenção dos dados de transferência:

![MVP PYTHON_extraindo players](https://github.com/pbrandao26/EngenhariaDeDados-MVP-2023/assets/145406479/433ebc05-71dc-49ca-878a-e7f894a5efb9)

É possível observar que os dados de alguns anos para algumas ligas não puderam ser obtidos devido a falhas de compreensão da estrutura da webpage transfermkt, entretanto foram poucos os casos em que este incidente ocorreu e estão exibidos na imagem.

* A imagem a seguir, exemplifica o processo para o caso de obtenção dos dados de performance dos jogadores:

![MVP PYTHON](https://github.com/pbrandao26/EngenhariaDeDados-MVP-2023/assets/145406479/fa9a9c0b-5b97-4fff-a230-b3abf62caf1d)

Não foram encontrados erros no processo de obtenção e coleta dos dados. Entranto, o site fbref só passou a fornecer algumas estatisticas avançadas, como gols esperados, assistências esperadas, passes de progressão, jogadas de progressão, entre outras, a partir de 2017, então os dados coletados entre 1999 e 2017 não apresentam estas estatisticas.

Os dados foram armazenados em um arquivo .xslx e posteriormente convertidos para .tsv, também através de um script em Python que se encontra no mesmo diretório dos outros dois mencionados.

* Por fim, a imagem a seguir, mostra o processo para conversão dos dados de .xlsx para .tsv

![MVP PYTHON_xlsx-to-tsv](https://github.com/pbrandao26/EngenhariaDeDados-MVP-2023/assets/145406479/35b75ee7-128b-4aee-a334-1574c12baad4)

Os scripts também fazem alguns tratamentos preliminares que serviram como pré-processamento dos dados antes de jogá-los para a nuvem. Porém, como o intuito era realizar as transformações durante a etapa de ETL, dentro do ambiente de nuvem, essas transformações foram as mais básicas possíveis, como por exemplo: remoção de cabeçalhos repetidos, remoção de colunas multiníveis, formatação de valores monetários, entre outros.

Por fim, é importante mencionar que os arquivos .tsv citados também se encontram na pasta [WebScraping](WebScraping).

# 3- Modelagem:
A modelagem escolhida para atender o objetivo em questão e responder às perguntas foi a modelagem estrela. Busquei criar uma estrutura com 3 tabelas de dimensão, sendo elas: dimensão jogador, dimensão liga/ano e dimensão time, e duas tabelas fato, tabela fato transferencias e tabela fato desempenho. 

A opção por essa modelagem é devida ao fato de que a modelagem estrela é especialmente eficaz para lidar com sistemas de suporte à decisão e análises complexas, como as que estavam previstas para este projeto. No contexto do projeto, ao analisar transferências e desempenhos de jogadores, era fundamental ter uma estrutura que permitisse cruzar facilmente diferentes dimensões, como jogadores, ligas e times, com as métricas quantitativas de performance e transferências.

Sendo assim, o modelo final atendeu ao seguinte formato:

![mermaid-diagram-2023-09-29-045403](https://github.com/pbrandao26/EngenhariaDeDados-MVP-2023/assets/145406479/b9b11319-7e92-46c8-91c1-6f0e32366483)

É importante frisar que os sufixos _PK e _FK não fazem parte dos identificadores destas colunas, são apenas indicadores ilustrativos que coloquei para identificar quais as chaves primárias e estrangeiras das relações.

Toda parte de catalogação e perfil dos dados foi realizada através da ferramenta Google Cloud Dataplex. Este processo será melhor explicado mais a frente.

De maneira geral, os dados foram descritos da seguinte forma:

* dim_jogador:
  
  ID_Jogador (Chave Primária): Um identificador único para cada jogador.

  Jogador: Nome completo do jogador.

  Nacionalidade: País de origem do jogador.

  Pos: Posição em que o jogador atua no campo (por exemplo, atacante, meia, zagueiro, etc.).

  Nascimento: Ano de nascimento do jogador.

* dim_liga_ano:
  
  ID_LigaAno (Chave Primária): Um identificador único para cada combinação de liga e ano.
  
  Liga: Nome da liga de futebol.
  
  Ano: Ano específico associado à liga.

* dim_time:

  ID_Time (Chave Primária): Um identificador único para cada time.
  
  Time_completo: Nome completo do time.
  
  Time: Nome abreviado ou mais comumente usado para se referir ao time.

* fato_transferencia:

  ID_Transferencia (Chave Primária): Um identificador único para cada registro de transferência.
  
  ID_Jogador (Chave Estrangeira): Referência ao jogador associado a esta transferência.
  Ela se relaciona com a chave primária de dim_jogador
  
  ID_Time_Origem_ou_Destino (Chave Estrangeira): Identifica o time de origem ou destino na transferência.
  Ela se relaciona com a chave primária de dim_time
  
  ID_Time_Ref (Chave Estrangeira): Identifica o time de referência na transferência, para entender se é um time de origem ou destino, dependendo do resultado na coluna "Tipo_de_transferencia".
  Ela se relaciona com a chave primária de dim_time
  
  ID_LigaAno (Chave Estrangeira): Identificador da liga e ano associados à transferência.
  Ela se relaciona com a chave primária de dim_liga_ano
  
  Valor_de_mercado: Valor de mercado do jogador no mês da extração dos dados.
  
  Quantia_Paga_ou_Recebida: Quantia paga ou recebida na transferência.
  
  Tipo_de_transferencia: Indica o tipo de transferência (por exemplo, entrada, saída).
  
  Contrato: Aquisição (compra) ou empréstimo do jogador.

* fato_desempenho:
  
  ID_Desempenho (Chave Primária): Um identificador único para cada registro de desempenho.
  
  ID_Jogador (Chave Estrangeira): Referência ao jogador associado a este desempenho.
  Ela se relaciona com a chavr primária de dim_jogador
  
  ID_Time (Chave Estrangeira): Identificador do time ao qual o jogador pertence durante este período de desempenho.
  Ela se relaciona com a chave primária de dim_time
  
  ID_LigaAno (Chave Estrangeira): Identificador da liga e ano em que o jogador atuou.
  Ela se relaciona com a chave primaria de dim_liga_ano.
  
  Idade: Idade do jogador na temporada em questão.
  
  Partidas: Número total de partidas que o jogador disputou durante a temporada.
  
  Partidas_iniciadas: Número total de partidas que o jogador começou jogando, sem considerar as vezes que entrou como substituto.
  
  Minutos_jogados: Total de minutos que o jogador esteve em campo durante a temporada.
  
  90_minutos_jogados: Representa quantas vezes o jogador completou o jogo inteiro (90 minutos).
  
  Gols: Total de gols marcados pelo jogador durante a temporada.
  
  Assistencias: Total de assistências realizadas pelo jogador, ou seja, passes que resultaram diretamente em gols.
  
  Gols_e_assistencias: Combinação do total de gols e assistências do jogador.
  
  Gols_sem_penaltis: Número de gols marcados pelo jogador excluindo gols de pênalti.
  
  Gols_de_penaltis: Total de gols que o jogador marcou a partir de cobranças de pênalti.
  
  Cobrancas_de_penaltis: Número total de cobranças de pênalti realizadas pelo jogador, independentemente de terem sido convertidas em gol ou não.
  
  cartoes_amarelos: Total de cartões amarelos recebidos pelo jogador durante a temporada.
  
  Cartoes_vermelhos: Total de cartões vermelhos recebidos pelo jogador.
  
  Progressao_jogadas: Métrica que quantifica a capacidade do jogador de avançar com a bola pelo campo, geralmente em situações de contra-ataque ou driblando adversários.
  
  Progressao_passes: Quantifica a capacidade do jogador de avançar a bola por meio de passes, seja em profundidade ou mudança de lado.
  
  Desarmes_de_progressao: Representa a quantidade de vezes que o jogador interrompeu uma jogada adversária, evitando sua progressão no campo.
  
  Gols_por_Jogo: Média de gols marcados pelo jogador por jogo.
  
  Min_para_participar: Média de minutos que o jogador precisa jogar para participar diretamente de um gol (marcando ou assistindo).

# 4- Processos na Google Cloud Plataform:

Como mencionado no início do relatório, a núvem escolhida foi a Google Cloud Plataform

  

  


