import mysql.connector
import csv
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

try:
    # Conexão com o banco de dados MySQL usando variáveis de ambiente
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    cursor = conn.cursor()

    # Criação da tabela 'temperatura' (se não existir)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS temperatura (
            id INT AUTO_INCREMENT PRIMARY KEY,
            timestamp DATETIME,
            temperature FLOAT
        )
    """)

    # Limpeza dos dados anteriores (opcional)
    cursor.execute("DELETE FROM temperatura")

    # Leitura e inserção de dados do arquivo CSV
    with open("feeds.csv", "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # Pular o cabeçalho
        for row in reader:
            # Ajuste dos índices conforme a estrutura do CSV
            timestamp = row[0]  # Primeiro índice para o timestamp
            temperature = row[4]  # Quinto índice para temperatura

            # Inserção dos dados na tabela
            cursor.execute(
                "INSERT INTO temperatura (timestamp, temperature) VALUES (%s, %s)",
                (timestamp, temperature)
            )

    # Confirmação das alterações e fechamento da conexão
    conn.commit()
    print("Banco de dados MySQL criado e populado com sucesso!")

except mysql.connector.Error as err:
    print(f"Erro ao conectar ou executar operação MySQL: {err}")
finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
        print("Conexão MySQL fechada.")
