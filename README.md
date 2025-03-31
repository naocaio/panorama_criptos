# Panorama Criptomoedas

Este projeto contém um script Python que coleta dados de criptomoedas da API CoinCap e os armazena em um banco de dados PostgreSQL, que está armazenado no render.com, podendo ser acessado remotamente. Também inclui um dashboard no PowerBI para visualização de uma panorama básico das criptomoedas.

## Funcionalidades

- **Coleta de dados**
  - Nome
  - Símbolo
  - Preço em USD
  - Market Cap em USD
  - Volume de 24h em USD
 
- **Armazenamento**
  - Banco de dados PostgreSQL hospedado gratuitamente no Render.
    
- **Histórico de preços**
  - Histórico de preço para todas as criptomoedas.
    
- **Dashboard interativo no Power BI**
  - Total Market Cap
  - Volume Movimentado, últimas 24h
  - Maior Preço, últimas 24h
  - Preço Médio por Criptomoeda
  - Participação das Criptomoedas no Volume Negociado
  - Cotação Atual das Criptomoedas
  - Variação de Preço, últimas 24h
  - Filtro por Criptomoeda
    
- **Segurança das credenciais**
  - Credenciais para autenticação no banco de dados via variável de ambiente. 

## Estrutura do Banco de Dados

O banco de dados contém as seguintes tabelas:

1. **cryptos**:
   - `id`: ID único da criptomoeda (chave primária).
   - `name`: Nome da criptomoeda.
   - `symbol`: Símbolo da criptomoeda.
   - `price_usd`: Preço da criptomoeda em USD.
   - `market_cap_usd`: Capitalização de mercado da criptomoeda em USD.
   - `volume_24h_usd`: Volume de negociação das últimas 24h em USD.

2. **history**:
   - `id`: ID único do histórico (chave primária).
   - `crypto_id`: Relacionamento com a tabela `cryptos` (chave estrangeira).
   - `price_usd`: Preço da criptomoeda no momento da coleta.
   - `timestamp`: Data e hora da coleta (timestamp).

## Como Usar

1. **Configuração do Banco de Dados**:
   - Utilizar instruções sobre a variável de ambiente enviadas por e-mail.
   - Pode ser necessário autenticar ao PostgreSQL ao acessar o dashboard pela primeira vez. Favor checar e-mail.

2. **Executar o Script**:
   - Clone este repositório para sua máquina local.
   - Instale as dependências necessárias com o seguinte comando:
     ```bash
     pip install -r requirements.txt
     ```
   - Execute o script Python para coletar e armazenar os dados:
     ```bash
     python script_panorama_criptos.py
     ```

3. **Atualizar Dados no Power BI**:
   - Após rodar o script e armazenar os dados no banco de dados, abra o Power BI.
   - Atualize o conjunto de dados do Power BI para refletir os dados mais recentes.

## Requisitos

- **Python 3.11.11**.
- **Bibliotecas**:
  - `os` para interação com o sistema operacional.
  - `psycopg2` para interação com o PostgreSQL.
  - `requests` para chamadas à API CoinCap.

