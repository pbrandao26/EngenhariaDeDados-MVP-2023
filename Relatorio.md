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

Como mencionado no início do relatório, a plataforma de nuvem escolhida foi a Google Cloud Platform. Nela, realizamos todas as etapas de ETL do projeto. O fluxograma abaixo mostra, de maneira resumida, todo o pipeline desenvolvido.

![ETL drawio](https://github.com/pbrandao26/EngenhariaDeDados-MVP-2023/assets/145406479/b5ae030a-6627-40c9-9790-f9a9bba28e4f)

## 4.1- Projeto:
O primeiro passo para iniciar o projeto no GCP foi justamente criar o projeto. No console do Google Cloud, criamos o projeto "MVP Futebol", que serviu como o ambiente onde todas as etapas subsequentes foram realizadas.

![image](https://github.com/pbrandao26/EngenhariaDeDados-MVP-2023/assets/145406479/d56c4da8-77f6-4db2-b9a4-6779315bf289)

## 4.2- Bucket:

Inicialmente, criamos um bucket multi-regional no Cloud Storage chamado 'pbrandao-transfer-data'. Dentro dele, foram criadas duas pastas, uma para cada arquivo de dados .tsv. O arquivo 'Allplayers_stats.tsv', que representa os dados de performance dos jogadores, foi armazenado na pasta 'Players Data'. Já o arquivo 'transfer_data.tsv', que representa os dados de transferência dos jogadores, foi armazenado na pasta 'Transfer Data'. A imagem abaixo ilustra a organização do bucket:

![bucket](https://github.com/pbrandao26/EngenhariaDeDados-MVP-2023/assets/145406479/d1ef3b93-cd89-4b78-8aa3-914c05c00e0e)

As imagens abaixo mostra como estão organizados os dois arquivos em suas respectivas pastas dentro do bcuket:

![image](https://github.com/pbrandao26/EngenhariaDeDados-MVP-2023/assets/145406479/4f640966-c3ff-49a4-aaba-55a2a5fc0ded)

![image](https://github.com/pbrandao26/EngenhariaDeDados-MVP-2023/assets/145406479/2e62353a-7f35-4da0-8ef8-bf05187dbe03)

## 4.3- Criação do Dataset no BigQuery:

Nesta etapa, criamos e configuramos o dataset 'pbrandao_mvp_futebol', que recebeu as cinco tabelas mencionadas anteriormente para serem manipuladas no BigQuery.

![image](https://github.com/pbrandao26/EngenhariaDeDados-MVP-2023/assets/145406479/01658ed8-6c22-471c-8495-da07e03bca0b)

## 4.4- ETL:

Conforme apresentado no fluxograma, toda a etapa de ETL foi realizada dentro do ambiente GCP, por meio do próprio editor de código do Google Cloud Shell. Foram elaborados cinco scripts em Python, um para cada tabela. Estes scripts extraíram os dados brutos do bucket, realizaram transformações e tratamentos específicos para cada tabela e, finalmente, carregaram os dados no BigQuery.

Esta etapa foi uma das mais delicadas do projeto. Ao final deste relatório, na seção de autoavaliação, abordarei algumas das dificuldades encontradas nesta fase, bem como as razões para não ter adotado uma ferramenta específica de ETL.

Foi criada uma pasta específica para armazenamento dos scripts mencionados. Inicialmente ela foi criada com o nome "dataflow_projects" pois ela serviria para armazenar os arquivos Python que seriam executados pelo job do Dataflow, o que não ocorreu por devido a alguns problemas que surgiram ao utilizar a ferramenta.

![etl_scripts_gcp](https://github.com/pbrandao26/EngenhariaDeDados-MVP-2023/assets/145406479/3dd4b217-09af-4925-b1c3-141a4eae3756)

A seguir, estão os scripts utilizados para a etapa de ETL realizada no editor de código do próprio Google CLoud Shell

### 4.4.1- dim_jogador:

```python
import pandas as pd
from google.cloud import bigquery, storage
import unicodedata

# Função para normalizar nomes (remove acentos e converte para minúsculas)
def normalize_name(name):
    name = unicodedata.normalize('NFD', name).encode('ascii', 'ignore').decode("utf-8")
    return name.lower()

# Definindo os caminhos dos arquivos no GCS
allplayers_stats_path = "gs://pbrandao-transfer-data/Players Data/Allplayers_stats.tsv"
transfer_data_path = "gs://pbrandao-transfer-data/Transfer Data/transfer_data.tsv"

# Carregando os dados dos arquivos
allplayers_stats_df = pd.read_csv(allplayers_stats_path, sep='\t')
transfer_data_df = pd.read_csv(transfer_data_path, sep='\t')

# Normalizando a coluna de nomes em ambos os DataFrames
allplayers_stats_df['Player'] = allplayers_stats_df['Player'].apply(normalize_name)
transfer_data_df['Nome'] = transfer_data_df['Nome'].apply(normalize_name)

# Junção dos conjuntos de dados
merged_df = pd.merge(allplayers_stats_df, transfer_data_df, left_on="Player", right_on="Nome", how="inner")

# Criando a tabela dim_jogador
dim_jogador = merged_df[["Player", "Nacionalidade", "Posição", "Born"]].copy()
dim_jogador['ID_Jogador'] = range(1, len(dim_jogador) + 1)
dim_jogador = dim_jogador[["ID_Jogador", "Player", "Nacionalidade", "Posição", "Born"]]
dim_jogador.columns = ["ID_Jogador", "Jogador", "Nacionalidade", "Posição", "Nascimento"]
dim_jogador = dim_jogador.drop_duplicates(subset="Jogador", keep="first").reset_index(drop=True)

# Convertendo colunas específicas para o formato string
string_columns = ["Jogador", "Nacionalidade", "Posição", "Nascimento"]
for column in string_columns:
    dim_jogador[column] = dim_jogador[column].astype(str)

dim_jogador.rename(columns={'Posição': 'Pos'}, inplace=True)

print(dim_jogador)

# Configuração do BigQuery
project_id = "mvp-futebol-398700"
dataset_id = "pbrandao_mvp_futebol"
table_id = "dim_jogador"
full_table_id = f"{project_id}.{dataset_id}.{table_id}"

# Esquema para a tabela dim_jogador
schema = [
    bigquery.SchemaField("ID_Jogador", "INT64", mode="REQUIRED"),
    bigquery.SchemaField("Jogador", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("Nacionalidade", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("Pos", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("Nascimento", "STRING", mode="NULLABLE")
]

# Inicializando o cliente do BigQuery
client = bigquery.Client(project=project_id)

# Carregando o DataFrame no BigQuery com esquema definido
job_config = bigquery.LoadJobConfig(schema=schema)
job = client.load_table_from_dataframe(dim_jogador, full_table_id, job_config=job_config)
job.result()  # Espera até a conclusão do job
```
Dado que estamos lidando com duas bases de dados distintas e independentes, enfrentamos o desafio de normalização dos nomes dos jogadores. Em ambas as bases de dados, os nomes dos jogadores poderiam diferir devido a vários fatores, como a presença de acentos, uso de letras maiúsculas/minúsculas, e outras variações ortográficas. Para garantir uma integração precisa e não perder dados, foi crucial padronizar ou "normalizar" esses nomes.

A principal finalidade desta tabela é consolidar informações de jogadores que estão presentes em ambas as bases de dados. Utilizamos um método de junção (ou ```.join```) para combinar os dados. Contudo, antes de executar essa junção, normalizamos os nomes dos jogadores, assegurando que diferenças sutis na escrita não resultassem em perda de registros relevantes.

Para cada jogador, atribuímos um ID único, resultando na coluna "ID_Jogador". Esta etapa é fundamental para garantir a integridade referencial e facilitar consultas futuras.

Para maior clareza e prevenção de possíveis erros, algumas colunas foram convertidas explicitamente para o tipo de dados string. Também optamos por renomear a coluna "Posição" para "Pos" para evitar possíveis complicações associadas a caracteres especiais no nome da coluna.

Finalmente, preparamos a configuração para carregar os dados no BigQuery. Definimos o "project_id" e "dataset_id", e especificamos o "table_id" como "dim_jogador". Estabelecemos também um esquema para a tabela no BigQuery, garantindo que cada campo do DataFrame fosse mapeado corretamente para seu tipo de dado correspondente no BigQuery.

 ### 4.4.2- dim_time:

 ```python
import pandas as pd
import unicodedata
from google.cloud import bigquery

# Função de normalização que apenas remove acentos e transforma em minúsculas
def simple_normalize(name):
    name = unicodedata.normalize('NFD', name).encode('ascii', 'ignore').decode("utf-8")
    return name.lower()

# Definindo os caminhos dos arquivos no GCS
allplayers_stats_path = "gs://pbrandao-transfer-data/Players Data/Allplayers_stats.tsv"
transfer_data_path = "gs://pbrandao-transfer-data/Transfer Data/transfer_data.tsv"

# Carregando os dados dos arquivos
allplayers_stats_df = pd.read_csv(allplayers_stats_path, sep='\t')
transfer_data_df = pd.read_csv(transfer_data_path, sep='\t')

# Normalização básica dos nomes dos times
allplayers_stats_df['Squad'] = allplayers_stats_df['Squad'].apply(simple_normalize)
transfer_data_df['Time'] = transfer_data_df['Time'].apply(simple_normalize)
transfer_data_df['Origem'] = transfer_data_df['Origem'].apply(simple_normalize)

manual_mapping = {
        'nurnberg': '1.fc nuremberga',
        "m'gladbach": 'borussia monchengladbach',
        'genoa': 'genova',
        'marseille': 'olympique marselha',
        'rennes': 'stade rennais fc',
        'qpr': 'queens park rangers',
        'koln': '1.fc colonia',
        'gazelec ajaccio': 'gfco ajaccio',
        'wolves': 'wolverhampton wanderers',
        'manchester utd': 'manchester united fc',
        'la coruna':'rc deportivo de corunha',
        'angers':'angers sco',
        'ulm':'ssv ulm 1846',
        'sheffield weds':'sheffield wednesday',
        'sheffield utd':'sheffield united',
        'athletic club':'athletic bilbao',
        'real murcia':'real murcia',
        }


# Nível 1: Correspondência direta
direct_mapping = manual_mapping.copy()
for team in allplayers_stats_df['Squad'].unique():
    if team in transfer_data_df['Time'].unique():
        direct_mapping[team] = team

# Nível 2: Verificar se o nome do time em allplayers_stats_df está contido no nome do time em transfer_data_df
partial_mapping = {}
for team in allplayers_stats_df['Squad'].unique():
    if team not in direct_mapping:  # Ignorar os que já foram mapeados no nível 1
        matching_teams = [full_name for full_name in transfer_data_df['Time'].unique() if team in full_name]
        if matching_teams:
            direct_mapping[team] = matching_teams[0]

# Nível 3: Correspondência usando as primeiras palavras
fw_mapping = {}
for team in allplayers_stats_df['Squad'].unique():
    if team not in direct_mapping:
        # Pega as primeiras palavras do nome do time
        first_words = ' '.join(team.split()[:-1])
        matching_teams = [full_name for full_name in transfer_data_df['Time'].unique() if first_words in full_name]
        
        if matching_teams:
            direct_mapping[team] = matching_teams[0]

# Nível 4: Correspondência usando a última palavra
lw_mapping = {}
for team in allplayers_stats_df['Squad'].unique():
    if team not in direct_mapping:
        # Pega a última palavra do nome do time
        last_word = team.split()[-1]
        matching_teams = [full_name for full_name in transfer_data_df['Time'].unique() if last_word in full_name]
        
        if matching_teams:
            direct_mapping[team] = matching_teams[0]

inverted_mapping = {v: k for k, v in direct_mapping.items()}

for team in transfer_data_df['Origem'].unique():
    if team not in inverted_mapping.keys():
        inverted_mapping[team] = None

mapping = inverted_mapping

# Criando o DataFrame para dim_time
dim_time = pd.DataFrame(list(mapping.items()), columns=['Time_completo', 'Time'])
dim_time['ID_Time'] = range(1, len(dim_time) + 1)

# Configuração do BigQuery
project_id = "mvp-futebol-398700"
dataset_id = "pbrandao_mvp_futebol"
table_id = "dim_time"
full_table_id = f"{project_id}.{dataset_id}.{table_id}"


# Inicializando o cliente do BigQuery
client = bigquery.Client(project=project_id)

# Esquema para a tabela dim_time
schema = [
    bigquery.SchemaField("ID_Time", "INT64", mode="REQUIRED"),
    bigquery.SchemaField("Time_completo", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("Time", "STRING", mode="NULLABLE")
]

# Carregando o DataFrame no BigQuery com esquema definido
job_config = bigquery.LoadJobConfig(schema=schema)
job = client.load_table_from_dataframe(dim_time, full_table_id, job_config=job_config)
job.result()  # Espera até a conclusão do jobb
 ```

Dado que estamos lidando com duas bases de dados, uma complexidade adicional surge quando se trata de mapear nomes de times, já que estes podem ser representados de diferentes maneiras em diferentes fontes de dados.

Para começar, definimos uma função de normalização, ```simple_normalize```, que transforma os nomes dos times para letras minúsculas e remove os acentos. Esta é uma etapa crucial para garantir que estamos comparando os nomes dos times de maneira consistente em ambas as bases de dados.

Após a importação dos dados dos arquivos, aplicamos a função de normalização nos nomes dos times das colunas relevantes. Esta normalização básica serve como uma primeira tentativa de padronizar os nomes.

No entanto, a simples normalização não é suficiente. Alguns clubes têm nomes que são representados de forma significativamente diferente nas duas bases de dados. Para resolver isso, criamos um mapeamento manual, ```manual_mapping```, que mapeia explicitamente certos nomes de equipes de uma representação para outra.

A seguir, implementamos várias estratégias de mapeamento:

* Correspondência Direta: Se um nome de equipe da primeira base de dados corresponde diretamente a um nome na segunda base, nós mapeamos diretamente.
  
* Correspondência Parcial: Se um nome de equipe da primeira base de dados estiver contido em um nome de equipe da segunda base, nós o mapeamos.
  
* Correspondência usando as Primeiras Palavras: Tentamos mapear com base nas primeiras palavras do nome da equipe.
  
* Correspondência usando a Última Palavra: Tentamos mapear com base na última palavra do nome da equipe.

Após aplicar essas estratégias de mapeamento, criamos o DataFrame dim_time que contém os nomes dos times mapeados e um ID único para cada time.

Finalmente, preparamos a configuração para carregar os dados no BigQuery. Definimos o project_id e dataset_id e especificamos o table_id como dim_time. Estabelecemos também um esquema para a tabela no BigQuery, garantindo que cada campo do DataFrame fosse mapeado corretamente para seu tipo de dado correspondente no BigQuery.

Esta abordagem meticulosa garante que os nomes dos times sejam consistentemente representados, independentemente das diferenças nas fontes de dados originais.

### 4.4.3- dim_liga_ano:

```python
import pandas as pd
from google.cloud import bigquery

# Definindo o caminho do arquivo no GCS
allplayers_stats_path = "gs://pbrandao-transfer-data/Players Data/Allplayers_stats.tsv"

# Carregando os dados do arquivo
allplayers_stats_df = pd.read_csv(allplayers_stats_path, sep='\t')

# Criando um DataFrame para dim_liga_ano
dim_liga_ano = allplayers_stats_df[['Liga', 'Ano']].drop_duplicates().reset_index(drop=True)
dim_liga_ano['ID_LigaAno'] = range(1, len(dim_liga_ano) + 1)

# Reordenando as colunas
dim_liga_ano = dim_liga_ano[['ID_LigaAno', 'Liga', 'Ano']]
dim_liga_ano = dim_liga_ano.dropna()

# Configuração do BigQuery
project_id = "mvp-futebol-398700"
dataset_id = "pbrandao_mvp_futebol"
table_id = "dim_liga_ano"
full_table_id = f"{project_id}.{dataset_id}.{table_id}"

# Esquema para a tabela dim_liga_ano
schema = [
    bigquery.SchemaField("ID_LigaAno", "INT64", mode="REQUIRED"),
    bigquery.SchemaField("Liga", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("Ano", "INT64", mode="NULLABLE")
]

# Inicializando o cliente do BigQuery
client = bigquery.Client(project=project_id)

# Carregando o DataFrame no BigQuery com esquema definido
job_config = bigquery.LoadJobConfig(schema=schema)
job = client.load_table_from_dataframe(dim_liga_ano, full_table_id, job_config=job_config)
job.result()  # Espera até a conclusão do job
```

A tabela dim_liga_ano foi criada para consolidar informações sobre as diferentes ligas e anos presentes na base de dados. Esta tabela dimensiona uma combinação única de liga e ano, facilitando consultas futuras e otimizando análises que requerem essa granularidade.

Para construir essa tabela, começamos carregando os dados do arquivo localizado no Google Cloud Storage, especificamente do caminho allplayers_stats_path. Uma vez carregados, extraímos as colunas 'Liga' e 'Ano' e removemos quaisquer duplicatas para garantir que cada combinação de liga e ano seja única.

O próximo passo envolveu a atribuição de um ID único para cada combinação de liga e ano, resultando na coluna "ID_LigaAno".

Após a preparação e ordenação adequada das colunas, garantimos que não existissem valores nulos, pois a presença de tais valores poderia comprometer a integridade dos dados.

Finalmente, preparamos a configuração para carregar os dados no BigQuery. O "project_id" e "dataset_id" foram definidos, e o "table_id" foi especificado como "dim_liga_ano". O esquema para a tabela no BigQuery foi estabelecido, garantindo que cada campo do DataFrame fosse mapeado corretamente para seu tipo de dado correspondente no BigQuery. A tabela foi então carregada no BigQuery e confirmamos sua criação bem sucedida.

### 4.4.4- fato_transferencia:

```python
import pandas as pd
import unicodedata
from google.cloud import bigquery

# Função de normalização que apenas remove acentos e transforma em minúsculas
def simple_normalize(name):
    name = unicodedata.normalize('NFD', name).encode('ascii', 'ignore').decode("utf-8")
    return name.lower()

# Função para determinar o tipo de contrato
def determine_contract_type(value):
    if isinstance(value, float):
        return "Aquisicao"
    elif value == "-":
        return ""
    elif "Emprestimo" in value or "Fim do empréstimo" in value:
        return "Emprestimo"
    else:
        return "Aquisicao"
    
# Função para extrair o valor do empréstimo
def extract_loan_value(value):
    if 'custo zero' in value:
        return 0
    if "Valor de empréstimo:" in value:
        extracted_value = value.split(":")[1].split(" ")[0].replace(',', '.')
        if extracted_value:  
            amount = float(extracted_value)
            if "mi." in value:
                return amount * 1e6
            elif "mil" in value:
                return amount * 1e3
        else:
            return None 
    if "Fim do empréstimo" in value:
        return None  
    return value


# Carregando os dados
transfer_data_df = pd.read_csv("gs://pbrandao-transfer-data/Transfer Data/transfer_data.tsv", sep='\t')

# Normalizando as colunas relevantes
transfer_data_df['Nome'] = transfer_data_df['Nome'].apply(simple_normalize)
transfer_data_df['Time'] = transfer_data_df['Time'].apply(simple_normalize)
transfer_data_df['Origem'] = transfer_data_df['Origem'].apply(simple_normalize)

# Aplicando as funções ao DataFrame
transfer_data_df['Contrato'] = transfer_data_df['Quantia Paga'].apply(determine_contract_type)
transfer_data_df['Quantia Paga'].replace(['Empréstimo', '?', '-', 'draft', float('nan')], '-', inplace=True)
transfer_data_df['Quantia Paga'] = transfer_data_df['Quantia Paga'].apply(extract_loan_value)
transfer_data_df['Quantia Paga'] = pd.to_numeric(transfer_data_df['Quantia Paga'], errors='coerce')

# Renomeando colunas
transfer_data_df.rename(columns={
    'Valor de Mercado': 'Valor_de_mercado',
    'Quantia Paga': 'Quantia_Paga_ou_Recebida',
    'Tipo Transferência': 'Tipo_de_transferencia'
}, inplace=True)

# Inicializando o cliente do BigQuery
project_id = "mvp-futebol-398700"
client = bigquery.Client(project=project_id)

# Carregando as tabelas de dimensão do BigQuery
query_jogador = "SELECT * FROM pbrandao_mvp_futebol.dim_jogador"
dim_jogador = client.query(query_jogador).to_dataframe()

query_time = "SELECT * FROM pbrandao_mvp_futebol.dim_time"
dim_time = client.query(query_time).to_dataframe()

query_liga_ano = "SELECT * FROM pbrandao_mvp_futebol.dim_liga_ano"
dim_liga_ano = client.query(query_liga_ano).to_dataframe()

# Cruzando os IDs
transfer_data_df = transfer_data_df.merge(dim_jogador, left_on='Nome', right_on='Jogador', how='left')
transfer_data_df = transfer_data_df.merge(dim_time, left_on='Origem', right_on='Time_completo', how='left')
transfer_data_df.rename(columns={'ID_Time': 'ID_Time_Origem_ou_Destino'}, inplace=True)
transfer_data_df = transfer_data_df.merge(dim_time, left_on='Time_x', right_on='Time_completo', how='left')
transfer_data_df.rename(columns={'ID_Time': 'ID_Time_Ref'}, inplace=True)
transfer_data_df = transfer_data_df.merge(dim_liga_ano, left_on=['Liga', 'Ano'], right_on=['Liga', 'Ano'], how='left')

# Selecionando as colunas
transferencia = transfer_data_df[[
    'ID_Jogador', 'ID_Time_Origem_ou_Destino', 'ID_Time_Ref', 'ID_LigaAno', 'Valor_de_mercado', 'Quantia_Paga_ou_Recebida', 'Tipo_de_transferencia', 'Contrato'
]].copy()
transferencia['ID_Transferencia'] = range(1, len(transferencia) + 1)
transferencia['Valor_de_mercado'] = pd.to_numeric(transferencia['Valor_de_mercado'], errors='coerce')
transferencia['Quantia_Paga_ou_Recebida'] = pd.to_numeric(transferencia['Quantia_Paga_ou_Recebida'], errors='coerce')

# Reordenando as colunas
transferencia = transferencia[['ID_Transferencia', 'ID_Jogador', 'ID_Time_Origem_ou_Destino', 'ID_Time_Ref', 'ID_LigaAno', 'Valor_de_mercado', 'Quantia_Paga_ou_Recebida', 'Tipo_de_transferencia', 'Contrato']]
transferencia=transferencia.dropna(subset=['ID_Jogador'])

# Configuração da tabela no BigQuery
dataset_id = "pbrandao_mvp_futebol"
table_id = "fato_transferencia"
full_table_id = f"{project_id}.{dataset_id}.{table_id}"

# Esquema para a tabela fato_transferencia
schema = [
    bigquery.SchemaField("ID_Transferencia", "INT64", mode="REQUIRED"),
    bigquery.SchemaField("ID_Jogador", "INT64", mode="REQUIRED"),
    bigquery.SchemaField("ID_Time_Origem_ou_Destino", "INT64", mode="REQUIRED"),
    bigquery.SchemaField("ID_Time_Ref", "INT64", mode="REQUIRED"),
    bigquery.SchemaField("ID_LigaAno", "INT64", mode="REQUIRED"),
    bigquery.SchemaField("Valor_de_mercado", "FLOAT64", mode="NULLABLE"),
    bigquery.SchemaField("Quantia_Paga_ou_Recebida", "FLOAT64", mode="NULLABLE"),
    bigquery.SchemaField("Tipo_de_transferencia", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("Contrato", "STRING", mode="NULLABLE")
]

# Carregando o DataFrame no BigQuery com esquema definido
job_config = bigquery.LoadJobConfig(schema=schema)
job = client.load_table_from_dataframe(transferencia, full_table_id, job_config=job_config)
job.result()  # Espera até a conclusão do job
```

A tabela fato_transferencias é uma das tebelas centrais do no nosso data warehouse, armazenando informações detalhadas sobre as transferências de jogadores. Iniciamos o processo aplicando uma função para normalizar os nomes dos jogadores e dos times. 

Para entender a natureza de cada transferência, implementamos a função ```determine_contract_type```, que categoriza a transação como "Aquisição" ou "Empréstimo" com base nos valores da coluna 'Quantia Paga'. Além disso, utilizamos a função ```extract_loan_value``` para isolar valores específicos associados a empréstimos.

Um aspecto fundamental foi a integração dessa tabela com outras tabelas de dimensão já presentes no BigQuery. Cruzamos os dados para associar os IDs de jogadores, times e ligas/anos à nossa tabela fato_transferencias.

Na etapa final, atribuímos um ID único para cada transferência, assegurando que cada registro seja único. Também fizemos um ajuste nos tipos de dados de valores monetários para garantir precisão nas análises. Com a tabela estruturada, definimos um esquema específico para ela e, por fim, carregamos o DataFrame no BigQuery.

### 4.4.5- fato_desempenho:

```python
import pandas as pd
import unicodedata
from google.cloud import bigquery

# Função de normalização que apenas remove acentos e transforma em minúsculas
def simple_normalize(name):
    name = unicodedata.normalize('NFD', name).encode('ascii', 'ignore').decode("utf-8")
    return name.lower()


# Carregando os dados
allplayers_stats_df = pd.read_csv("gs://pbrandao-transfer-data/Players Data/Allplayers_stats.tsv", sep='\t')

# Normalizando as colunas relevantes
allplayers_stats_df['Squad'] = allplayers_stats_df['Squad'].apply(simple_normalize)
allplayers_stats_df['Player'] = allplayers_stats_df['Player'].apply(simple_normalize)

# Inicializando o cliente do BigQuery
project_id = "mvp-futebol-398700"
client = bigquery.Client(project=project_id)

# Carregando as tabelas de dimensão do BigQuery
query_jogador = "SELECT * FROM pbrandao_mvp_futebol.dim_jogador"
dim_jogador = client.query(query_jogador).to_dataframe()

query_time = "SELECT * FROM pbrandao_mvp_futebol.dim_time"
dim_time = client.query(query_time).to_dataframe()

query_liga_ano = "SELECT * FROM pbrandao_mvp_futebol.dim_liga_ano"
dim_liga_ano = client.query(query_liga_ano).to_dataframe()

# Cruzando os IDs
allplayers_stats_df = allplayers_stats_df.merge(dim_jogador, left_on='Player', right_on='Jogador', how='left')
allplayers_stats_df = allplayers_stats_df.merge(dim_time, left_on='Squad', right_on='Time', how='left')
allplayers_stats_df = allplayers_stats_df.merge(dim_liga_ano, left_on=['Liga', 'Ano'], right_on=['Liga', 'Ano'], how='left')

# Selecionando e renomeando colunas
desempenho = allplayers_stats_df[[
    'ID_Jogador', 'ID_Time', 'ID_LigaAno', 'Age', 'MP', 'Starts', 'Min', '90s', 'Gls', 'Ast', 'G+A', 'G-PK', 'PK', 'PKatt', 'CrdY', 'CrdR', 'PrgC', 'PrgP', 'PrgR'
]].copy()

columns_translation = {
    'Age': 'Idade',
    'MP': 'Partidas',
    'Starts': 'Partidas_iniciadas',
    'Min': 'Minutos_jogados',
    '90s': '90_minutos_jogados',
    'Gls': 'Gols',
    'Ast': 'Assistencias',
    'G+A': 'Gols_e_assistencias',
    'G-PK': 'Gols_sem_penaltis',
    'PK': 'Gols_de_penaltis',
    'PKatt': 'Cobrancas_de_penaltis',
    'CrdY': 'cartoes_amarelos',
    'CrdR': 'Cartoes_vermelhos',
    'PrgC': 'Progressao_jogadas',
    'PrgP': 'Progressao_passes',
    'PrgR': 'Desarmes_de_progressao'
}

desempenho.rename(columns=columns_translation, inplace=True)

# Calculando colunas adicionais
desempenho['Gols_por_Jogo'] = desempenho['Gols'] / desempenho['Partidas']
desempenho['Min_para_participar'] = desempenho.apply(lambda row: row['Minutos_jogados'] / row['Gols_e_assistencias'] if row['Gols_e_assistencias'] != 0 else 0, axis=1)

# Adicionando ID_Desempenho
desempenho['ID_Desempenho'] = range(1, len(desempenho) + 1)

# Limpar linhas com valores nulos para 'ID_Jogador':
desempenho = desempenho.dropna(subset=['ID_Jogador'])

# Configuração da tabela no BigQuery
dataset_id = "pbrandao_mvp_futebol"
table_id = "fato_desempenho"
full_table_id = f"{project_id}.{dataset_id}.{table_id}"

# Esquema para a tabela fato_desempenho
schema = [
    bigquery.SchemaField("ID_Desempenho", "INT64", mode="REQUIRED"),
    bigquery.SchemaField("ID_Jogador", "INT64", mode="REQUIRED"),
    bigquery.SchemaField("ID_Time", "INT64", mode="NULLABLE"),
    bigquery.SchemaField("ID_LigaAno", "INT64", mode="NULLABLE"),
    bigquery.SchemaField("Idade", "INT64", mode="NULLABLE"),
    bigquery.SchemaField("Partidas", "INT64", mode="NULLABLE"),
    bigquery.SchemaField("Partidas_iniciadas", "INT64", mode="NULLABLE"),
    bigquery.SchemaField("Minutos_jogados", "INT64", mode="NULLABLE"),
    bigquery.SchemaField("90_minutos_jogados", "FLOAT64", mode="NULLABLE"),
    bigquery.SchemaField("Gols", "INT64", mode="NULLABLE"),
    bigquery.SchemaField("Assistencias", "INT64", mode="NULLABLE"),
    bigquery.SchemaField("Gols_e_assistencias", "FLOAT64", mode="NULLABLE"),
    bigquery.SchemaField("Gols_sem_penaltis", "FLOAT64", mode="NULLABLE"),
    bigquery.SchemaField("Gols_de_penaltis", "INT64", mode="NULLABLE"),
    bigquery.SchemaField("Cobrancas_de_penaltis", "INT64", mode="NULLABLE"),
    bigquery.SchemaField("cartoes_amarelos", "INT64", mode="NULLABLE"),
    bigquery.SchemaField("Cartoes_vermelhos", "INT64", mode="NULLABLE"),
    bigquery.SchemaField("Progressao_jogadas", "INT64", mode="NULLABLE"),
    bigquery.SchemaField("Progressao_passes", "INT64", mode="NULLABLE"),
    bigquery.SchemaField("Desarmes_de_progressao", "INT64", mode="NULLABLE"),
    bigquery.SchemaField("Gols_por_Jogo", "FLOAT64", mode="NULLABLE"),
    bigquery.SchemaField("Min_para_participar", "FLOAT64", mode="NULLABLE")
]

# Carregando o DataFrame no BigQuery com esquema definido
job_config = bigquery.LoadJobConfig(schema=schema)
job = client.load_table_from_dataframe(desempenho, full_table_id, job_config=job_config)
job.result()  # Espera até a conclusão do job
```

A tabela fato_desempenho foi projetada para conter os detalhes sobre o desempenho dos jogadores ao longo das temporadas. Começamos carregando os dados dos jogadores, depois aplicamos uma função para normalizar os nomes dos jogadores e dos times, facilitando a integração e consulta de dados posteriormente.

Uma parte crucial deste processo é cruzar os dados desta tabela com outras tabelas de dimensão previamente carregadas no BigQuery. Isso nos permite associar IDs de jogadores, times e ligas/anos à tabela fato_desempenho, enriquecendo a informação e tornando-a mais valiosa para análises futuras.

Depois de cruzar os dados, algumas transformações e cálculos adicionais são realizados. Por exemplo, calculamos 'Gols_por_Jogo' para entender a eficiência de um jogador em marcar gols, e 'Min_para_participar', que nos mostra quantos minutos, em média, um jogador leva para contribuir com um gol ou assistência.

Uma vez que todos os dados são preparados e as transformações aplicadas, procedemos com a configuração para carregar os dados no BigQuery. Definimos um esquema para a tabela fato_desempenho, garantindo que cada coluna do DataFrame seja mapeada corretamente para seu tipo correspondente no BigQuery. Com tudo configurado, carregamos o DataFrame no BigQuery e concluímos o processo.

### 4.4.6- Executando os scripts:

Depois de definir todos os esquemas e relações, realizando todo tratamento adequado para cada tebela, foi necessário executar os scirpts para realizar a carga no BigQuery. Para isso, bastou especificar no terminal onde os arquivos estavam e referenciar o nome deles com 'python' antes do nome do arquivo. 

Os prints abaixo mostram como foi realizada esta etapa.

Subindo as tabelas dimensão para o BigQuery:

![tabelas_dim_shell](https://github.com/pbrandao26/EngenhariaDeDados-MVP-2023/assets/145406479/a1d3f404-e03d-4b8a-ba91-7c0135e5bd86)

Subindo as tabelas fato para o BigQuery:

![tabelas_fato_shell](https://github.com/pbrandao26/EngenhariaDeDados-MVP-2023/assets/145406479/97cac9c0-d3bf-4045-84e9-ad661868997a)

Por fim, todas as tabelas desejadas foram carregadas no BigQuery:

![image](https://github.com/pbrandao26/EngenhariaDeDados-MVP-2023/assets/145406479/dc6928fb-ebf5-4763-b0f6-cb3d2d27cca7)

## 4.5- Perfil e catalogação dos dados:

A governança de dados é uma peça-chave para garantir a integridade, qualidade e utilidade dos dados no nosso projeto. Para isso, realizamos a catalogação e definição do perfil dos dados. Portanto, contamos com a eficiência da API do Google Dataplex.

Começamos estabelecendo descrições claras e precisas para os dados de cada tabela, alinhadas às definições apresentadas na [seção 3 - Modelagem](#3--modelagem) deste relatório:

![categor_descri_dataplex](https://github.com/pbrandao26/EngenhariaDeDados-MVP-2023/assets/145406479/ad9db986-4bc1-4d15-b662-2f59905cad5d)

Em seguida, demos um passo adiante ao criar verificações de perfil no Dataplex. A imagem a seguir mostra o processo de criação para a tabela fato_desempenho, mas é importante destacar que implementamos uma verificação individual para cada tabela do tipo fato:

![criar_perfil_dataplex](https://github.com/pbrandao26/EngenhariaDeDados-MVP-2023/assets/145406479/126cc99d-12fb-428a-bc19-135913aeda35)

![perfis criados no dataplex](https://github.com/pbrandao26/EngenhariaDeDados-MVP-2023/assets/145406479/b45fb05f-daa9-44e8-821b-f771609594d8)

Depois de ter os perfis de dados estabelecidos, a análise se torna bastante direta. Basta acessar a tabela específica e navegar até a aba de perfil de dados para obter insights detalhados sobre a distribuição, qualidade e outras métricas relevantes dos dados.

![visu_perfil_dados_bigquery](https://github.com/pbrandao26/EngenhariaDeDados-MVP-2023/assets/145406479/06689ee3-a747-4ffc-be61-a16178ecb0f2)

