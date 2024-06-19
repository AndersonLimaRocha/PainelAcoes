# PainelAcoes
Projeto de visualização de ações da Bolsa

## **Script do Pipeline de Carga das Cotações das Ações negociadas na Bolsa (Ibovespa/B3)**

Este é um pipeline Python para carregar dados de cotações de ações negociadas na Bolsa de Valores (B3) do Brasil. \
O Pipeline consolida as informações e as exporta para um arquivo Excel. \
Os detalhes das ações que você negocia na bolsa podem ser acessadas pela **Nota de Corretagem**, emitida pela corretora.\
A nota é um extrato das operações realizadas na Bolsa de Valores e contém detalhes como: 
* Espécie da operação
* Quantidade de títulos
* Preço
* Data do pregão
* Valor da negociação
* Corretagem cobrada
* Emolumentos devidos
* Mercado em que a operação foi realizada
* Se a operação foi de compra (C) ou venda (V)
* Tipo de mercado em que a operação foi realizada
* Especificações do título 


#### **Funcionalidades do Pipeline:** 
* Carregar detalhes das ações negociadas a partir de um arquivo Excel.
* Obter informações de setor e segmento das ações utilizando a biblioteca tradingcomdados.
* Carregar o histórico de cotações e dividendos das ações utilizando a biblioteca yahooquery.
* Consolidar os dados das ações, histórico de cotações e dividendos em um único DataFrame.
* Exportar os dados consolidados para um arquivo Excel.


#### **Funções criadas para execução do Pipeline:**
* **run_pipeline:**             Função principal que coordena todo o processo.
* **load_acoes_ibov:**          Carrega os dados das ações do arquivo Excel (Input).
* **get_sector_segment:**       Obtém informações de setor e segmento das ações.
* **load_historical_data:**     Carrega o histórico de cotações e dividendos das ações.
* **consolidate_data:**         Consolida os dados das ações.
* **export_to_excel:**          Exporta os dados consolidados para um arquivo Excel (Output).

#### **Bibliotecas utilizadas:**
* **pandas** -> biblioteca utilizada para armazenar os dados do Pipeline
* **tradingcomdados** -> obtem detalhes de setores econômicos, subsetores e segmentos de mercado, para ativos financeiros negociados na bolsa
* **yahooquery** -> para obter dados históricos de cotações e dividendos das ações.

#### **Diretórios e arquivos dependentes e gerados (Input / Output):**
* **Inputs/MinhasAcoes.xlsx:** Arquivo de entrada contendo os detalhes das ações negociadas.
* **Outputs/MinhasCotacoes.xlsx:** Arquivo de saída onde os dados consolidados são exportados.

#### **O Pipeline Carregará o arquivo com layout (INPUT):**
* **TITULO** CORRETORA = Descrição do Titulo na corretora
* **CODIGO** = Código da ação para negociação na Bolsa
* **COTAS** = Quantidade de fração/Cotas compradas
* **VALOR** = Valor pago na Cota/Fração da Ação
* **DATA COMPRA** = Data da compra da Cota/Fração 

#### **O Pipeline extrairá o arquivo com layout (OUTPUT):**
* **SETORECONOMICO**    = Descrição do Setor ecônomico da ação
* **SUBSETOR**          = Descrição do subsetor ecônomico da ação
* **SEGMENTO**          = Descrição do segmento ecônomico da ação
* **TITULO**            = Código do título da acão
* **ACAO**              = Código da ação negociada na Bolsa de Valores (B3)
* **QTDECOTAS**         = Quantidade de Cotas/Fração da ação
* **VALOR**             = Valor de compra pago na ação
* **DATACOMPRA**        = Data da compra da Cota/Fração
* **DATACOTACAO**       = Data da cotação da Cota/Fração
* **VALORABERTURA**     = Valor de abertura que a Cota/Fração iniciou no dia da cotação
* **MAIORCOTACAO**      = Maior valor/pico que a Cota/Fração da ação chegou no dia da cotação
* **MENORCOTACAO**      = Menor valor que a Cota/Fração da ação chegou no dia da cotação
* **VALORAJUSTADO**     = Valor final da Cota/Fração da ação fechou no dia da cotação
* **DATAPROCESSAMENTO** = Data de processamento/excecução
* **VALORDIVIDENDO**    = Valor do dividendo 
* **FLAG_DIVIDENDOS**   = Data de pagto do dividendo
* **ANOCOTACAO**   = Ano do pagto do dividendo
* **DIVIDENDOSANO**   = Flag do pagto do dividendo no Ano

#### **Observações:** 

O Pipeline não acessa nenhuma plataforma para negociação das suas ações. Ele apenas busca as cotações divugadas no mercado pela B3. \
Em nenhum momento será solicitado nenhum dado pessoal ou login e senha de seus Brokers.

