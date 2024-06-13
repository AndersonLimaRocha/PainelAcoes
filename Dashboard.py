 #1. importar bibliotecas

import pandas as pd
import yfinance as yf
import datetime as dt
import streamlit as st
from streamlit_modal import Modal
from datetime import datetime
import os
import numpy as np
import plotly.express as px 
import plotly.graph_objects as go

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


# Função para retornar a ultima cotação da ação
def retorna_ultima_cotacao_acao(df):
    latest_quotes = df.loc[df.groupby('ACAO')['DATACOTACAO'].idxmax()]
    latest_quotes = latest_quotes[['ACAO', 'DATACOTACAO', 'QTDECOTAS', 'VALORFECHAMENTO']].drop_duplicates()
    latest_quotes['VALORTOTALATUAL'] = latest_quotes['QTDECOTAS'] * latest_quotes['VALORFECHAMENTO']
    return latest_quotes

# Função para retornar um dataframe geral agrupado
def retorna_agrupamento_geral():
  df = minhasacoes[['SETORECONOMICO', 'SUBSETOR', 'SEGMENTO','EMPRESA', 'ACAO','QTDECOTAS', 'VALORCOMPRA']].drop_duplicates()
  df['VALORTOTALCOMPRA'] = df['QTDECOTAS'] * df['VALORCOMPRA']
  df = df.groupby(['SETORECONOMICO', 'SUBSETOR', 'SEGMENTO','EMPRESA', 'ACAO']).agg({
      'QTDECOTAS': np.sum,
      'VALORTOTALCOMPRA': np.sum
  }).sort_values(by='VALORTOTALCOMPRA', ascending=False).reset_index()
  return df

# Função para retornar um dataframe agrupado
def create_dataframe(coluna):
    df = minhasacoes[[coluna, 'QTDECOTAS', 'VALORCOMPRA', 'ACAO']].drop_duplicates()
    df['VALORTOTALCOMPRA'] = df['QTDECOTAS'] * df['VALORCOMPRA']
    df = df.groupby([coluna, 'ACAO']).agg({
        'QTDECOTAS': np.sum,
        'VALORTOTALCOMPRA': np.sum
    }).sort_values(by='VALORTOTALCOMPRA', ascending=False).reset_index()
    return df

# Função para consolidar o dataframe
def consolidate_details(df, latest_quotes):
    df = pd.merge(df, latest_quotes[['ACAO', 'DATACOTACAO', 'VALORTOTALATUAL']], on='ACAO', how='inner', validate="many_to_many")
    df = df.drop_duplicates().sort_values(by='ACAO').reset_index(drop=True)
    return df

# Função para agrupar o dataframe
def group_by(df,coluna):
    df = df.groupby(coluna).agg({
        'QTDECOTAS': np.sum,
        'VALORTOTALCOMPRA': np.sum,
        'VALORTOTALATUAL': np.sum
    }).sort_values(by='VALORTOTALCOMPRA', ascending=False).reset_index()
    return df

# Função para agrupar o dataframe
def geral_group_by(df):
    df = df.groupby(['SETORECONOMICO', 'SUBSETOR', 'SEGMENTO','EMPRESA', 'ACAO']).agg({
        'QTDECOTAS': np.sum,
        'VALORTOTALCOMPRA': np.sum,
        'VALORTOTALATUAL': np.sum
    }).sort_values(by='VALORTOTALCOMPRA', ascending=False).reset_index()
    return df

# Função para atualizar percentual de rendimento e prejuizo
def update_performance(df):
    df['RENDIMENTO(%)'] = ((df['VALORTOTALATUAL'] / df['VALORTOTALCOMPRA'] - 1) * 100).round(2)
    df['PREJUIZO(%)'] = ((df['VALORTOTALCOMPRA'] / df['VALORTOTALATUAL'] - 1) * 100).round(2)
    df['RETORNO(%)'] = ((df['VALORTOTALATUAL'] / df['VALORTOTALCOMPRA'] - 1) * 100).round(2)
    df.loc[df['VALORTOTALATUAL'] < df['VALORTOTALCOMPRA'], 'RENDIMENTO(%)'] = 0
    df.loc[df['VALORTOTALATUAL'] >= df['VALORTOTALCOMPRA'], 'PREJUIZO(%)'] = 0
    return df

