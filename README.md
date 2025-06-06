# atividade-pi-dw3

## Implementação de um serviço de cache para informações de filmes e séries

Desenvolver uma API REST que disponibilize informações sobre filmes e séries, simulando o funcionamento de um sistema de cache. A fonte principal de dados será o serviço público disponibilizado em https://www.omdbapi.com/. <br>
A API desenvolvida deverá permitir buscas de filmes e séries tanto pelo nome quanto pelo ID. No momento de uma solicitação, o sistema deve seguir a seguinte lógica: <br>
Primeiramente, realizar a consulta em um banco de dados local próprio. <br>
Caso a informação não esteja disponível no banco de dados, a API deverá buscar os dados no site OMDb. <br>
Após buscar a informação no OMDb, os dados recuperados deverão ser armazenados no banco de dados para futuras consultas. <br>
<br>
Requisitos: <br>
Implementar endpoints para consulta por nome e por ID.<br>
Utilizar banco de dados PostgreSQL para armazenar as informações recuperadas.<br>
Documentar brevemente a API no arquivo README.md<br>
Postar o código em um repositório público do Github e enviar o link do repositório no classroom<br>

## Resumo 

A API tem dois endpoint principais para fazer a consulta de informações obre filmes e séries usa o banco de dados PostgreSQl e a API pública OMDb. Quando tentamos buscar com um ID, usamos o método GET e o código verifica se as informações que respectivas ao ID existem no banco de dados do grupo, se estiver os dados são retornados. Se não estiver uma requisição é feita ao OMDb para obter as informações, a partir do momento que os dados são encontrados eles são armazenados no banco de dados do grupo e depois retornado para o usuário.

O endpoint que consulta pelo nome segue uma lógica parecida com o anterior, primeiro é verificado se o filme buscado está armazenado no banco de dados do grupo, se estiver os dados desejados são retornados. Agora se não existir o filme procurado no banco de dados do grupo uma requisição é enviada ao OMDb para obter as informações. Depois de conseguir os dados, armazenamos eles no nosso banco de dados e retornamos as informações para quem fez a consulta.

## Para rodar:

Para rodar a API é necessário rodar os comandos:
```bash
python -m venv .venv
```
```bash
.venv\Scripts\Activate
```
```python
pip install flask psycopg[binary] dotenv requests
```
Também é necessário criar um arquivo **.env** no diretório do projeto e adicionar as informações necessárias para as requisições e para a conexão com o banco.

### Para utilizar:

Para utilizar a API rode o comando:
```python
python app.py
```

Copie o link do servidor de testes que o flask gerar, envie uma requisição http para o endpoint **/consultarpornome/** nome do filme ou para o endpoint **/consultarporid/** id do filme