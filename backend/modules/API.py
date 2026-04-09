from flask import Flask, request, jsonify
from curriculo.curr import *
from user.user import *

app = Flask(__name__)

user_Vazio = User() #Variável para manusear os dados

#POST em user
@app.route('/user', methods=['POST'])
def cria_user():
    dados = request.get_json()
    if not dados:
        return jsonify({"Erro": "JSON inválido ou ausente"})
    response = user_Vazio.post(dados)
    return jsonify(response), 201

#GET em user
@app.route('/user', method=['GET'])
def lista_user():
    response = user_Vazio.get()
    return jsonify(response), 200

curriculo_Vazio = Curriculo()

#POST em curriculo
@app.route('/curriculo', method=['POST'])
def cria_curr():
    dados = request.get_json()
    if not dados:
        return jsonify({"Erro": "JSON inválido ou ausente"})
    response = curriculo_Vazio.post(dados)
    return jsonify(response), 201

#GET em curriculos
@app.route('/curriculo', method=['GET'])
def lista_curr():
    response = curriculo_Vazio.get()
    return jsonify(response), 200
