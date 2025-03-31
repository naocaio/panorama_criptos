import os
import psycopg2
import requests

# Pegar os dados de configuraçao de acesso o Postgre no Render da variável de ambiente.
DB_URL = os.getenv("DB_URL")

if DB_URL is None:
    print("Erro com a variável de ambiente. Favor verificar.")
    exit()

def create_tables():
    conn = psycopg2.connect(DB_URL)
    cursor = conn.cursor()


    # Tabela com as infos das criptos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cryptos (
            id SERIAL PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            symbol TEXT UNIQUE NOT NULL,
            price_usd REAL NOT NULL,
            market_cap_usd REAL,
            volume_24h_usd REAL
        )
    ''')

    # Tabela do histórico, amarrada pelo id das criptos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id SERIAL PRIMARY KEY,
            crypto_id INTEGER REFERENCES cryptos(id),
            price_usd REAL NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    cursor.close()
    conn.close()
    print("Tabelas criadas ou já existentes no PostgreSQL.")

def fetch_crypto_data():
    url = "https://api.coincap.io/v2/assets"
    response = requests.get(url)
    return response.json()["data"] if response.status_code == 200 else []

def save_data_to_postgres(data):
    conn = psycopg2.connect(DB_URL)
    cursor = conn.cursor()

    for item in data:
        # Insert/update na tabela de criptos
        cursor.execute('''
            INSERT INTO cryptos (name, symbol, price_usd, market_cap_usd, volume_24h_usd)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (symbol) DO UPDATE
            SET price_usd = EXCLUDED.price_usd,
                market_cap_usd = EXCLUDED.market_cap_usd,
                volume_24h_usd = EXCLUDED.volume_24h_usd
        ''', (item["name"], item["symbol"], float(item["priceUsd"]),
              float(item["marketCapUsd"]), float(item["volumeUsd24Hr"])))

        # Insert na tabela de histórico
        cursor.execute('''
            INSERT INTO history (crypto_id, price_usd, timestamp)
            SELECT id, %s, CURRENT_TIMESTAMP FROM cryptos WHERE symbol = %s
        ''', (float(item["priceUsd"]), item["symbol"]))

    conn.commit()
    cursor.close()
    conn.close()
    print("Os dados foram atualizados com sucesso PostgreSQL! \n\nPor favor, atualize os dados no arquivo PBI.")

# Execução final do script.
## Primeiro ele cria as tabelas, caso elas não existam no banco.
## Na sequência ele pega os dados na api e armanezam na variável cryto_data.
## Por último ele faz os inserts/update no Postgres no Render.
create_tables()
crypto_data = fetch_crypto_data()
save_data_to_postgres(crypto_data)
