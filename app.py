import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# Função para carregar e processar dados
def load_and_process_data(csv_path):
    df = pd.read_csv(csv_path, delimiter=';')

    # Tratamento dos dados
    df['First Received'] = pd.to_datetime(df['First Received'], errors='coerce', format='%d/%m/%Y')
    df['Last Received'] = pd.to_datetime(df['Last Received'], errors='coerce', format='%d/%m/%Y')
    df['date_update'] = pd.to_datetime(df['date_update'], errors='coerce', format='%d/%m/%Y')
    df['FRxLR(dias)'] = pd.to_numeric(df['FRxLR(dias)'], errors='coerce')
    df['Qtd_Received'] = pd.to_numeric(df['Qtd_Received'], errors='coerce')
    df['valor'] = pd.to_numeric(df['valor'], errors='coerce')

    # Adicionar colunas de ano, mês e semana
    df['Ano'] = df['First Received'].dt.year
    df['Mês'] = df['First Received'].dt.strftime('%B')  # Nome do mês em inglês
    df['Semana'] = df['First Received'].dt.isocalendar().week  # Semana do ano

    # Mapear os nomes dos meses para português
    month_translation = {
        'January': 'Janeiro', 'February': 'Fevereiro', 'March': 'Março', 'April': 'Abril',
        'May': 'Maio', 'June': 'Junho', 'July': 'Julho', 'August': 'Agosto',
        'September': 'Setembro', 'October': 'Outubro', 'November': 'Novembro', 'December': 'Dezembro'
    }
    df['Mês'] = df['Mês'].map(month_translation)

    return df

# Caminho para o seu arquivo CSV
csv_path = 'csv.csv'  # Substitua pelo caminho correto do seu arquivo

# Carregar e processar os dados
df = load_and_process_data(csv_path)

# Configurar o Streamlit
st.title("Lost & Damaged")
# Criar gráfico de perda de pacotes por mês e semana
st.text("Este relatório fornece uma análise detalhada das perdas e danos dos pacotes")

# Adicionar espaço entre os KPIs e o texto
st.markdown("<br><br>", unsafe_allow_html=True)  # Adiciona dois quebras de linha

# Adicionar uma sidebar para o filtro de station_name
station_names = ['Selecionar tudo'] + df['station_name'].unique().tolist()
selected_station = st.sidebar.selectbox('Selecione a estação', options=station_names)

# Adicionar filtro de período
start_date = st.sidebar.date_input("Data de Início", df['First Received'].min())
end_date = st.sidebar.date_input("Data de Fim", df['First Received'].max())

# Filtrar os dados com base na seleção da estação e no período
if selected_station == 'Selecionar tudo':
    df_filtered = df
else:
    df_filtered = df[df['station_name'] == selected_station]

df_filtered = df_filtered[
    (df_filtered['First Received'] >= pd.to_datetime(start_date)) &
    (df_filtered['First Received'] <= pd.to_datetime(end_date))
]

# Filtrar os dados com status 'Lost' e 'Damaged'
df_filtered = df_filtered[df_filtered['Status_OM'].isin(['LOST', 'Damaged'])]

# Calcular KPIs com base nos dados filtrados
total_consignment_count = df_filtered['consignment_no'].nunique()
lost_count = df_filtered[df_filtered['Status_OM'] == 'LOST']['consignment_no'].nunique()
damaged_count = df_filtered[df_filtered['Status_OM'] == 'Damaged']['consignment_no'].nunique()

# Adicionar cartões de KPIs no topo
# Criar colunas para o layout dos KPIs
col1, col2, col3 = st.columns(3)

# Adicionar cartões de KPIs nas colunas
with col1:
    st.metric(
        label="Total de perdas",
        value=total_consignment_count
    )

with col2:
    st.metric(
        label="Total de Lost",
        value=lost_count
    )

with col3:
    st.metric(
        label="Total de Damage",
        value=damaged_count
    )

