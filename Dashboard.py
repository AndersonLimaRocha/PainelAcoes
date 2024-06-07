 #1. importar bibliotecas

import pandas as pd
import yfinance as yf
import datetime as dt
import streamlit as st
from datetime import datetime
import os

st.set_page_config( page_title="Indicadores de Ações da Bolsa", layout="wide")

st.title("Dashboard dos Indicadores da Bolsa")
st.caption("Dashboard para acompanhamento dos indicadores das ações das Bolsa de Valores IBOVESPA")

#######################################################################################################
                            ######### Carga do Dataframe ##########
#######################################################################################################
file = '/Outputs/MinhasCotacoes.xlsx'
caminho_atual = os.getcwd()
file = caminho_atual + file

minhasacoes = pd.read_excel(file, sheet_name='Cotação das Ações')

lista = ['Todos']
lista = pd.DataFrame(columns=['Col'], data=lista)
Setores = minhasacoes[['SETORECONOMICO']].drop_duplicates().reset_index().rename(columns={'SETORECONOMICO':'Col'})
Setores = pd.concat([lista,Setores]).reset_index(drop=True).drop(columns={'index'})
lista_setores = list(Setores['Col'])

end_date = dt.datetime.today()

# função para selecionar a quantidade de linhas do dataframe
def mostra_qntd_linhas(dataframe):

    qntd_linhas = st.sidebar.slider('Selecione a quantidade de linhas que deseja mostrar na tabela', min_value = 1, max_value = len(dataframe), step = 1)

    #st.write(dataframe.head(qntd_linhas).style.format(subset = ['Valor'], formatter="{:.2f}"))

########################################################################################################
                # ------------ FILTROS DA COLUNA ESQUERDA DO FRAME ------------
########################################################################################################

# filtros para a tabela
st.sidebar.markdown('## Filtros de Seleção')

setor = st.sidebar.selectbox('Selecione o Setor desejado:', options = lista_setores)

if setor != 'Todos':
    sub = minhasacoes[['SUBSETOR']][minhasacoes['SETORECONOMICO'] == setor].drop_duplicates().reset_index().rename(columns={'SUBSETOR':'Col'})
    sub = pd.concat([lista,sub]).reset_index(drop=True).drop(columns={'index'})
    lista_subsetores = list(sub['Col'])
    subsetor = st.sidebar.selectbox('Selecione o Sub Setor desejado:', options = lista_subsetores)

else:
    sub = minhasacoes[['SUBSETOR']].drop_duplicates().reset_index().rename(columns={'SUBSETOR':'Col'})
    sub = pd.concat([lista,sub]).reset_index(drop=True).drop(columns={'index'})
    lista_subsetores = list(sub['Col'])
    subsetor = st.sidebar.selectbox('Selecione o Sub Setor desejado:', options = lista_subsetores)

if subsetor != 'Todos':
    seg = minhasacoes[['SEGMENTO']][minhasacoes['SUBSETOR'] == subsetor].drop_duplicates().reset_index().rename(columns={'SEGMENTO':'Col'})
    seg = pd.concat([lista,seg]).reset_index(drop=True).drop(columns={'index'})
    lista_segmentos = list(seg['Col'])
    segmento = st.sidebar.selectbox('Selecione o Segmento desejado:', options = lista_segmentos)

else:
    seg = minhasacoes[['SEGMENTO']].drop_duplicates().reset_index().rename(columns={'SEGMENTO':'Col'})
    seg = pd.concat([lista,seg]).reset_index(drop=True).drop(columns={'index'})
    lista_segmentos = list(seg['Col'])
    segmento = st.sidebar.selectbox('Selecione o Segmento desejado:', options = lista_segmentos)

if segmento != 'Todos':
    emp = minhasacoes[['EMPRESA']][minhasacoes['SEGMENTO'] == segmento].drop_duplicates().reset_index().rename(columns={'EMPRESA':'Col'})
    emp = pd.concat([lista,emp]).reset_index(drop=True).drop(columns={'index'})
    emp['Col'] = emp['Col'].replace('Todos','Todas')
    lista_empresas = list(emp['Col'] )
    empresa = st.sidebar.selectbox('Selecione a Empresa desejada:', options = lista_empresas)