# Função que centraliza as funções 
def agupamento(agrupamento, df):
    coluna = agrupamento
    ult_cot = retorna_ultima_cotacao_acao(df)
    dtf = create_dataframe(coluna)
    dtf = consolidate_details(dtf, ult_cot)
    dtf = group_by(dtf, coluna)
    dtf = update_performance(dtf)
    return dtf

# Função que centraliza as funções 
def agupamento_geral(df):
    ult_cot = retorna_ultima_cotacao_acao(df)
    dtf = retorna_agrupamento_geral()
    dtf = consolidate_details(dtf, ult_cot)
    dtf = geral_group_by(dtf)
    dtf = update_performance(dtf)
    return dtf


lista = ['Todos']
lista = pd.DataFrame(columns=['Col'], data=lista)
Setores = minhasacoes[['SETORECONOMICO']].drop_duplicates().reset_index().rename(columns={'SETORECONOMICO':'Col'})
Setores = pd.concat([lista,Setores]).reset_index(drop=True)
lista_setores = list(Setores['Col'])

end_date = dt.datetime.today()

########################################################################################################
                # ------------ FRAME PRINCIPAL CENTRAL ------------
########################################################################################################        
@st.experimental_dialog(" ",width="large")
def macro_grafico(indicador):
        ind = indicador
        if ind == 'SETORECONOMICO':
            stor = agupamento('SETORECONOMICO', minhasacoes)
            fig=px.bar(stor,
                    title='Ações por volume de compra (R$) e % de retorno',
                    x='VALORTOTALCOMPRA',
                    y='SETORECONOMICO', 
                    orientation='h', 
                    color='RETORNO(%)', 
                    color_continuous_scale = 'darkmint',
                    text_auto=True)
            fig.update_layout(yaxis=dict(autorange="reversed"))
            fig.update_layout(yaxis_title=None)
            fig.update_layout(xaxis_title=None)
            st.plotly_chart(fig) 
        elif ind == 'SUBSETOR':
            stor = agupamento('SUBSETOR', minhasacoes)
            fig=px.bar(stor,
                    title='Ações por volume de compra (R$) e % de retorno',
                    x='VALORTOTALCOMPRA',
                    y='SUBSETOR', 
                    orientation='h', 
                    color='RETORNO(%)', 
                    color_continuous_scale = 'darkmint',
                    text_auto=True)
            fig.update_layout(yaxis=dict(autorange="reversed"))
            fig.update_layout(yaxis_title=None)
            fig.update_layout(xaxis_title=None)
            st.plotly_chart(fig, use_container_width= True)      
        elif ind == 'SEGMENTO':
            stor = agupamento('SEGMENTO', minhasacoes)
            fig=px.bar(stor,
                    title='Ações por volume de compra (R$) e % de retorno',                       
                    x='VALORTOTALCOMPRA',
                    y='SEGMENTO', 
                    orientation='h', 
                    color='RETORNO(%)', 
                    color_continuous_scale = 'darkmint',
                    text_auto=True)
            fig.update_layout(yaxis=dict(autorange="reversed"))
            fig.update_layout(yaxis_title=None)
            fig.update_layout(xaxis_title=None)
            st.plotly_chart(fig, use_container_width= True) 
        elif ind == 'EMPRESA':
            stor = agupamento('EMPRESA', minhasacoes)
            fig=px.bar(stor,
                    title='Ações por volume de compra (R$) e % de retorno',                       
                    x='VALORTOTALCOMPRA',
                    y='EMPRESA', 
                    orientation='h', 
                    color='RETORNO(%)', 
                    color_continuous_scale = 'darkmint',
                    text_auto=True)
            fig.update_layout(yaxis=dict(autorange="reversed"))
            fig.update_layout(yaxis_title=None)
            fig.update_layout(xaxis_title=None)
            st.plotly_chart(fig, use_container_width= True)    
        elif ind == 'GERAL':          
            dtf = agupamento_geral(minhasacoes)
            fig = px.treemap(dtf, 
                            title='Ações por volume de compra (R$) e % de retorno',                             
                            path=[px.Constant('Ações da Bovespa'), 'SETORECONOMICO', 'SUBSETOR', 'SEGMENTO', 'EMPRESA', 'ACAO'], 
                            values='VALORTOTALCOMPRA',
                            color='RETORNO(%)', 
                            color_continuous_scale = 'darkmint', 
                            hover_data=['ACAO'])
            st.plotly_chart(fig, use_container_width= True)     




