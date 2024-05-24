# PainelAcoes
Projeto de visualização de ações da Bolsa

## Script Principal de Carga e cotações das Ações.

### Tratamento de Exceção na Importação de Módulos

Blocos `try-except` para:
- `warnings`
- `pandas`
- `tradingcomdados.alternative_data`
- `yahooquery` (`Ticker`)
- `datetime`

### Leitura do Arquivo Excel

Arquivo: `Inputs/MinhasAcoes.xlsx`
- Função: `pd.read_excel()`
- Variável: `file`

### Criação do DataFrame `dfAcoes`

Definição da estrutura e tipagem das colunas:
- Colunas: `['SETORECONOMICO', 'SUBSETOR', 'SEGMENTO', 'EMPRESA', 'TITULO', 'ACAO', 'QTDECOTAS', 'VALOR', 'DATACOMPRA']`
- Tipos:
  - `SETORECONOMICO`: `str`
  - `SUBSETOR`: `str`
  - `SEGMENTO`: `str`
  - `EMPRESA`: `str`
  - `TITULO`: `str`
  - `ACAO`: `str`
  - `QTDECOTAS`: `int`
  - `VALOR`: `Float64`
  - `DATACOMPRA`: `str`

### Loop: Processamento das Ações

Informação dos setores econômicos e preenchimento do DataFrame `dfAcoes`:
- Loop sobre: `acoes_ibov['CODIGO']`
- Função: `ad.get_sectors(tkt)`
- Campos:
  - `SETOR ECONÔMICO`
  - `SUBSETOR`
  - `SEGMENTO`
  - `NOME NO PREGÃO`
  - `TITULO CORRETORA RICO`
  - `COTAS`
  - `VALOR`
  - `DATA`

### Deduplicação e Ordenação do DataFrame `dfAcoes`

- Funções: 
  - `drop_duplicates()`
  - `sort_values(by=['ACAO'])`
  - `reset_index()`

### Criação do DataFrame `historico_cotacao`

Definição da estrutura e tipagem das colunas:
- Colunas: `['ACAO', 'DATACOTACAO', 'VALORABERTURA', 'MAIORCOTACAO', 'MENORCOTACAO', 'VALORFECHAMENTO', 'VALORAJUSTADO', 'DATAPROCESSAMENTO']`

### Loop: Obtenção de Cotações Históricas

Utilizando a biblioteca `yahooquery` e preenchimento do DataFrame `historico_cotacao`:
- Loop sobre: `dfAcoes.index`
- Função: `Ticker(tkt).history(start=dtcompra, end=end_date).reset_index()`

### Consolidação dos Dados de Ações e Cotações Históricas

- Função: `pd.merge(dfAcoes, historico_cotacao, on='ACAO')`

### Exibição do DataFrame `CotacaoConsolidadas`

- Função: `CotacaoConsolidadas`
