#Biblioteca Geral
import streamlit as st
#Biblioteca para Manipulação de Dados
import pandas as pd
#Biblioteca Geração de Graficos 
import numpy as np

# Titulo Relatorio
st.title('Uber coleta em Nova York')

# Dados que a documentação indica
DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

# Função
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Icones de carregamento dos Dados
# Crie um elemento de texto e informe ao leitor que os dados estão sendo carregados.
data_load_state = st.text('Carregando dados...')
# Carregue 10.000 linhas de dados no dataframe.
data = load_data(10000)
# Notifique o leitor que os dados foram carregados com sucesso.
data_load_state.text('Carregando dados...Pronto!')

# Cache sem esforço
@st.cache_data
def load_data(nrows):
    data_load_state.text("Pronto! (using st.cache_data)")# Substituir a linha data_load_state.text('Loading data...done!')

# Ver dados em Tabelão
st.subheader('Dados Bruto') # Subtitulo
st.write(data) # Mostra os dados em tabela

# GRAFICOS
st.subheader('Número de coletas por hora')

# Use o NumPy(np) para gerar um HISTOGRAMA que divide os horários de coleta classificados por hora
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
# Mostrar
st.bar_chart(hist_values)

# Grafico MAPA
st.subheader('Mapa de todos os pontos de coleta')
st.map(data)

# Mapa com Filtro fixo
hour_to_filter = 17
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'1 - Mapa concentração de coletas às {hour_to_filter}:00')
st.map(filtered_data)

# Filtrar resultados com um controle deslizante
hour_to_filter_f = st.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h
filtered_data_f = data[data[DATE_COLUMN].dt.hour == hour_to_filter_f]
st.subheader(f'2 - Mapa concentração de coletas às {hour_to_filter_f}:00')
st.map(filtered_data_f)

# Ver dados em Tabelão com checkbox
if st.checkbox('Mostrar dados Brutos?'):
    st.subheader('Tabela')
    st.write(data)