with st.container(border=True ):
    st.header("Distribuição do volume de Ações")
    st.markdown(f"Clique nos botões abaixo para visualizar os gráficos e analisar o percentual de retorno")

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("GERAL", use_container_width=True):
            macro_grafico('GERAL')
    with col2:
        if st.button("SETOR ECONÔMICO", use_container_width=True):
            macro_grafico('SETORECONOMICO')
    with col3:                                  
        if st.button("SUB SETOR ECONÔMICO", use_container_width=True):
            macro_grafico('SUBSETOR')
    with col4:                                  
        if st.button("SEGMENTO", use_container_width=True):
            macro_grafico('SUBSETOR')
    with col5:                                  
        if st.button("EMPRESA", use_container_width=True):
            macro_grafico('EMPRESA')



with st.container(border=True ):

    st.header("Selecione os filtros abaixo para visualizar os detalhes das ações")

    col1a, col2a, col3a, col4a = st.columns(4)

    with col1a:
        setor = st.selectbox('Selecione o Setor desejado:', options = lista_setores)

    with col2a:
        if setor != 'Todos':
            sub = minhasacoes[['SUBSETOR']][minhasacoes['SETORECONOMICO'] == setor].drop_duplicates().reset_index().rename(columns={'SUBSETOR':'Col'})
            sub = pd.concat([lista,sub]).reset_index(drop=True)
            lista_subsetores = list(sub['Col'])
            subsetor = st.selectbox('Selecione o Sub Setor desejado:', options = lista_subsetores)

        else:
            sub = minhasacoes[['SUBSETOR']].drop_duplicates().reset_index().rename(columns={'SUBSETOR':'Col'})
            sub = pd.concat([lista,sub]).reset_index(drop=True)
            lista_subsetores = list(sub['Col'])
            subsetor = st.selectbox('Selecione o Sub Setor desejado:', options = lista_subsetores)

    with col3a: 
        if subsetor != 'Todos':
            seg = minhasacoes[['SEGMENTO']][minhasacoes['SUBSETOR'] == subsetor].drop_duplicates().reset_index().rename(columns={'SEGMENTO':'Col'})
            seg = pd.concat([lista,seg]).reset_index(drop=True)
            lista_segmentos = list(seg['Col'])
            segmento = st.selectbox('Selecione o Segmento desejado:', options = lista_segmentos)

        else:
            seg = minhasacoes[['SEGMENTO']].drop_duplicates().reset_index().rename(columns={'SEGMENTO':'Col'})
            seg = pd.concat([lista,seg]).reset_index(drop=True)
            lista_segmentos = list(seg['Col'])
            segmento = st.selectbox('Selecione o Segmento desejado:', options = lista_segmentos)

    with col4a:
        if segmento != 'Todos':
            emp = minhasacoes[['EMPRESA']][minhasacoes['SEGMENTO'] == segmento].drop_duplicates().reset_index().rename(columns={'EMPRESA':'Col'})
            emp = pd.concat([lista,emp]).reset_index(drop=True)
            emp['Col'] = emp['Col'].replace('Todos','Todas')
            lista_empresas = list(emp['Col'] )
            empresa = st.selectbox('Selecione a Empresa desejada:', options = lista_empresas)

        else:
            emp = minhasacoes[['EMPRESA']][minhasacoes['SEGMENTO'] == segmento].drop_duplicates().reset_index().rename(columns={'EMPRESA':'Col'})
            emp = pd.concat([lista,emp]).reset_index(drop=True)
            emp['Col'] = emp['Col'].replace('Todos','Todas')
            lista_empresas = list(emp['Col'] )
            empresa = st.selectbox('Selecione a Empresa desejada:', options = lista_empresas)
    
    
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
        dtcompra = str(dt.datetime.strptime(dtcompra, '%Y-%m-%d').strftime('%d/%m/%Y'))
        end_date = dt.datetime.today()

        start_date = (minhasacoes['DATACOMPRA'][minhasacoes['ACAO'] == tkt].iloc[0])
        vlpago = float(str(minhasacoes['VALORCOMPRA'][minhasacoes['ACAO'] == tkt].iloc[0]))
        qtdct = minhasacoes['QTDECOTAS'][minhasacoes['ACAO'] == tkt].iloc[0]

        setoreco = str(minhasacoes['SETORECONOMICO'][minhasacoes['ACAO'] == tkt].iloc[0])
        subsetoreco = str(minhasacoes['SUBSETOR'][minhasacoes['ACAO'] == tkt].iloc[0])
        segmento = str(minhasacoes['SEGMENTO'][minhasacoes['ACAO'] == tkt].iloc[0])
        empresa = str(minhasacoes['EMPRESA'][minhasacoes['ACAO'] == tkt].iloc[0])


    with col2:
        data_inicial = str(st.date_input("Selecione a Data inicial", start_date, format= 'DD/MM/YYYY'))
        data_inicial = dt.datetime.strptime(data_inicial, '%Y-%m-%d')

    with col3:
        data_final = str(st.date_input("Selecione a Data final", end_date, format= 'DD/MM/YYYY'))
        data_final = dt.datetime.strptime(data_final, '%Y-%m-%d')