else:
    emp = minhasacoes[['EMPRESA']][minhasacoes['SEGMENTO'] == segmento].drop_duplicates().reset_index().rename(columns={'EMPRESA':'Col'})
    emp = pd.concat([lista,emp]).reset_index(drop=True).drop(columns={'index'})
    emp['Col'] = emp['Col'].replace('Todos','Todas')
    lista_empresas = list(emp['Col'] )
    empresa = st.sidebar.selectbox('Selecione a Empresa desejada:', options = lista_empresas)

########################################################################################################
                # ------------ FRAME PRINCIPAL CENTRAL ------------
########################################################################################################        

with st.container():
    st.header("Selecione os filtros abaixo para visualizar as ações")

    col1, col2, col3 = st.columns(3)

    with col1:

        if empresa != 'Todas':
            lista_empresa = minhasacoes[['ACAO']][minhasacoes['EMPRESA'] == empresa].drop_duplicates()
            lista_empresa = lista_empresa + '.SA'     
            ativo = st.selectbox("Selecione os ativo desejado:", options=lista_empresa)            

        elif segmento != 'Todos':
            lista_empresa = minhasacoes[['ACAO']][minhasacoes['SEGMENTO'] == segmento].drop_duplicates()
            lista_empresa = lista_empresa + '.SA'        
            ativo = st.selectbox("Selecione os ativo desejado:", options=lista_empresa)

        elif subsetor != 'Todos':
            lista_empresa = minhasacoes[['ACAO']][minhasacoes['SUBSETOR'] == subsetor].drop_duplicates()
            lista_empresa = lista_empresa + '.SA'        
            ativo = st.selectbox("Selecione os ativo desejado:", options=lista_empresa)            

        elif setor != 'Todos':
            lista_empresa = minhasacoes[['ACAO']][minhasacoes['SETORECONOMICO'] == setor].drop_duplicates()
            lista_empresa = lista_empresa + '.SA'        
            ativo = st.selectbox("Selecione os ativo desejado:", options=lista_empresa)

        else:
            lista_empresa = minhasacoes[['ACAO']].drop_duplicates()
            lista_empresa = lista_empresa + '.SA'
            ativo = str(st.selectbox("Selecione os ativo desejado:", options=lista_empresa))

        #tratando o retorno da ação selecionada
        tkt = ativo.replace('.SA','')

        dtcompra = str(minhasacoes['DATACOMPRA'][minhasacoes['ACAO'] == tkt].iloc[0]).replace(' 00:00:00','')
        start_date = minhasacoes['DATACOMPRA'][minhasacoes['ACAO'] == tkt].iloc[0]
        vlpago = float(str(minhasacoes['VALORCOMPRA'][minhasacoes['ACAO'] == tkt].iloc[0]))
        qtdct = minhasacoes['QTDECOTAS'][minhasacoes['ACAO'] == tkt].iloc[0]

    with col2:
        data_inicial = st.date_input("Selecione a Data inicial", start_date)

    with col3:
        data_final = st.date_input("Selecione a Data final", end_date)

df = minhasacoes[minhasacoes['ACAO'] == tkt]
df['VALORCOMPRA'] = float(vlpago)
df = df.rename(columns={'VALORAJUSTADO':'Cotação no Período','MAIORCOTACAO':'Máxima Cotação Período', 'MENORCOTACAO':'Menor Cotação Período', 'VALORCOMPRA': 'Valor de Compra'})

########################################################################################################

#4. Criando metricas
ult_atualizacao =  str(df['DATACOTACAO'].max()).replace(' 00:00:00','') #Data da ultima att
ult_cotacao = round(df.loc[df.index.max(), "Cotação no Período"], 2) #Pega a última cotacao
menor_cotacao = round(df["Cotação no Período"].min(), 2) #Pega a menor cotacao do periodo
maior_cotacao = round(df["Cotação no Período"].max(), 2) #Pega a maior cotacao do periodo
prim_cotacao = round(df.loc[df.index.min(), "Cotação no Período"],2 ) #Pega a primeira cotacao encontrada
delta = round(((ult_cotacao- vlpago)/ vlpago)*100,2) #A variacao da cotacao no periodo
data = df[df["VALORDIVIDENDO"]>0]
dividendo = data["VALORDIVIDENDO"].mean()
dividendo_soma = data["VALORDIVIDENDO"].sum()
historico = data["VALORDIVIDENDO"].count()
Pl = ult_cotacao / dividendo_soma
dividen_max = data["VALORDIVIDENDO"].max()
dividen_min = data["VALORDIVIDENDO"].min()
dividend_yeld = round(dividendo_soma/ult_cotacao,4)*100

