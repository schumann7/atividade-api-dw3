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

@app.route("/consultar/<nome>", methods=['GET'])
def consultar_nome(nome):
    nome = nome.lower()
    nome = nome.replace(" ", "+")
    if nome == "":
        cursor = get_db_connection.cursor()
        cursor.execute("select * from filmes where titulo = %s", (nome,))
        lista = []
        for item in cursor:
            lista.append({
                "id": item[0],
                "title": item[1],
                "year": item[2],
                "rated": item[3],
                "released": item[4],
                "runtime": item[5],
                "genre": item[6],
                "director": item[7],
                "writer": item[8],
                "actors": item[9],
                "plot": item[10],
                "language": item[11],
                "country": item[12],
                "awards": item[13],
                "poster": item[14],
                "ratings": item[15],
                "metascore": item[16],
                "imdb_rating": item[17],
                "imdb_votes": item[18],
                "imdb_id": item[19],
                "type": item[20],
                "dvd": item[21],
                "box_office": item[22],
                "production": item[23],
                "website": item[24],
                "response": item[25]
            })  
            return lista
        else:
            url = f"http://www.omdbapi.com/?t={nome}&apikey={API_KEY}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data['Response'] == 'True':
                    cursor = get_db_connection.cursor()
                    cursor.execute("insert into filmes (title, year, rated, released, runtime, genre, director, writer, actors, plot, language, country, awards, poster, ratings, metascore, imdb_rating, imdb_votes, imdb_id, type, dvd, box_office, production, website, response) values (%")
        

if __name__ == '__main__':
    conn = get_db_connection()
    if conn:
        print("Conexão com o banco de dados foi bem-sucedida!")
        conn.close()  
    else:
        print("Não foi possível conectar ao banco de dados.")
    app.run(debug=True)