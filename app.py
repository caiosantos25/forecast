#!/usr/bin/env python
# coding: utf-8

def main():
    !pip install agg
    import matplotlib
    matplotlib.use("agg")
    import matplotlib.pyplot as plt
    import streamlit as st
    import pandas as pd
    from json import loads
    import time
    import numpy as np
    import pandas as pd
    # import matplotlib.pyplot as plt
    # import scipy
    # import warnings
    st.title("Olá Cadastrer")
    st.write("texto 1")
    
    st.header("UPLOAD arquivo de .csv com os dados sobre sessões da empresa")
    arquivo = st.file_uploader('Suba seu arquivo csv', type = 'csv', key='arquivo')
    if arquivo:
        st.write("Nome do arquivo: ", arquivo)
        colunas_selecionadas = ['Month','Sessions']
        dados = pd.read_csv(arquivo, parse_dates = True, usecols=colunas_selecionadas)
        dados['Sessões executadas'] = dados['Sessions']
        dados['Month'] = pd.to_datetime(dados['Month'], format='%d/%m/%Y')
        dados = dados.sort_values(by='Month')
        dados = dados.drop(['Sessions'], axis = 1)
        st.dataframe(dados)
        # Criar o gráfico de linha
        fig, ax = plt.subplots()
        
        ax.plot(dados['Month'], dados['Sessões executadas'], marker='o', linestyle='-', color='b', label='CTR')

        # Adicionar rótulos aos eixos
        plt.xlabel('Meses')
        ax.set_ylabel('Sessões')

        # Adicionar título ao gráfico
        ax.set_title('Gráfico de Linha - Meses X Sessões')

        # Adicionar legenda
        ax.legend()
        plt.xticks(rotation=25)
        # Exibir o gráfico
        st.pyplot(fig)
        
        # Criar um dicionário com os dados
        dados_ctr_crescimento = {
            'Posicao antes': list(range(1, 11)),  # Coluna 'Posicao' de 1 a 10
            'Posicao depois': list(range(0, 10)),  # Coluna 'Posicao' de 1 a 10
            'Crescimento do CTR': [ 0, 0.745, 0.434, 0.319, 0.326, 0.293, 0.235, 0.205, 0.236, 0.112]
        }

        # Criar o DataFrame
        df_crescimento = pd.DataFrame(dados_ctr_crescimento)
        # df = df.drop(['Posicao'], axis = 1)
        # Imprimir o DataFrame
        st.header("Estudo sobre crescimento do CTR")
        st.write(df_crescimento)
        df1 = dados.copy()
        df2 = dados.copy()
        df3 = dados.copy()
        df4 = dados.copy()
        df5 = dados.copy()
        df6 = dados.copy()
        df7 = dados.copy()
        df8 = dados.copy()
        df9 = dados.copy()
        df10 = dados.copy()
    else:
        st.error("Ainda não possuo um arquivo .csv")
        
    st.header("Loading")
    with st.spinner("Aguarde o carregamento"):
        time.sleep(3)
    
    st.header("UPLOAD arquivo de .csv com os dados sobre estudo de kw")
    arquivo2 = st.file_uploader('Suba seu arquivo csv', type = 'csv', key='arquivo2')
    if arquivo2:
        df_palavras = pd.read_csv(arquivo2)
        df_palavras = df_palavras[['Palavra-chave', 'Semrush']]
        df_palavras['Semrush'] = pd.to_numeric(df_palavras['Semrush'], errors='coerce')
        df_palavras = df_palavras[df_palavras['Semrush'] < 10]
        df_palavras = df_palavras.rename(columns={'Semrush': 'Numeros'})
        # Exibir o resultado
        st.dataframe(df_palavras)
        # Adicionando 10 colunas no df_palavras
        for i in range(1, 10):
            posicao_antes_col = f'{i}'
            df_palavras[posicao_antes_col] = df_palavras['Numeros']-i+1
            df_palavras[posicao_antes_col] = df_palavras[posicao_antes_col].map(df_crescimento.set_index('Posicao antes')['Crescimento do CTR'])
            df_palavras = df_palavras.ffill(axis=1)
        df_palavras = df_palavras.drop(['Palavra-chave'], axis = 1)
        
        # Realizando a soma acumulada a partir da coluna "2"
        df_palavras.iloc[:, 1:] = df_palavras.iloc[:, 1:].cumsum(axis=1)
        # Obtendo todas as colunas numéricas (excluindo 'Numeros' se necessário)
        colunas_numericas = df_palavras.columns
        # Inicializando um dicionário para armazenar as médias
        medias_por_coluna = {}

        # Calculando a média para cada coluna
        for coluna in colunas_numericas:
            media_coluna = df_palavras[coluna].mean()
            medias_por_coluna[coluna] = media_coluna

        # Exibindo as médias
        print("Médias por coluna:")
        for coluna, media in medias_por_coluna.items():
            print(f"{coluna}: {media}")

        # Criando um DataFrame a partir do dicionário de médias
        df_medias = pd.DataFrame(list(medias_por_coluna.items()), columns=['Cresicmento de posições', 'Média'])
        df_medias = df_medias.drop(0)
        # Exibindo o novo DataFrame
        st.header("Crescimento médio por melhora de palavra chave")
        st.write(df_medias)
        # Obter o último valor da coluna 'Sessões executadas'
        média = dados['Sessões executadas'].mean()

        # Loop de 12 meses multiplicando pelo crescimento percentual
        for j in range(12):
            for i in range(1):
                crescimento_percentual = df_medias['Média'][1]
                novo_valor = média * (1 + crescimento_percentual)
                ultimo_valor = novo_valor

                # Adicionar novo valor ao DataFrame de dados
                nova_data = df1['Month'].iloc[-1] + pd.DateOffset(months=1)
        #         print(nova_data)
                novo_registro = pd.DataFrame({'Month': [nova_data], 'Sessões executadas': novo_valor})
        #         print(novo_registro)
                df1 = pd.concat([df1, novo_registro], ignore_index=True)
            
            # Obter o último valor da coluna 'Sessões executadas'
        média = dados['Sessões executadas'].mean()

        # Loop de 6 meses multiplicando pelo crescimento percentual
        for j in range(12):
            for i in range(1):
                crescimento_percentual = df_medias['Média'][2]
                novo_valor = média * (1 + crescimento_percentual)
                ultimo_valor = novo_valor

                # Adicionar novo valor ao DataFrame de dados
                nova_data = df2['Month'].iloc[-1] + pd.DateOffset(months=1)
        #         print(nova_data)
                novo_registro = pd.DataFrame({'Month': [nova_data], 'Sessões executadas': novo_valor})
        #         print(novo_registro)
                df2 = pd.concat([df2, novo_registro], ignore_index=True)
            # Obter o último valor da coluna 'Sessões executadas'
        média = dados['Sessões executadas'].mean()

        # Loop de 6 meses multiplicando pelo crescimento percentual
        for j in range(12):
            for i in range(1):
                crescimento_percentual = df_medias['Média'][3]
                novo_valor = média * (1 + crescimento_percentual)
                ultimo_valor = novo_valor

                # Adicionar novo valor ao DataFrame de dados
                nova_data = df3['Month'].iloc[-1] + pd.DateOffset(months=1)
        #         print(nova_data)
                novo_registro = pd.DataFrame({'Month': [nova_data], 'Sessões executadas': novo_valor})
        #         print(novo_registro)
                df3 = pd.concat([df3, novo_registro], ignore_index=True)
            # Obter o último valor da coluna 'Sessões executadas'
        média = dados['Sessões executadas'].mean()

        # Loop de 6 meses multiplicando pelo crescimento percentual
        for j in range(12):
            for i in range(1):
                crescimento_percentual = df_medias['Média'][4]
                novo_valor = média * (1 + crescimento_percentual)
                ultimo_valor = novo_valor

                # Adicionar novo valor ao DataFrame de dados
                nova_data = df4['Month'].iloc[-1] + pd.DateOffset(months=1)
        #         print(nova_data)
                novo_registro = pd.DataFrame({'Month': [nova_data], 'Sessões executadas': novo_valor})
        #         print(novo_registro)
                df4 = pd.concat([df4, novo_registro], ignore_index=True)
        # Obter o último valor da coluna 'Sessões executadas'
        média = dados['Sessões executadas'].mean()

        # Loop de 6 meses multiplicando pelo crescimento percentual
        for j in range(12):
            for i in range(1):
                crescimento_percentual = df_medias['Média'][5]
                novo_valor = média * (1 + crescimento_percentual)
                ultimo_valor = novo_valor

                # Adicionar novo valor ao DataFrame de dados
                nova_data = df5['Month'].iloc[-1] + pd.DateOffset(months=1)
        #         print(nova_data)
                novo_registro = pd.DataFrame({'Month': [nova_data], 'Sessões executadas': novo_valor})
        #         print(novo_registro)
                df5 = pd.concat([df5, novo_registro], ignore_index=True)
            # Obter o último valor da coluna 'Sessões executadas'
        média = dados['Sessões executadas'].mean()

        # Loop de 6 meses multiplicando pelo crescimento percentual
        for j in range(12):
            for i in range(1):
                crescimento_percentual = df_medias['Média'][6]
                novo_valor = média * (1 + crescimento_percentual)
                ultimo_valor = novo_valor

                # Adicionar novo valor ao DataFrame de dados
                nova_data = df6['Month'].iloc[-1] + pd.DateOffset(months=1)
        #         print(nova_data)
                novo_registro = pd.DataFrame({'Month': [nova_data], 'Sessões executadas': novo_valor})
        #         print(novo_registro)
                df6 = pd.concat([df6, novo_registro], ignore_index=True)
        # Obter o último valor da coluna 'Sessões executadas'
        média = dados['Sessões executadas'].mean()

        # Loop de 6 meses multiplicando pelo crescimento percentual
        for j in range(12):
            for i in range(1):
                crescimento_percentual = df_medias['Média'][7]
                novo_valor = média * (1 + crescimento_percentual)
                ultimo_valor = novo_valor

                # Adicionar novo valor ao DataFrame de dados
                nova_data = df7['Month'].iloc[-1] + pd.DateOffset(months=1)
        #         print(nova_data)
                novo_registro = pd.DataFrame({'Month': [nova_data], 'Sessões executadas': novo_valor})
        #         print(novo_registro)
                df7 = pd.concat([df7, novo_registro], ignore_index=True)
            # Obter o último valor da coluna 'Sessões executadas'
        média = dados['Sessões executadas'].mean()

        # Loop de 6 meses multiplicando pelo crescimento percentual
        for j in range(12):
            for i in range(1):
                crescimento_percentual = df_medias['Média'][8]
                novo_valor = média * (1 + crescimento_percentual)
                ultimo_valor = novo_valor

                # Adicionar novo valor ao DataFrame de dados
                nova_data = df8['Month'].iloc[-1] + pd.DateOffset(months=1)
        #         print(nova_data)
                novo_registro = pd.DataFrame({'Month': [nova_data], 'Sessões executadas': novo_valor})
        #         print(novo_registro)
                df8 = pd.concat([df8, novo_registro], ignore_index=True)
        # Obter o último valor da coluna 'Sessões executadas'
        média = dados['Sessões executadas'].mean()

        # Loop de 6 meses multiplicando pelo crescimento percentual
        for j in range(12):
            for i in range(1):
                crescimento_percentual = df_medias['Média'][9]
                novo_valor = média * (1 + crescimento_percentual)
                ultimo_valor = novo_valor

                # Adicionar novo valor ao DataFrame de dados
                nova_data = df9['Month'].iloc[-1] + pd.DateOffset(months=1)
        #         print(nova_data)
                novo_registro = pd.DataFrame({'Month': [nova_data], 'Sessões executadas': novo_valor})
        #         print(novo_registro)
                df9 = pd.concat([df9, novo_registro], ignore_index=True)

        # # Especifique os DataFrames que deseja plotar
        dataframes_para_plotar = [df1, df2, df3, df4, df5, df6, df7, df8, df9]
        
        # Plotar gráfico usando matplotlib
        fig, ax = plt.subplots()

        # Crie um gráfico de linha para cada DataFrame
        for i, dataframe in enumerate(dataframes_para_plotar, start=1):
            ax.plot(dataframe['Month'], dataframe['Sessões executadas'], label=f'Quantidade de posições melhoradas {i}', marker='o', linestyle='-')

        # Adicione rótulos aos eixos
        ax.set_xlabel('Meses')
        ax.set_ylabel('Sessões executadas')

        # Adicione título ao gráfico
        ax.set_title('Gráfico de Linha - Meses X Sessões executadas para df1, df2, ..., df9')

        # Adicione legenda
        ax.legend()

        # Exiba o gráfico
        st.pyplot(fig)


        # Lista de DataFrames para plotar
        dataframes_para_plotar = [df1, df2, df3, df4, df5, df6, df7, df8, df9]

         # Exibir DataFrames no Streamlit
        for i, dataframe in enumerate(dataframes_para_plotar, start=1):

            # Criar uma nova figura para cada gráfico
            fig, ax = plt.subplots()

            # Plote a linha principal
            ax.plot(dataframe['Month'], dataframe['Sessões executadas'], label=f'df{i}', marker='o', linestyle='-', color='black')

            # Adicione intervalo de confiança
            conf_int = 0.05  # Defina o intervalo de confiança desejado
            ax.fill_between(dataframe['Month'], dataframe['Sessões executadas'] * (1 - conf_int), dataframe['Sessões executadas'] * (1 + conf_int),
                            color='gray', alpha=0.2, label=f'Intervalo de Confiança ({1-conf_int:.0%}-{1+conf_int:.0%})')

            # Adicione rótulos aos eixos
            ax.set_xlabel('Meses')
            ax.set_ylabel('Sessões executadas')

            # Adicione título ao gráfico
            ax.set_title(f'Gráfico de Linha - Meses X Crescimento em {i} posições')

            # Adicione legenda
            ax.legend()

            # Exiba o gráfico no Streamlit
            st.pyplot(fig)

    
main()


# In[ ]:


# !streamlit run app.py