# Adicionar espaço entre os KPIs e o texto
st.markdown("<br><br>", unsafe_allow_html=True)  # Adiciona dois quebras de linha

# Contar a quantidade de pacotes por mês e semana
perda_por_mes_semana = df_filtered.groupby(['Mês', 'Semana', 'Status_OM'])['consignment_no'].count().reset_index()
perda_por_mes_semana.columns = ['Mês', 'Semana', 'Status', 'Quantidade de Consignments']

# Definindo a paleta de cores laranja com o status 'LOST' em cor mais fraca
orange_palette = {
    'LOST': '#FF9A8B',  # Cor mais fraca para LOST
    'Damaged': '#EE4D2D'  # Cor mais forte para Damaged
}

# Criando a coluna de semana do mês para exibir no gráfico
perda_por_mes_semana['Semana_Mês'] = perda_por_mes_semana.apply(
    lambda x: f"{x['Semana']} ({x['Mês']})", axis=1
)

fig = go.Figure()

for status in perda_por_mes_semana['Status'].unique():
    df_status = perda_por_mes_semana[perda_por_mes_semana['Status'] == status]
    fig.add_trace(go.Bar(
        x=df_status['Semana_Mês'],
        y=df_status['Quantidade de Consignments'],
        name=status,
        marker_color=orange_palette[status],
        hoverinfo='x+y+name',
        customdata=df_status[['Semana', 'Mês', 'Status', 'Quantidade de Consignments']].values,
        hovertemplate="<b>%{x}</b><br>Quantidade de Consignments: %{y}<br>Status: %{customdata[2]}<extra></extra>"
    ))

# Adicionando os rótulos de texto nas barras para melhor visualização
fig.update_traces(texttemplate='%{y}', textposition='inside', textfont=dict(size=12, color='white'))

# Ajustar layout
fig.update_layout(
    xaxis_title='Semana do Mês',
    yaxis_title='Quantidade de Consignments',
    barmode='group',
    legend_title='Status',
    xaxis=dict(tickangle=45),
    yaxis=dict(range=[0, perda_por_mes_semana['Quantidade de Consignments'].max() + 10]),
    width=1000,  # Ajustar a largura do gráfico
    height=600   # Ajustar a altura do gráfico
)

# Centralizar os rótulos dos eixos
fig.update_xaxes(tickangle=45)
fig.update_yaxes(title_standoff=20)
fig.update_layout(
    title={
        'text': "Perda de Pacotes por Mês e Semana",
        'x': 0.5,  # Centralizar o título
        'xanchor': 'center'
    }
)

# Adiciona o gráfico ao Streamlit
st.plotly_chart(fig, use_container_width=True)

# Exibir a tabela de e-mails e quantidade de bips
st.subheader("E-mails e Quantidade de Bips")
email_bips = df_filtered.groupby('last_user')['consignment_no'].count().reset_index()
email_bips.columns = ['Email', 'Quantidade de Bips']
email_bips_sorted = email_bips.sort_values(by='Quantidade de Bips', ascending=False)
st.dataframe(email_bips_sorted.reset_index(drop=True), use_container_width=True)

# Mostrar detalhes com base na seleção do gráfico
st.subheader("Detalhes dos Pacotes Selecionados")
details_df = pd.DataFrame()

# Função para atualizar os detalhes com base na seleção do gráfico
def update_details(selected_index):
    global details_df
    details_df = df_filtered[
        (df_filtered['Semana'].astype(str) + ' (' + df_filtered['Mês'] + ')') == selected_index
    ]
    details_df = details_df[details_df['Status_OM'].isin(['LOST', 'Damaged'])]
    st.dataframe(details_df.reset_index(drop=True))  # Remover o índice da tabela

# Usar um seletor para simular a seleção de uma barra
selected_index = st.selectbox(
    "Selecione a Semana e Mês para ver os detalhes",
    options=perda_por_mes_semana['Semana_Mês'].unique()
)

update_details(selected_index)