df = minhasacoes[(minhasacoes['ACAO'] == tkt)]
df['VALORCOMPRA'] = float(vlpago)
df = df.rename(columns={'VALORAJUSTADO':'Cotação no Período','MAIORCOTACAO':'Máxima Cotação Período', 'MENORCOTACAO':'Menor Cotação Período', 'VALORCOMPRA': 'Valor de Compra'})
df = df[(df['DATACOTACAO'] >= data_inicial) & (df['DATACOTACAO'] <= data_final)]

if df.empty:
    df = minhasacoes[(minhasacoes['ACAO'] == tkt)]
    df['VALORCOMPRA'] = float(vlpago)
    df = df.rename(columns={'VALORAJUSTADO':'Cotação no Período','MAIORCOTACAO':'Máxima Cotação Período', 'MENORCOTACAO':'Menor Cotação Período', 'VALORCOMPRA': 'Valor de Compra'})    
    st.markdown("<p style='color:red;'><b>OBS:</b> Períodos das datas não localizados </p>", unsafe_allow_html = True)
    st.markdown(f"Refaça os filtros das datas respeitando o período mínimo de {start_date.strftime('%d/%m/%Y')} e máximo de {end_date.strftime('%d/%m/%Y')} de cotação da ação {tkt}.")
    

########################################################################################################
#4. Criando metricas
ult_atualizacao =  str(df['DATACOTACAO'].max()).replace(' 00:00:00','') #Data da ultima att
ult_atualizacao = str(dt.datetime.strptime(ult_atualizacao, '%Y-%m-%d').strftime('%d/%m/%Y')) #Data da ultima att
ult_cotacao = float(str(df.loc[df.index.max(), "Cotação no Período"])) #Pega a última cotacao
menor_cotacao = round(df["Cotação no Período"].min(), 2) #Pega a menor cotacao do periodo
maior_cotacao = round(df["Cotação no Período"].max(), 2) #Pega a maior cotacao do periodo
prim_cotacao = df.loc[df.index.min(), "Cotação no Período"] #Pega a primeira cotacao encontrada
delta = round(((ult_cotacao - vlpago)/ vlpago)*100,2) #A variacao da cotacao no periodo
data = df[df["VALORDIVIDENDO"]>0]
dividendo = data["VALORDIVIDENDO"].mean()
dividendo_soma = data["VALORDIVIDENDO"].sum()
historico = data["VALORDIVIDENDO"].count()
Pl = ult_cotacao / dividendo_soma
dividen_max = data["VALORDIVIDENDO"].max()
dividen_min = data["VALORDIVIDENDO"].min()
dividend_yeld = round(dividendo_soma/ult_cotacao,4)*100

