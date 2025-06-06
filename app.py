# Imports necessários
from flask import Flask
from dotenv import load_dotenv
import os
import psycopg
import requests
import json

app = Flask(__name__)

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações pra puxar as informações das variáveis de ambiente
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

# Tentando conectar no banco
def get_db_connection():
    try:
        return psycopg.connect(**DB_CONFIG)
    except psycopg.Error as e:
        print(f"Erro ao conectar ao banco: {e}")
        return None

# Função para formatar os dados do filme
def formatar_filme(filme):
    return {
        "id": filme[0],
        "title": filme[1],
        "year": filme[2],
        "rated": filme[3],
        "released": filme[4],
        "runtime": filme[5],
        "genre": filme[6],
        "director": filme[7],
        "writer": filme[8],
        "actors": filme[9],
        "plot": filme[10],
        "language": filme[11],
        "country": filme[12],
        "awards": filme[13],
        "poster": filme[14],
        "ratings": json.loads(filme[15]) if filme[15] else None,
        "metascore": filme[16],
        "imdb_rating": filme[17],
        "imdb_votes": filme[18],
        "imdb_id": filme[19],
        "type": filme[20],
        "dvd": filme[21],
        "box_office": filme[22],
        "production": filme[23],
        "website": filme[24],
        "response": filme[25]
    }

# Função para inserir filme no banco
def inserir_filme(cursor, data):
    cursor.execute("""
        INSERT INTO filmes (
            title, year, rated, released, runtime, genre,
            director, writer, actors, plot, language, country,
            awards, poster, ratings, metascore, imdb_rating,
            imdb_votes, imdb_id, type, dvd, box_office,
            production, website, response
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
    """, (
        data.get('Title'),
        data.get('Year'),
        data.get('Rated'),
        data.get('Released'),
        data.get('Runtime'),
        data.get('Genre'),
        data.get('Director'),
        data.get('Writer'),
        data.get('Actors'),
        data.get('Plot'),
        data.get('Language'),
        data.get('Country'),
        data.get('Awards'),
        data.get('Poster'),
        json.dumps(data.get('Ratings')),
        data.get('Metascore'),
        data.get('imdbRating'),
        data.get('imdbVotes'),
        data.get('imdbID'),
        data.get('Type'),
        data.get('DVD'),
        data.get('BoxOffice'),
        data.get('Production'),
        data.get('Website'),
        data.get('Response')
    ))

# Rota para consulta por id
@app.route("/consultarporid/<id>", methods=['GET'])
def consultar_id(id):
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                # Busca no banco de dados pelo IMDb ID
                cursor.execute("SELECT * FROM filmes WHERE imdb_id = %s", (id,))
                filme = cursor.fetchone()
                
                if filme:
                    return formatar_filme(filme)
                
                # Se não encontrou no banco, busca na API OMDb
                url = f"http://www.omdbapi.com/?i={id}&apikey={API_KEY}"
                response = requests.get(url)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('Response') == 'True':
                        inserir_filme(cursor, data)
                        conn.commit()
                        return data
                    else:
                        return {"error": "Filme não encontrado na API OMDB"}, 404
                else:
                    return {"error": "Erro ao acessar a API OMDB"}, response.status_code
                    
        except Exception as e:
            return {"error": f"Erro ao processar a requisição: {str(e)}"}, 500
        finally:
            conn.close()
    else:
        return {"error": "Erro ao conectar com o banco de dados"}, 500

# Rota para consulta por nome
@app.route("/consultarpornome/<nome>", methods=['GET'])
def consultar_nome(nome):
    # Formatação do nome para a busca na API
    nome_busca = nome.replace("%20", " ")
    nome_formatado = nome_busca.strip()
    
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                # Busca no banco de dados pelo título
                cursor.execute("SELECT * FROM filmes WHERE LOWER(title) = LOWER(%s)", (nome_formatado,))
                filme = cursor.fetchone()
                
                if filme:
                    return formatar_filme(filme)
                
                # Se não encontrou no banco, busca na API OMDb
                nome_api = nome_formatado.replace(" ", "+")
                url = f"http://www.omdbapi.com/?t={nome_api}&apikey={API_KEY}"
                response = requests.get(url)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('Response') == 'True':
                        # Verifica se o filme já existe pelo IMDb ID antes de inserir
                        cursor.execute("SELECT * FROM filmes WHERE imdb_id = %s", (data.get('imdbID'),))
                        filme_existente = cursor.fetchone()
                        
                        if filme_existente:
                            return formatar_filme(filme_existente)
                            
                        # Se não existe, insere no banco
                        inserir_filme(cursor, data)
                        conn.commit()
                        return data
                    else:
                        return {"error": "Filme não encontrado na API OMDB"}, 404
                else:
                    return {"error": "Erro ao acessar a API OMDB"}, response.status_code
                    
        except Exception as e:
            return {"error": f"Erro ao processar a requisição: {str(e)}"}, 500
        finally:
            conn.close()
    else:
        return {"error": "Erro ao conectar com o banco de dados"}, 500

if __name__ == '__main__':
    conn = get_db_connection()
    if conn:
        print("Conexão com o banco de dados foi bem-sucedida!")
        conn.close()  
    else:
        print("Não foi possível conectar ao banco de dados.")
    app.run()