########################################################################################################

with st.container():

    st.subheader(f"Indicadores principais da ação {ativo}")
    col11, col12, col13, col14, col15 = st.columns(5)

    with col11:
        st.metric(f"Valor Pago em \n {dtcompra} "," R$ {:,.2f}".format(vlpago))

    with col12:
        st.metric(f"Qtde de Cotas: ","{:,.0f}".format(qtdct))

    with col13:
        st.metric(f"Ultima Cotação \n {ult_atualizacao} "," R$ {:,.2f}".format(ult_cotacao),f"{delta}%" )

    with col14:
        st.metric(f"Menor cotação do período: "," R$ {:,.2f}".format(menor_cotacao))

    with col15:
        st.metric(f"Maior cotação do período: "," R$ {:,.2f}".format(maior_cotacao))


with st.container():
    #Exibindo gráfico de área
    st.text("Variação da Cotação no Período:")
    st.area_chart(df["Cotação no Período"])

    #Exibindo gráfico de linha para comparação de valores no período
    st.text("Valor de Compra, Cotação no Período e Máximo Cotação no Período")
    st.line_chart(df[["Valor de Compra","Cotação no Período", "Máxima Cotação Período"]])

########################################################################################################
                    # ----------------- Tabela analítica -----------------
########################################################################################################
with st.container():
    st.subheader("Tabela analítica dos Ativos")
    if empresa != 'Todas':
        st.markdown(f"Tabela analítica dos Ativos Filtrado por **Empresa:** {empresa}")
        tb = minhasacoes[minhasacoes['EMPRESA'] == empresa]
########################################################################################################
        st.dataframe(tb, use_container_width= True)

    elif segmento != 'Todos':
        st.markdown(f"Tabela analítica dos Ativos Filtrado por **Segmento:** {segmento}")
        tb = minhasacoes[minhasacoes['SEGMENTO'] == segmento]
        st.dataframe(tb)

    elif subsetor != 'Todos':
        st.markdown(f"Tabela analítica dos Ativos Filtrado por **Subsetor:** {subsetor}")
        tb = minhasacoes[minhasacoes['SUBSETOR'] == subsetor]
        st.dataframe(tb)

    elif setor != 'Todos':
        st.markdown(f"Tabela analítica dos Ativos Filtrado por **Setor:** {setor}")
        tb = minhasacoes[minhasacoes['SETORECONOMICO'] == setor]
        st.dataframe(tb)

    else:
        st.markdown(f"Tabela analítica de todos os Ativos")
        tb = minhasacoes
        st.dataframe(tb)

########################################################################################################

with st.container():
    st.subheader("Sobre os dividendos")
    st.caption(f"Analise dos Dividendos pagos pela {ativo}")

    col5, col6, col7 = st.columns(3)

    with col5:
        st.caption("Tabela com todos os pagamentos no intervalo: ")
        st.dataframe(data[["VALORDIVIDENDO"]])

    with col6:
        st.metric(f"Quantidade de pagamentos no intervalo: ", " {:,.2f}".format(historico))
        st.metric(f"Pagamento médio (Dividendos): ", " R$ {:,.2f}".format(dividendo))

    with col7:
        st.metric(f"Pagamento máximo Dividendo", "R$ {:,.2f}".format(dividen_max))
        st.metric(f"Pagamento mínimo Dividendo", "R$ {:,.2f}".format(dividen_min))


with st.container():
    st.caption("Grafico de linhas com os pagamentos dos Dividendos:")
    st.line_chart(data["VALORDIVIDENDO"])


