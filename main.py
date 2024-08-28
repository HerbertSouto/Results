import pandas as pd

# Carregar o CSV com o delimitador correto
csv = 'csv.csv'  # Substitua pelo caminho correto do seu arquivo
df = pd.read_csv(csv, delimiter=';')

# Tratamento dos dados
df['First Received'] = pd.to_datetime(df['First Received'], errors='coerce', format='%d/%m/%Y')
df['Last Received'] = pd.to_datetime(df['Last Received'], errors='coerce', format='%d/%m/%Y')
df['date_update'] = pd.to_datetime(df['date_update'], errors='coerce', format='%d/%m/%Y')
df['FRxLR(dias)'] = pd.to_numeric(df['FRxLR(dias)'], errors='coerce')
df['Qtd_Received'] = pd.to_numeric(df['Qtd_Received'], errors='coerce')
df['valor'] = pd.to_numeric(df['valor'], errors='coerce')

# Filtrar os dados com status 'Lost' e 'Damaged'
df_filtered = df[df['Status_OM'].isin(['Lost', 'Damaged'])]

# Contar a quantidade de pacotes bipados por e-mail
email_bips = df_filtered.groupby('last_user')['consignment_no'].count().reset_index()
email_bips.columns = ['Email', 'Quantidade de Bips']

# Ordenar a lista em ordem decrescente de quantidade de bips
email_bips_sorted = email_bips.sort_values(by='Quantidade de Bips', ascending=False)

# Exibir a lista ordenada
print(email_bips_sorted)