########################################################################################################

with st.container(border=True ):

    st.subheader(f"Indicadores principais da ação {ativo}")

    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.write(f'*Setor Econômico:* {setoreco}')

    with col2:
        st.write(f'*Sub Setor Econômico:* {subsetoreco}')

    with col3:
        st.write(f'*Segmento:* {segmento}')

    with col4:
        st.write(f'*Empresa:* {empresa}')                

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


with st.container(border=True ):
    #Exibindo gráfico de área
    fig = px.area(df, x="DATACOTACAO", y="Cotação no Período", line_group="EMPRESA", title="Variação da Cotação no Período")
    fig.update_layout(
                    xaxis_title='Período',
                    yaxis_title='Cotação')        
    st.plotly_chart(fig, use_container_width= True)

    #Exibindo gráfico de linha para comparação de valores no período  
    fig = px.line(df, 
                  x="DATACOTACAO", 
                  y=["Valor de Compra","Cotação no Período", "Máxima Cotação Período"], 
                  title='Comparação de Valor de Compra, Cotação no Período e a Cotação Máxima no Período', 
                  color_discrete_sequence=["gray", "light blue", "red"])
    fig.update_layout(
                    xaxis_title='Período',
                    yaxis_title='Cotação')
    st.plotly_chart(fig, use_container_width= True)


########################################################################################################
                    # ----------------- Tabela analítica -----------------
########################################################################################################
cxt = st.checkbox('Clique aqui para Exibir tabela analítica')

if cxt:

    with st.container(border=True ):
        
        if empresa != 'Todas':
            st.subheader(f"Tabela analítica dos Ativos Filtrado por Empresa: {empresa}")
            tb = minhasacoes[minhasacoes['EMPRESA'] == empresa]
    ########################################################################################################
            st.dataframe(tb, use_container_width= True)

        elif segmento != 'Todos':
            st.subheader(f"Tabela analítica dos Ativos Filtrado por Segmento: {segmento}")
            tb = minhasacoes[minhasacoes['SEGMENTO'] == segmento]
            st.dataframe(tb)

        elif subsetor != 'Todos':
            st.subheader(f"Tabela analítica dos Ativos Filtrado por Subsetor: {subsetor}")
            tb = minhasacoes[minhasacoes['SUBSETOR'] == subsetor]
            st.dataframe(tb)

        elif setor != 'Todos':
            st.subheader(f"Tabela analítica dos Ativos Filtrado por Setor: {setor}")
            tb = minhasacoes[minhasacoes['SETORECONOMICO'] == setor]
            st.dataframe(tb)

        else:
            tb = minhasacoes
            st.subheader(f"Tabela analítica dos Ativos")
            st.dataframe(tb)

########################################################################################################

# with st.container():
#     st.subheader("Sobre os dividendos")
#     st.caption(f"Analise dos Dividendos pagos pela {ativo}")

#     col5, col6, col7 = st.columns(3)

#     with col5:
#         st.caption("Tabela com todos os pagamentos no intervalo: ")
#         st.dataframe(data[["VALORDIVIDENDO"]])

#     with col6:
#         st.metric(f"Quantidade de pagamentos no intervalo: ", " {:,.2f}".format(historico))
#         st.metric(f"Pagamento médio (Dividendos): ", " R$ {:,.2f}".format(dividendo))

#     with col7:
#         st.metric(f"Pagamento máximo Dividendo", "R$ {:,.2f}".format(dividen_max))
#         st.metric(f"Pagamento mínimo Dividendo", "R$ {:,.2f}".format(dividen_min))


# with st.container():
#     st.caption("Grafico de linhas com os pagamentos dos Dividendos:")
#     st.line_chart(data["VALORDIVIDENDO"])