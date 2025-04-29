from flask import Flask, request
from dotenv import load_dotenv
import os
import psycopg
import requests
import json

app = Flask(__name__)

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações
API_KEY = os.getenv('OMDB_API_KEY')
if not API_KEY:
    print("Erro: Coloque a chave da API do OMDb no arquivo .env")
    exit()

DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'port': os.getenv('DB_PORT')
}

def get_db_connection():
    try:
        return psycopg.connect(**DB_CONFIG)
    except psycopg.Error as e:
        print(f"Erro ao conectar ao banco: {e}")
        return None

@app.route("/consultar/<id>", methods=['GET'])
def consultar_id(id):
    return

@app.route("/consultar", methods=['GET'])
def consultar_nome():
    return

if __name__ == '__main__':
    conn = get_db_connection()
    if conn:
        print("Conexão com o banco de dados foi bem-sucedida!")
        conn.close()  
    else:
        print("Não foi possível conectar ao banco de dados.")
    app.run(debug=True)