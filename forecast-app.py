# In[16]:


def main():
    !pip install seaborn
    import streamlit as st
    import pandas as pd
    from json import loads
    import time
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib as m
    import seaborn as sns
    import pmdarima as pm
    from matplotlib import pyplot
    import streamlit as st
    from pathlib import Path
    from urllib.parse import urlparse, parse_qs
    import openai
    import json
    import requests
    from flask import Flask, render_template, request
    import scipy
    import warnings
    st.title("Olá Cadastrer")
    
    st.header("UPLOAD arquivo de .csv com os dados sobre sessões da empresa")
    arquivo = st.file_uploader('Suba seu arquivo csv', type = 'csv', key='arquivo')
    if arquivo:
        st.write("Nome do arquivo: ", arquivo)
        colunas_selecionadas = ['Month','Sessions', 'Transaction_revenue']
        dados = pd.read_csv(arquivo, parse_dates = True, usecols=colunas_selecionadas)
        dados = pd.DataFrame(dados)
        dados['Transaction_revenue'] = pd.to_numeric(dados['Transaction_revenue'].str.replace(',', '.'), errors='coerce')
        dados['Sessões executadas'] = dados['Sessions']
        dados['Month'] = pd.to_datetime(dados['Month'], format='%d/%m/%Y')
        dados = dados.sort_values(by='Month')
        dados = dados.drop(['Sessions'], axis = 1)
        st.dataframe(dados)
    else:
        st.error("Ainda não possuo um arquivo .csv")
        
    # Criar o gráfico de linha
    fig, ax = plt.subplots()
    
    ax.plot(dados['Month'], dados['Sessões executadas'], marker='o', linestyle='-', color='b', label='Sessões')

    # Adicionar rótulos aos eixos
    plt.xlabel('Meses')
    ax.set_ylabel('Sessões')

    # Adicionar título ao gráfico
    ax.set_title('Meses X Sessões')

    # Adicionar legenda
    ax.legend()
    plt.xticks(rotation=25)
    # Exibir o gráfico
    st.pyplot(fig)

    # Criar o gráfico 2
    fig2, ax2 = plt.subplots()
    
    ax2.plot(dados['Month'], dados['Transaction_revenue'], marker='o', linestyle='-', color='b', label='Receita')

    # Adicionar rótulos aos eixos
    plt.xlabel('Meses')
    ax2.set_ylabel('Receita')

    # Adicionar título ao gráfico
    ax2.set_title('Meses X Receita')

    # Adicionar legenda
    ax2.legend()
    plt.xticks(rotation=25)
    # Exibir o gráfico
    st.pyplot(fig2)
    
    # Criar um dicionário com os dados
    dados_ctr_Clicks = {
    'Posicao': list(range(1, 11)),  # Coluna 'Posicao' de 1 a 10
    'Crescimento do CTR': [ 0.404, 0.215, 0.142, 0.11, 0.092, 0.087, 0.068, 0.061, 0.073, 0.054]}

    # Criar o DataFrame
    df_Clicks = pd.DataFrame(dados_ctr_Clicks)

    # Imprimir o DataFrame
    st.header("Estudo sobre crescimento do CTR")
    st.write(df_Clicks)

    st.header("Médias de crescimento por posições")
    # Calculando a média para as posições 1 a 3
    media_posicoes_1_a_3 = df_Clicks.loc[0:2, 'Crescimento do CTR'].mean().round(2)

    # Calculando a média para as posições 4 a 10
    media_posicoes_4_a_10 = df_Clicks.loc[3:9, 'Crescimento do CTR'].mean().round(2)

    # Calculando a média para as posições top 10
    media_posicoes_top10 = df_Clicks.loc[:9, 'Crescimento do CTR'].mean().round(2)

    st.write('media de 1 a 3: ',media_posicoes_1_a_3)
    st.write('media de 4 a 10: ',media_posicoes_4_a_10)
    st.write('media top 10: ',media_posicoes_top10)
        
    st.header("Loading")
    with st.spinner("Aguarde o carregamento"):
        time.sleep(3)
    
    st.header("UPLOAD arquivo de .csv com os dados sobre estudo de kw")
    arquivo2 = st.file_uploader('Suba seu arquivo csv', type = 'csv', key='arquivo2')
    if arquivo2:
        df_palavras = pd.read_csv(arquivo2)
        df_palavras['Position'] = pd.to_numeric(df_palavras['Position'], errors='coerce')
        # Exibir o resultado
        st.header("Base de dados completa")
        st.dataframe(df_palavras)
        st.write("Quantidade de palavras no estudo de palavras:" , len(df_palavras))

        # Criando um DataFrame sobre top 3
        df_palavras_top3 = df_palavras[(df_palavras['Position'] <= 3) & (df_palavras['Search Volume'] > 0)]
        soma_busca_top3 = df_palavras_top3['Search Volume'].sum() * media_posicoes_1_a_3
        # Exibindo o novo DataFrame
        st.header("Base de dados top 3")
        st.dataframe(df_palavras_top3)
        st.write("Quantidade de palavras no estudo de palavras:" , len(df_palavras_top3))
        st.write("Esperado recebido pelo top 3: ", soma_busca_top3)

        # Criando um DataFrame sobre top 4 a 10
        df_entre_4a10 = df_palavras[(df_palavras['Position'] > 3)  & (df_palavras['Position'] < 11) & (df_palavras['Search Volume']>0)]
        soma_busca_top4a10 = df_entre_4a10['Search Volume'].sum() * media_posicoes_4_a_10        
        # Exibindo o novo DataFrame
        st.header("Base de dados top 4 a 10")
        st.dataframe(df_entre_4a10)
        st.write("Quantidade de palavras no estudo de palavras:" , len(df_entre_4a10))
        st.write("Esperado recebido pelo top 4 a 10: ", soma_busca_top4a10)

        # Criando um DataFrame sobre top 10
        df_palavras_top10 = df_palavras[(df_palavras['Position'] <= 10) & (df_palavras['Search Volume'] > 0)]
        soma_busca_top10 = df_palavras_top10['Search Volume'].sum() * media_posicoes_top10
        # Exibindo o novo DataFrame
        st.header("Base de dados top 10")
        st.dataframe(df_palavras_top10)
        st.write("Quantidade de palavras no estudo de palavras:" , len(df_palavras_top10))
        st.write("Esperado recebido pelo top 10: ", soma_busca_top10)


        #Adicionando palavras a incrementações
        st.header("Base de dados fora do top 10")
        df_fora_top10 = df_palavras[(df_palavras['Search Volume'] > 0)  & (df_palavras['Position'] >= 11)]
        st.dataframe(df_fora_top10)
        st.write("Quantidade de palavras no estudo de palavras:" , len(df_fora_top10))
        df = df_fora_top10

        st.title('Dados completos a serem filtrados de SEO')

        # Sidebar filters for Position
        st.sidebar.header('Filtro de Position')
        Position_range = st.sidebar.slider('Selecione o Intervalo de Position',
                                            min_value=int(df['Position'].min()),
                                            max_value=int(df['Position'].max()),
                                            value=(int(df['Position'].min()), int(df['Position'].max())))

        # Sidebar filters for Search Volume
        st.sidebar.header('Filtro de Search Volume')
        search_volume_range = st.sidebar.slider('Selecione o Intervalo de Search Volume',
                                                min_value=int(df['Search Volume'].min()),
                                                max_value=int(df['Search Volume'].max()),
                                                value=(int(df['Search Volume'].min()), int(df['Search Volume'].max())))

        # Sidebar filters for  Keyword Difficulty
        st.sidebar.header('Filtro de Keyword Difficulty')
        keyword_difficulty_range = st.sidebar.slider('Selecione o Intervalo de  Keyword Difficulty',
                                                        min_value=int(df['Keyword Difficulty'].min()),
                                                        max_value=int(df['Keyword Difficulty'].max()),
                                                        value=(int(df['Keyword Difficulty'].min()), int(df['Keyword Difficulty'].max())))
        
         # Sidebar filters for Clicks
        st.sidebar.header('Filtro de Clicks')
        Clicks_range = st.sidebar.slider('Selecione o Intervalo de Clicks',
                                                        min_value=int(df['Clicks'].min()),
                                                        max_value=int(df['Clicks'].max()),
                                                        value=(int(df['Clicks'].min()), int(df['Clicks'].max())))
        # Sidebar filters for Traffic
        st.sidebar.header('Filtro de Traffic')
        impressoes_range = st.sidebar.slider('Selecione o Intervalo de Traffic',
                                                        min_value=int(df['Traffic'].min()),
                                                        max_value=int(df['Traffic'].max()),
                                                        value=(int(df['Traffic'].min()), int(df['Traffic'].max())))
    
        keyword_intents_options = df["Keyword Intents"].unique()

        valores_categoria = df['Categoria'].unique()

        def filter_by_range(df, column_name, selected_range):
                return df[(df[column_name] >= selected_range[0]) & (df[column_name] <= selected_range[1])]

        # Sidebar widget to collect keyword intents from the user
        st.sidebar.header('Filtro de Keyword Intents')
        intencao_busca = st.sidebar.multiselect('Selecione as Inteções de busca para filtrar', keyword_intents_options)
        st.sidebar.header('Filtro de Categoria de busca')
        selected_valores_categorias = st.sidebar.multiselect('Selecione as Categorias de busca para filtrar', valores_categoria)
            
        st.sidebar.button('Filtrar')

        def apply_filters():
            df_filtrado = filter_by_range(df, 'Position', Position_range)
            df_filtrado = filter_by_range(df_filtrado, 'Search Volume', search_volume_range)
            df_filtrado = filter_by_range(df_filtrado, 'Clicks', Clicks_range)
            df_filtrado = filter_by_range(df_filtrado, 'Traffic', impressoes_range)
            df_filtrado = filter_by_range(df_filtrado, 'Keyword Difficulty', keyword_difficulty_range)
            # Aplicando filtro apenas se opções forem selecionadas
            if intencao_busca:
                df_filtrado = df_filtrado[df_filtrado['Keyword Intents'].isin(intencao_busca)]
            
            # Aplicando filtro apenas se opções forem selecionadas
            if selected_valores_categorias:
                df_filtrado = df_filtrado[df_filtrado['Categoria'].isin(selected_valores_categorias)]
            return df_filtrado
        

        # Aplicar filtros ao DataFrame
        df_filtrado = apply_filters()
        df_filtrado1 = df_filtrado.copy()
        st.dataframe(df_filtrado)
        st.write("Quantidade de palavras no estudo de palavras:" , len(df_filtrado))

        # Criando um DataFrame sobre top 3
        soma_top4a10_para_top3 = df_entre_4a10['Search Volume'].sum() *media_posicoes_1_a_3
        soma_estimativa_top3 = (df_filtrado['Search Volume'].sum() * media_posicoes_1_a_3 + soma_busca_top3 + soma_top4a10_para_top3).round(0).astype(int)
        # Exibindo o novo DataFrame
        st.write("Esperado recebido pelo top 3: ", dados['Sessões executadas'].mean() + soma_estimativa_top3)

        # Criando um DataFrame sobre top 4 a 10
        soma_estimativa_top4a10 = (df_filtrado['Search Volume'].sum() * media_posicoes_4_a_10 + soma_busca_top4a10 + soma_busca_top3).round(0).astype(int)      
        # Exibindo o novo DataFrame
        st.write("Esperado recebido pelo top 4 a 10: ", dados['Sessões executadas'].mean() + soma_estimativa_top4a10)

        # Criando um DataFrame sobre top 10
        soma_estimativa_top10 = (df_filtrado['Search Volume'].sum() * media_posicoes_top10 + soma_busca_top10 + soma_busca_top3).round(0).astype(int)
        # Exibindo o novo DataFrame
        st.write("Esperado recebido pelo top 10: ",dados['Sessões executadas'].mean() + soma_estimativa_top10)

        st.title("Digite o ticket médio e a taxa de conversão do seu cliente")

        # Criando um campo de entrada para o valor do ticket médio
        receita = dados['Transaction_revenue'].mean().round(2)
        ticket_medio = st.text_input("Insira o valor do ticket médio:")
        # Convertendo o valor do ticket médio para float
        try:
            ticket_medio = float(ticket_medio)
        except ValueError:
            st.error("Por favor, insira um valor numérico para o ticket médio.")

        # Exibindo o valor do ticket médio inserido pelo usuário
        if ticket_medio:
            st.write("Valor do ticket médio inserido:", ticket_medio)

        taxa_conversao = st.text_input("Insira o valor da taxa de conversão(forma decimal, exemplo para 2%- 0.02):")
        # Convertendo o valor do ticket médio para float
        try:
            taxa_conversao = float(taxa_conversao)
        except ValueError:
            st.error("Por favor, insira um valor numérico para o ticket médio.")

        # Exibindo o valor do ticket médio inserido pelo usuário
        if ticket_medio:
            st.write("Valor da taxa de conversão inserido:", taxa_conversao)

        st.write("media de receita: ", receita)

        # palavras para o primeiro mês
        st.title("Selecionar palavras chave para trabalhar no primeiro mês")

        # Obter uma lista única de todas as palavras-chave no DataFrame
        palavras_chave_unicas = sorted(df_filtrado['Keyword'].unique())

        # Criar um widget multiselect para selecionar palavras-chave
        palavras_selecionadas = st.multiselect('Selecione palavras-chave:', palavras_chave_unicas)

        # Filtrar o DataFrame com base nas palavras-chave selecionadas
        dados_filtrados = df_filtrado[df_filtrado['Keyword'].isin(palavras_selecionadas)]
         # Filtrar o DataFrame com base nas palavras-chave selecionadas
        df_filtrado = df_filtrado[~df_filtrado['Keyword'].isin(palavras_selecionadas)]
        
        #cálculo da média da receita
        media_receita = dados['Transaction_revenue'].mean()
        media_receita = round(media_receita, 2)

        df_filtrado_Top3_1 = dados['Sessões executadas'].mean() + (dados_filtrados['Search Volume'].sum() * media_posicoes_1_a_3 + soma_busca_top3 + soma_top4a10_para_top3)
        receita_top3_1 = media_receita + (((dados_filtrados['Search Volume'].sum() * media_posicoes_1_a_3 + soma_busca_top3 + soma_top4a10_para_top3) * taxa_conversao) * ticket_medio)
        df_filtrado_Top4a10_1 = dados['Sessões executadas'].mean() + (dados_filtrados['Search Volume'].sum() * media_posicoes_4_a_10 + soma_busca_top4a10 + soma_busca_top3)
        receita_top4a10_1 = media_receita + (((dados_filtrados['Search Volume'].sum() * media_posicoes_4_a_10 + soma_busca_top4a10 + soma_busca_top3) * taxa_conversao) * ticket_medio)
        df_filtrado_Top10_1 = dados['Sessões executadas'].mean() + (dados_filtrados['Search Volume'].sum() * media_posicoes_top10 + soma_busca_top10)
        receita_top10_1 =  media_receita + (((dados_filtrados['Search Volume'].sum() * media_posicoes_top10 + soma_busca_top10) * ticket_medio) * taxa_conversao)

        # Mostrar o DataFrame filtrado na interface do Streamlit
        st.dataframe(dados_filtrados)
        st.write("Esperado top 3: ",df_filtrado_Top3_1)
        st.write("Receita esperada top 3: ", receita_top3_1)
        st.write("Esperado top 4 a 10: ",df_filtrado_Top4a10_1)
        st.write("Receita esperada top 4 a 10: ", receita_top4a10_1)
        st.write("Esperado top 10: ",df_filtrado_Top10_1)
        st.write("Receita esperada top 10: ", receita_top10_1)

        with st.spinner("Aguarde o carregamento"):
            time.sleep(1)


        # palavras para o primeiro mês
        st.title("Selecionar palavras chave para trabalhar no segundo mês")

        # Obter uma lista única de todas as palavras-chave no DataFrame
        palavras_chave_unicas = sorted(df_filtrado['Keyword'].unique())

        # Criar um widget multiselect para selecionar palavras-chave
        palavras_selecionadas = st.multiselect('Selecione palavras-chave:', palavras_chave_unicas)

        # Filtrar o DataFrame com base nas palavras-chave selecionadas
        dados_filtrados = df_filtrado[df_filtrado['Keyword'].isin(palavras_selecionadas)]
         # Filtrar o DataFrame com base nas palavras-chave selecionadas
        df_filtrado = df_filtrado[~df_filtrado['Keyword'].isin(palavras_selecionadas)]

        df_filtrado_Top3_2 = df_filtrado_Top3_1 + (dados_filtrados['Search Volume'].sum() * media_posicoes_1_a_3)
        df_filtrado_Top4a10_2 = df_filtrado_Top4a10_1 + (dados_filtrados['Search Volume'].sum() * media_posicoes_4_a_10)
        df_filtrado_Top10_2 = df_filtrado_Top10_1 + (dados_filtrados['Search Volume'].sum() * media_posicoes_top10)
        receita_top3_2 = receita_top3_1 + (dados_filtrados['Search Volume'].sum() * media_posicoes_1_a_3 * ticket_medio * taxa_conversao)
        receita_top4a10_2 = receita_top4a10_1 + (dados_filtrados['Search Volume'].sum() * media_posicoes_4_a_10 * ticket_medio * taxa_conversao)
        receita_top10_2 = receita_top10_1 + (dados_filtrados['Search Volume'].sum() * media_posicoes_top10 * ticket_medio * taxa_conversao)


        # Mostrar o DataFrame filtrado na interface do Streamlit
        st.dataframe(dados_filtrados)
        st.write("Esperado top 3: ",df_filtrado_Top3_2)
        st.write("Receita esperada top 3: ", receita_top3_2)
        st.write("Esperado top 4 a 10: ",df_filtrado_Top4a10_2)
        st.write("Receita esperada top 4 a 10: ", receita_top4a10_2)
        st.write("Esperado top 10: ",df_filtrado_Top10_2)
        st.write("Receita esperada top 10: ", receita_top10_2)
        with st.spinner("Aguarde o carregamento"):
            time.sleep(1)



        # palavras para o primeiro mês
        st.title("Selecionar palavras chave para trabalhar no terceiro mês")

        # Obter uma lista única de todas as palavras-chave no DataFrame
        palavras_chave_unicas = sorted(df_filtrado['Keyword'].unique())

        # Criar um widget multiselect para selecionar palavras-chave
        palavras_selecionadas = st.multiselect('Selecione palavras-chave:', palavras_chave_unicas)

        # Filtrar o DataFrame com base nas palavras-chave selecionadas
        dados_filtrados = df_filtrado[df_filtrado['Keyword'].isin(palavras_selecionadas)]
         # Filtrar o DataFrame com base nas palavras-chave selecionadas
        df_filtrado = df_filtrado[~df_filtrado['Keyword'].isin(palavras_selecionadas)]

        df_filtrado_Top3_3 = df_filtrado_Top3_2 + (dados_filtrados['Search Volume'].sum() * media_posicoes_1_a_3)
        df_filtrado_Top4a10_3 = df_filtrado_Top4a10_2 + (dados_filtrados['Search Volume'].sum() * media_posicoes_4_a_10)
        df_filtrado_Top10_3 = df_filtrado_Top10_2 + (dados_filtrados['Search Volume'].sum() * media_posicoes_top10)

        receita_top3_3 = receita_top3_2 + (dados_filtrados['Search Volume'].sum() * media_posicoes_1_a_3 * ticket_medio * taxa_conversao)
        receita_top4a10_3 = receita_top4a10_2 + (dados_filtrados['Search Volume'].sum() * media_posicoes_4_a_10 * ticket_medio * taxa_conversao)
        receita_top10_3 = receita_top10_2 + (dados_filtrados['Search Volume'].sum() * media_posicoes_top10 * ticket_medio * taxa_conversao)


        # Mostrar o DataFrame filtrado na interface do Streamlit
        st.dataframe(dados_filtrados)
        st.write("Esperado top 3: ",df_filtrado_Top3_3)
        st.write("Receita esperada top 3: ", receita_top3_3)
        st.write("Esperado top 4 a 10: ",df_filtrado_Top4a10_3)
        st.write("Receita esperada top 4 a 10: ", receita_top4a10_3)
        st.write("Esperado top 10: ",df_filtrado_Top10_3)
        st.write("Receita esperada top 10: ", receita_top10_3)
        with st.spinner("Aguarde o carregamento"):
            time.sleep(1)

        # palavras para o primeiro mês
        st.title("Selecionar palavras chave para trabalhar no quarto mês")

        # Obter uma lista única de todas as palavras-chave no DataFrame
        palavras_chave_unicas = sorted(df_filtrado['Keyword'].unique())

        # Criar um widget multiselect para selecionar palavras-chave
        palavras_selecionadas = st.multiselect('Selecione palavras-chave:', palavras_chave_unicas)

        # Filtrar o DataFrame com base nas palavras-chave selecionadas
        dados_filtrados = df_filtrado[df_filtrado['Keyword'].isin(palavras_selecionadas)]
         # Filtrar o DataFrame com base nas palavras-chave selecionadas
        df_filtrado = df_filtrado[~df_filtrado['Keyword'].isin(palavras_selecionadas)]

        df_filtrado_Top3_4 = df_filtrado_Top3_3 + (dados_filtrados['Search Volume'].sum() * media_posicoes_1_a_3)
        df_filtrado_Top4a10_4 = df_filtrado_Top4a10_3 + (dados_filtrados['Search Volume'].sum() * media_posicoes_4_a_10)
        df_filtrado_Top10_4 = df_filtrado_Top10_3 + (dados_filtrados['Search Volume'].sum() * media_posicoes_top10)
        receita_top3_4 = receita_top3_3 + (dados_filtrados['Search Volume'].sum() * media_posicoes_1_a_3 * ticket_medio * taxa_conversao)
        receita_top4a10_4 = receita_top4a10_3 + (dados_filtrados['Search Volume'].sum() * media_posicoes_4_a_10 * ticket_medio * taxa_conversao)
        receita_top10_4 = receita_top10_3 + (dados_filtrados['Search Volume'].sum() * media_posicoes_top10 * ticket_medio * taxa_conversao)

        # Mostrar o DataFrame filtrado na interface do Streamlit
        st.dataframe(dados_filtrados)
        st.write("Esperado top 3: ",df_filtrado_Top3_4)
        st.write("Receita esperada top 3: ", receita_top3_4)
        st.write("Esperado top 4 a 10: ",df_filtrado_Top4a10_4)
        st.write("Receita esperada top 4 a 10: ", receita_top4a10_4)
        st.write("Esperado top 10: ",df_filtrado_Top10_4)
        st.write("Receita esperada top 10: ", receita_top10_4)
        with st.spinner("Aguarde o carregamento"):
            time.sleep(1)


        # palavras para o primeiro mês
        st.title("Selecionar palavras chave para trabalhar no quinto mês")

        # Obter uma lista única de todas as palavras-chave no DataFrame
        palavras_chave_unicas = sorted(df_filtrado['Keyword'].unique())

        # Criar um widget multiselect para selecionar palavras-chave
        palavras_selecionadas = st.multiselect('Selecione palavras-chave:', palavras_chave_unicas)

        # Filtrar o DataFrame com base nas palavras-chave selecionadas
        dados_filtrados = df_filtrado[df_filtrado['Keyword'].isin(palavras_selecionadas)]
         # Filtrar o DataFrame com base nas palavras-chave selecionadas
        df_filtrado = df_filtrado[~df_filtrado['Keyword'].isin(palavras_selecionadas)]

        df_filtrado_Top3_5 = df_filtrado_Top3_4 + (dados_filtrados['Search Volume'].sum() * media_posicoes_1_a_3)
        df_filtrado_Top4a10_5 = df_filtrado_Top4a10_4 + (dados_filtrados['Search Volume'].sum() * media_posicoes_4_a_10)
        df_filtrado_Top10_5 = df_filtrado_Top10_4 + (dados_filtrados['Search Volume'].sum() * media_posicoes_top10)

        receita_top3_5 = receita_top3_4 + (dados_filtrados['Search Volume'].sum() * media_posicoes_1_a_3 * ticket_medio * taxa_conversao)
        receita_top4a10_5 = receita_top4a10_4 + (dados_filtrados['Search Volume'].sum() * media_posicoes_4_a_10 * ticket_medio * taxa_conversao)
        receita_top10_5 = receita_top10_4 + (dados_filtrados['Search Volume'].sum() * media_posicoes_top10 * ticket_medio * taxa_conversao)

        # Mostrar o DataFrame filtrado na interface do Streamlit
        st.dataframe(dados_filtrados)
        st.write("Esperado top 3: ",df_filtrado_Top3_5)
        st.write("Receita esperada top 3: ", receita_top3_5)
        st.write("Esperado top 4 a 10: ",df_filtrado_Top4a10_5)
        st.write("Receita esperada top 4 a 10: ", receita_top4a10_5)
        st.write("Esperado top 10: ",df_filtrado_Top10_5)
        st.write("Receita esperada top 10: ", receita_top10_5)
        with st.spinner("Aguarde o carregamento"):
            time.sleep(1)


        # palavras para o primeiro mês
        st.title("Selecionar palavras chave para trabalhar no sexto mês")

        # Obter uma lista única de todas as palavras-chave no DataFrame
        palavras_chave_unicas = sorted(df_filtrado['Keyword'].unique())

        # Criar um widget multiselect para selecionar palavras-chave
        palavras_selecionadas = st.multiselect('Selecione palavras-chave:', palavras_chave_unicas)

        # Filtrar o DataFrame com base nas palavras-chave selecionadas
        dados_filtrados = df_filtrado[df_filtrado['Keyword'].isin(palavras_selecionadas)]
         # Filtrar o DataFrame com base nas palavras-chave selecionadas
        df_filtrado = df_filtrado[~df_filtrado['Keyword'].isin(palavras_selecionadas)]

        df_filtrado_Top3_6 = df_filtrado_Top3_5 + (dados_filtrados['Search Volume'].sum() * media_posicoes_1_a_3)
        df_filtrado_Top4a10_6 = df_filtrado_Top4a10_5 + (dados_filtrados['Search Volume'].sum() * media_posicoes_4_a_10)
        df_filtrado_Top10_6 = df_filtrado_Top10_5 + (dados_filtrados['Search Volume'].sum() * media_posicoes_top10)
        receita_top3_6 = receita_top3_5 + (dados_filtrados['Search Volume'].sum() * media_posicoes_1_a_3 * ticket_medio * taxa_conversao)
        receita_top4a10_6 = receita_top4a10_5 + (dados_filtrados['Search Volume'].sum() * media_posicoes_4_a_10 * ticket_medio * taxa_conversao)
        receita_top10_6 = receita_top10_5 + (dados_filtrados['Search Volume'].sum() * media_posicoes_top10 * ticket_medio * taxa_conversao)


        # Mostrar o DataFrame filtrado na interface do Streamlit
        st.dataframe(dados_filtrados)
        st.write("Esperado top 3: ",df_filtrado_Top3_6)
        st.write("Receita esperada top 3: ", receita_top3_6)
        st.write("Esperado top 4 a 10: ",df_filtrado_Top4a10_6)
        st.write("Receita esperada top 4 a 10: ", receita_top4a10_6)
        st.write("Esperado top 10: ",df_filtrado_Top10_6)
        st.write("Receita esperada top 10: ", receita_top10_6)
        with st.spinner("Aguarde o carregamento"):
            time.sleep(1)

        st.title("Palavras não utilizadas no mês a mês")
        st.dataframe(df_filtrado)
        st.write("Palavras restantes: ", len(df_filtrado))
             
        st.title("Tabela demonstrando o crescimento mensal médio")
        
        dados['Top 3'] = dados['Sessões executadas'].copy()
        dados['Crescimento Top 3(%)'] = (((dados['Top 3'] - dados['Sessões executadas'] ) / dados['Sessões executadas']) * 100).round(0).astype(str) + "%"
        dados['Receita top 3'] = dados['Transaction_revenue'].copy()
        dados['Crescimento de Receita Top 3(%)'] = (((dados['Receita top 3'] - dados['Transaction_revenue'] ) / dados['Transaction_revenue']) * 100).round(0).astype(str) + "%"
        dados['Top 4 a 10'] = dados['Sessões executadas'].copy()
        dados['Crescimento Top 4 a 10(%)'] = (((dados['Top 4 a 10'] - dados['Sessões executadas'] ) / dados['Sessões executadas']) * 100).round(0).astype(str) + "%"
        dados['Receita top 4 a 10'] = dados['Transaction_revenue'].copy()
        dados['Crescimento de Receita Top 4 a 10(%)'] = (((dados['Receita top 4 a 10'] - dados['Transaction_revenue'] ) / dados['Transaction_revenue']) * 100).round(0).astype(str) + "%"
        dados['Top 10'] = dados['Sessões executadas'].copy() 
        dados['Crescimento Top 10(%)'] = (((dados['Top 10'] - dados['Sessões executadas'] ) / dados['Sessões executadas']) * 100).round(0).astype(str) + "%"
        dados['Receita Top 10'] = dados['Receita top 4 a 10'].copy()
        dados['Crescimento de Receita Top 10(%)'] = (((dados['Receita Top 10'] - dados['Transaction_revenue'] ) / dados['Transaction_revenue']) * 100).round(0).astype(str) + "%"

        
        st.write("Utilizando todas as ", len(df_filtrado1), "filtradas no estudo")

        df_mes = dados.copy()
        # Loop de 6 meses multiplicando pelo crescimento percentual

        # Novo valor para o último item da coluna "Month"
        novo_valor = "Último mês"

        # Alterando o valor do último item da coluna "Month"
        dados.at[dados.index[-1], 'Month'] = novo_valor
        
        # Adicionar novo valor ao DataFrame de dados
        nova_data = "Média da empresa"
        novo_registro = pd.DataFrame({'Month': 'Média da empresa', 
                                    'Transaction_revenue': [media_receita],
                                    'Sessões executadas': dados['Sessões executadas'].mean().round(0).astype(int), 
                                    'Top 3': dados['Sessões executadas'].mean().round(0).astype(int) + soma_estimativa_top3,
                                    'Crescimento Top 3(%)': (((dados['Top 3'] - dados['Sessões executadas']) / dados['Sessões executadas']) * 100).iloc[-1].round(0).astype(str) + "%",
                                    'Receita top 3': (media_receita + ((df_filtrado1['Search Volume'].sum() * media_posicoes_1_a_3 + soma_busca_top3 + soma_top4a10_para_top3) * taxa_conversao) * ticket_medio).round(2),
                                    'Crescimento de Receita Top 3(%)': (((dados['Receita top 3'] - dados['Transaction_revenue'] ) / dados['Transaction_revenue']) * 100).iloc[-1].round(0).astype(str) + "%",
                                    'Top 4 a 10':dados['Sessões executadas'].mean().round(0).astype(int) + soma_estimativa_top4a10,
                                    'Crescimento Top 4 a 10(%)': (((dados['Top 4 a 10'] - dados['Sessões executadas']) / dados['Sessões executadas']) * 100).iloc[-1].round(0).astype(str) + "%",
                                    'Receita top 4 a 10': (media_receita + ((df_filtrado1['Search Volume'].sum() * media_posicoes_4_a_10 + soma_busca_top3 + soma_top4a10_para_top3) * taxa_conversao) * ticket_medio).round(2),
                                    'Crescimento de Receita Top 4 a 10(%)': (((dados['Receita top 4 a 10'] - dados['Transaction_revenue'] ) / dados['Transaction_revenue']) * 100).iloc[-1].round(0).astype(str) + "%",                                   
                                    'Top 10': dados['Sessões executadas'].mean().round(0).astype(int) + soma_estimativa_top10,
                                    'Crescimento Top 10(%)': (((dados['Top 10'] - dados['Sessões executadas']) / dados['Sessões executadas']) * 100).iloc[-1].round(0).astype(str) + "%",
                                    'Receita Top 10': (media_receita + ((df_filtrado1['Search Volume'].sum() * media_posicoes_top10 + soma_busca_top3 + soma_top4a10_para_top3))),# * taxa_conversao) * ticket_medio).round(2),
                                    'Crescimento de Receita Top 10(%)': (((dados['Receita Top 10'] - dados['Transaction_revenue'] ) / dados['Transaction_revenue']) * 100).iloc[-1].round(0).astype(str) + "%",
                                    })
        
        dados = pd.concat([dados, novo_registro], ignore_index=True)

        # Adicionar novo valor ao DataFrame de dados
        nova_data2 = "Após 6 meses"
        novo_registro2 = pd.DataFrame({'Month': [nova_data2], 
                                        'Transaction_revenue': media_receita,
                                        'Sessões executadas': dados['Sessões executadas'].mean().round(0).astype(int), 
                                        'Top 3': dados['Sessões executadas'].mean().round(0).astype(int) + soma_estimativa_top3,
                                        'Crescimento Top 3(%)': (((dados['Top 3'] - dados['Sessões executadas']) / dados['Sessões executadas']) * 100).iloc[-1].round(0).astype(str) + "%",
                                        'Receita top 3': (media_receita + ((df_filtrado1['Search Volume'].sum() * media_posicoes_1_a_3 + soma_busca_top3 + soma_top4a10_para_top3) * taxa_conversao) * ticket_medio).round(2),
                                        'Crescimento de Receita Top 3(%)': (((dados['Receita top 3'] - dados['Transaction_revenue']) / dados['Transaction_revenue']) * 100).iloc[-1].round(0).astype(str) + "%",
                                        'Top 4 a 10':dados['Sessões executadas'].mean().round(0).astype(int) + soma_estimativa_top4a10,
                                        'Crescimento Top 4 a 10(%)': (((dados['Top 4 a 10'] - dados['Sessões executadas']) / dados['Sessões executadas']) * 100).iloc[-1].round(0).astype(str) + "%",
                                        'Receita top 4 a 10': (media_receita + ((df_filtrado1['Search Volume'].sum() * media_posicoes_4_a_10 + soma_busca_top3 + soma_top4a10_para_top3) * taxa_conversao) * ticket_medio).round(2),
                                        'Crescimento de Receita Top 4 a 10(%)' : (((dados['Receita top 4 a 10'] - dados['Transaction_revenue']) / dados['Transaction_revenue']) * 100).iloc[-1].round(0).astype(str) + "%",
                                        'Top 10': dados['Sessões executadas'].mean().round(0).astype(int) + soma_estimativa_top10,
                                        'Crescimento Top 10(%)': (((dados['Top 10'] - dados['Sessões executadas']) / dados['Sessões executadas']) * 100).iloc[-1].round(0).astype(str) + "%",
                                        'Receita Top 10': (media_receita + ((df_filtrado1['Search Volume'].sum() * media_posicoes_top10 + soma_busca_top3 + soma_top4a10_para_top3))),# * taxa_conversao) * ticket_medio).round(2),
                                        'Crescimento de Receita Top 10(%)': (((dados['Receita Top 10'] - dados['Transaction_revenue']) / dados['Transaction_revenue']) * 100).iloc[-1].round(0).astype(str) + "%"})
        dados = pd.concat([dados, novo_registro2], ignore_index=True)
        traco  =  "-" 
           
        dados.at[dados.index[-2], 'Crescimento Top 3(%)'] = traco
        dados.at[dados.index[-2], 'Crescimento Top 4 a 10(%)'] = traco
        dados.at[dados.index[-2], 'Crescimento Top 10(%)'] = traco
        dados.at[dados.index[-2], 'Top 3'] = traco
        dados.at[dados.index[-2], 'Top 4 a 10'] = traco
        dados.at[dados.index[-2], 'Receita top 3'] = traco
        dados.at[dados.index[-2], 'Receita top 4 a 10'] = traco
        dados.at[dados.index[-2], 'Receita Top 10'] = traco
        dados.at[dados.index[-2], 'Crescimento de Receita Top 3(%)'] = traco
        dados.at[dados.index[-2], 'Crescimento de Receita Top 4 a 10(%)'] = traco
        dados.at[dados.index[-2], 'Crescimento de Receita Top 10(%)'] = traco

        st.dataframe(dados.tail(3)) 

        st.write("Crescimento mês a mês:")
        
        #acrescentar nova linha no df
        nova_data = df_mes['Month'].iloc[-1] + pd.DateOffset(months=1)
        novo_registro = pd.DataFrame({
            'Month': nova_data,
            'Transaction_revenue': media_receita,
            'Sessões executadas': df_mes['Sessões executadas'].mean().round(0).astype(int),
            'Top 3': [round(df_filtrado_Top3_1,0)],
            'Crescimento Top 3(%)': (((df_mes['Top 3'] - df_mes['Sessões executadas']) / df_mes['Sessões executadas']) * 100).iloc[-1].round(0).astype(str) + "%",
            'Top 4 a 10': round(df_filtrado_Top4a10_1, 0 ),
            'Crescimento Top 4 a 10(%)': (((df_mes['Top 4 a 10'] - df_mes['Sessões executadas']) / df_mes['Sessões executadas']) * 100).iloc[-1].round(0).astype(str) + "%",
            'Top 10': round(df_filtrado_Top10_1, 0),
            'Crescimento Top 10(%)': (((df_mes['Top 10'] - df_mes['Sessões executadas']) / df_mes['Sessões executadas']) * 100).iloc[-1].round(0).astype(str) + "%",
            "Receita top 3": receita_top3_1,
            'Receita top 4 a 10' : receita_top4a10_1,
            'Receita Top 10': receita_top10_1,  
            'Crescimento de Receita Top 3(%)': (((df_mes['Receita top 3'] - df_mes['Transaction_revenue']) / df_mes['Transaction_revenue']) * 100).iloc[-1].round(0).astype(str) + "%",
            'Crescimento de Receita Top 4 a 10(%)': (((df_mes['Receita top 4 a 10'] - df_mes['Transaction_revenue']) / df_mes['Transaction_revenue']) * 100).iloc[-1].round(0).astype(str) + "%",
            'Crescimento de Receita Top 10(%)' : (((df_mes['Receita Top 10'] - df_mes['Transaction_revenue']) / df_mes['Transaction_revenue']) * 100).iloc[-1].round(0).astype(str) + "%",
        }, index=[0])
        df_mes = pd.concat([df_mes, novo_registro], ignore_index=True)

        nova_data = df_mes['Month'].iloc[-1] + pd.DateOffset(months=1)
        novo_registro = pd.DataFrame({
            'Month': nova_data,
            'Transaction_revenue': media_receita,
            'Sessões executadas': df_mes['Sessões executadas'].mean().round(0).astype(int),
            'Top 3': [round(df_filtrado_Top3_2,0)],
            'Crescimento Top 3(%)': (((df_mes['Top 3'] - df_mes['Sessões executadas']) / df_mes['Sessões executadas']) * 100).iloc[-1].round(0).astype(str) + "%",
            'Top 4 a 10': round(df_filtrado_Top4a10_2, 0 ),
            'Crescimento Top 4 a 10(%)': (((df_mes['Top 4 a 10'] - df_mes['Sessões executadas']) / df_mes['Sessões executadas']) * 100).iloc[-1].round(0).astype(str) + "%",
            'Top 10': round(df_filtrado_Top10_2, 0),
            'Crescimento Top 10(%)': (((df_mes['Top 10'] - df_mes['Sessões executadas']) / df_mes['Sessões executadas']) * 100).iloc[-1].round(0).astype(str) + "%",
            "Receita top 3": receita_top3_2,
            'Receita top 4 a 10' : receita_top4a10_2,
            'Receita Top 10': receita_top10_2,  
            'Crescimento de Receita Top 3(%)': (((df_mes['Receita top 3'] - df_mes['Transaction_revenue']) / df_mes['Transaction_revenue']) * 100).iloc[-1].round(0).astype(str) + "%",
            'Crescimento de Receita Top 4 a 10(%)': (((df_mes['Receita top 4 a 10'] - df_mes['Transaction_revenue']) / df_mes['Transaction_revenue']) * 100).iloc[-1].round(0).astype(str) + "%",
            'Crescimento de Receita Top 10(%)' : (((df_mes['Receita Top 10'] - df_mes['Transaction_revenue']) / df_mes['Transaction_revenue']) * 100).iloc[-1].round(0).astype(str) + "%",
        }, index=[0])
        df_mes = pd.concat([df_mes, novo_registro], ignore_index=True)

        nova_data = df_mes['Month'].iloc[-1] + pd.DateOffset(months=1)
        novo_registro = pd.DataFrame({
            'Month': nova_data,
            'Transaction_revenue': media_receita,
            'Sessões executadas': df_mes['Sessões executadas'].mean().round(0).astype(int),
            'Top 3': [round(df_filtrado_Top3_3,0)],
            'Crescimento Top 3(%)': (((df_mes['Top 3'] - df_mes['Sessões executadas']) / df_mes['Sessões executadas']) * 100).iloc[-1].round(0).astype(str) + "%",
            'Top 4 a 10': round(df_filtrado_Top4a10_3, 0 ),
            'Crescimento Top 4 a 10(%)': (((df_mes['Top 4 a 10'] - df_mes['Sessões executadas']) / df_mes['Sessões executadas']) * 100).iloc[-1].round(0).astype(str) + "%",
            'Top 10': round(df_filtrado_Top10_3, 0),
            'Crescimento Top 10(%)': (((df_mes['Top 10'] - df_mes['Sessões executadas']) / df_mes['Sessões executadas']) * 100).iloc[-1].round(0).astype(str) + "%",
            "Receita top 3": receita_top3_3,
            'Receita top 4 a 10' : receita_top4a10_3,
            'Receita Top 10': receita_top10_3,  
            'Crescimento de Receita Top 3(%)': (((df_mes['Receita top 3'] - df_mes['Transaction_revenue']) / df_mes['Transaction_revenue']) * 100).iloc[-1].round(0).astype(str) + "%",
            'Crescimento de Receita Top 4 a 10(%)': (((df_mes['Receita top 4 a 10'] - df_mes['Transaction_revenue']) / df_mes['Transaction_revenue']) * 100).iloc[-1].round(0).astype(str) + "%",
            'Crescimento de Receita Top 10(%)' : (((df_mes['Receita Top 10'] - df_mes['Transaction_revenue']) / df_mes['Transaction_revenue']) * 100).iloc[-1].round(0).astype(str) + "%",
        }, index=[0])
        df_mes = pd.concat([df_mes, novo_registro], ignore_index=True)

        nova_data = df_mes['Month'].iloc[-1] + pd.DateOffset(months=1)
        novo_registro = pd.DataFrame({
            'Month': nova_data,
            'Transaction_revenue': media_receita,
            'Sessões executadas': df_mes['Sessões executadas'].mean().round(0).astype(int),
            'Top 3': [round(df_filtrado_Top3_4,0)],
            'Crescimento Top 3(%)': (((df_mes['Top 3'] - df_mes['Sessões executadas']) / df_mes['Sessões executadas']) * 100).iloc[-1].round(0).astype(str) + "%",
            'Top 4 a 10': round(df_filtrado_Top4a10_4, 0 ),
            'Crescimento Top 4 a 10(%)': (((df_mes['Top 4 a 10'] - df_mes['Sessões executadas']) / df_mes['Sessões executadas']) * 100).iloc[-1].round(0).astype(str) + "%",
            'Top 10': round(df_filtrado_Top10_4, 0),
            'Crescimento Top 10(%)': (((df_mes['Top 10'] - df_mes['Sessões executadas']) / df_mes['Sessões executadas']) * 100).iloc[-1].round(0).astype(str) + "%",
            "Receita top 3": receita_top3_4,
            'Receita top 4 a 10' : receita_top4a10_4,
            'Receita Top 10': receita_top10_4,  
            'Crescimento de Receita Top 3(%)': (((df_mes['Receita top 3'] - df_mes['Transaction_revenue']) / df_mes['Transaction_revenue']) * 100).iloc[-1].round(0).astype(str) + "%",
            'Crescimento de Receita Top 4 a 10(%)': (((df_mes['Receita top 4 a 10'] - df_mes['Transaction_revenue']) / df_mes['Transaction_revenue']) * 100).iloc[-1].round(0).astype(str) + "%",
            'Crescimento de Receita Top 10(%)' : (((df_mes['Receita Top 10'] - df_mes['Transaction_revenue']) / df_mes['Transaction_revenue']) * 100).iloc[-1].round(0).astype(str) + "%",
        }, index=[0])
        df_mes = pd.concat([df_mes, novo_registro], ignore_index=True)

        nova_data = df_mes['Month'].iloc[-1] + pd.DateOffset(months=1)
        novo_registro = pd.DataFrame({
            'Month': nova_data,
            'Transaction_revenue': media_receita,
            'Sessões executadas': df_mes['Sessões executadas'].mean().round(0).astype(int),
            'Top 3': [round(df_filtrado_Top3_5,0)],
            'Crescimento Top 3(%)': (((df_mes['Top 3'] - df_mes['Sessões executadas']) / df_mes['Sessões executadas']) * 100).iloc[-1].round(0).astype(str) + "%",
            'Top 4 a 10': round(df_filtrado_Top4a10_5, 0 ),
            'Crescimento Top 4 a 10(%)': (((df_mes['Top 4 a 10'] - df_mes['Sessões executadas']) / df_mes['Sessões executadas']) * 100).iloc[-1].round(0).astype(str) + "%",
            'Top 10': round(df_filtrado_Top10_5, 0),
            'Crescimento Top 10(%)': (((df_mes['Top 10'] - df_mes['Sessões executadas']) / df_mes['Sessões executadas']) * 100).iloc[-1].round(0).astype(str) + "%",
            "Receita top 3": receita_top3_5,
            'Receita top 4 a 10' : receita_top4a10_5,
            'Receita Top 10': receita_top10_5,  
            'Crescimento de Receita Top 3(%)': (((df_mes['Receita top 3'] - df_mes['Transaction_revenue']) / df_mes['Transaction_revenue']) * 100).iloc[-1].round(0).astype(str) + "%",
            'Crescimento de Receita Top 4 a 10(%)': (((df_mes['Receita top 4 a 10'] - df_mes['Transaction_revenue']) / df_mes['Transaction_revenue']) * 100).iloc[-1].round(0).astype(str) + "%",
            'Crescimento de Receita Top 10(%)' : (((df_mes['Receita Top 10'] - df_mes['Transaction_revenue']) / df_mes['Transaction_revenue']) * 100).iloc[-1].round(0).astype(str) + "%",
        }, index=[0])
        df_mes = pd.concat([df_mes, novo_registro], ignore_index=True)

        nova_data = df_mes['Month'].iloc[-1] + pd.DateOffset(months=1)
        novo_registro = pd.DataFrame({
            'Month': nova_data,
            'Transaction_revenue': media_receita,
            'Sessões executadas': df_mes['Sessões executadas'].mean().round(0).astype(int),
            'Top 3': [round(df_filtrado_Top3_6,0)],
            'Crescimento Top 3(%)': (((df_mes['Top 3'] - df_mes['Sessões executadas']) / df_mes['Sessões executadas']) * 100).iloc[-1].round(0).astype(str) + "%",
            'Top 4 a 10': round(df_filtrado_Top4a10_6, 0 ),
            'Crescimento Top 4 a 10(%)': (((df_mes['Top 4 a 10'] - df_mes['Sessões executadas']) / df_mes['Sessões executadas']) * 100).iloc[-1].round(0).astype(str) + "%",
            'Top 10': round(df_filtrado_Top10_6, 0),
            'Crescimento Top 10(%)': (((df_mes['Top 10'] - df_mes['Sessões executadas']) / df_mes['Sessões executadas']) * 100).iloc[-1].round(0).astype(str) + "%",
        "Receita top 3": receita_top3_6,
            'Receita top 4 a 10' : receita_top4a10_6,
            'Receita Top 10': receita_top10_6,  
            'Crescimento de Receita Top 3(%)': (((df_mes['Receita top 3'] - df_mes['Transaction_revenue']) / df_mes['Transaction_revenue']) * 100).iloc[-1].round(0).astype(str) + "%",
            'Crescimento de Receita Top 4 a 10(%)': (((df_mes['Receita top 4 a 10'] - df_mes['Transaction_revenue']) / df_mes['Transaction_revenue']) * 100).iloc[-1].round(0).astype(str) + "%",
            'Crescimento de Receita Top 10(%)' : (((df_mes['Receita Top 10'] - df_mes['Transaction_revenue']) / df_mes['Transaction_revenue']) * 100).iloc[-1].round(0).astype(str) + "%",
        }, index=[0])
        df_mes = pd.concat([df_mes, novo_registro], ignore_index=True)

        st.dataframe(df_mes)

    
main()


# In[ ]:


# !streamlit run app.py

