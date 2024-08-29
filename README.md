# 📊 Lost & Damaged Analysis Dashboard

Este projeto é um dashboard interativo para análise de pacotes perdidos e danificados, desenvolvido em Streamlit. Ele permite visualizar dados de pacotes com filtros por estação, período, e status dos pacotes, fornecendo insights detalhados através de gráficos e KPIs.

## 📝 Funcionalidades

- Visualização de pacotes perdidos e danificados por mês e semana.
- Filtros de estação e período para personalização dos dados exibidos.
- Cartões de KPIs mostrando as principais métricas do desempenho.
- Gráfico interativo para análise de perda e dano com destaque por semana e status.
- Detalhamento dos pacotes selecionados com dados específicos.

## 🚀 Tecnologias Utilizadas

- **Python**: Linguagem principal para o desenvolvimento.
- **Streamlit**: Para criação do dashboard interativo.
- **Pandas**: Manipulação e tratamento de dados.
- **Plotly**: Visualização gráfica avançada.
- **Docker**: Para containerização da aplicação.

## 📦 Instalação e Configuração com Docker

### Pré-requisitos

- Docker instalado na máquina.

### Passo a Passo

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/seu-usuario/lost-damaged-analysis.git
   cd lost-damaged-analysis

2. **Crie a imagem Docker:**

- Execute o comando abaixo para construir a imagem Docker do projeto:
    ```bash
    docker build -t lost-damaged-analysis .

3. **Execute o container:**
- Após construir a imagem, execute o container:
    ```bash
    docker run -p 8501:8501 lost-damaged-analysis

4. **Acesse o dashboard:**
- Abra o navegador e acesse o endereço: http://localhost:8501


