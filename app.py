from flask import Flask, request
import psycopg

app = Flask(__name__)

if __name__ == '__main__':
    app.run()
    
try:
    with psycopg.connect("host=164.90.152.205 dbname=eldorado user=postgres password=3f@db port=80") as conectDb:
        print("Conexão com o banco de dados realizada com sucesso.")
except psycopg.Error as e:
    print("Erro ao conectar ao banco de dados:", e)

@app.route("/consultar/<id>", methods=['GET'])
def consultar_id(id):
    return

@app.route("/consultar/<nome>", methods=['GET'])
def consultar_id(nome):
    return
   
# Notas
# rota para consulta por id
# rota para consulta por nome
# a consulta é realizada no banco próprio
# se não tiver no banco, busca na api
# após a busca, adiciona as informações no banco