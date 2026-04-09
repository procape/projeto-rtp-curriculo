from flask import Flask, request, jsonify
from modules.curriculo.curr import *
from modules.user.user import *

app = Flask(__name__)

user_Vazio = User() #Variável para manusear os dados

#POST em user
@app.route('/user/post', methods=['POST'])
def cria_user():
    dados = request.get_json()
    if not dados:
        return jsonify({"Erro": "JSON inválido ou ausente"})
    response = user_Vazio.post(dados)
    return jsonify(response), 201

#GET em user
@app.route('/user/get', methods=['GET'])
def lista_user():
    response = user_Vazio.get()
    return jsonify(response), 200

@app.route('user/put/<int:id>', methods=['PUT'])
def updt_curr(id):
    try:
        dados = request.get_json()
        if not dados:
            return jsonify({"Erro": "JSON inválido ou ausente"})
        response = user_Vazio.updt(id, dados)
    except:
        return jsonify({"status": "erro", "mensagem": str(Exception)}), 400
    return jsonify(response),200

@app.route('user/delete/<int:id>', methods=['DELETE'])
def del_curr(id):
    try:
        response = user_Vazio.remove(id)
    except:
        return jsonify({"status": "erro", "mensagem": str(Exception)}), 400
    return jsonify(response),200

curriculo_Vazio = Curriculo()

#POST em curriculo
@app.route('/curriculo/post', methods=['POST'])
def cria_curr():
    dados = request.get_json()
    if not dados:
        return jsonify({"Erro": "JSON inválido ou ausente"})
    response = curriculo_Vazio.post(dados)
    return jsonify(response), 201

#GET em curriculos
@app.route('/curriculo/get', methods=['GET'])
def lista_curr():
    response = curriculo_Vazio.get()
    return jsonify(response), 200

@app.route('curriculo/put/<int:id>', methods=['PUT'])
def updt_curr(id):
    try:
        dados = request.get_json()
        if not dados:
            return jsonify({"Erro": "JSON inválido ou ausente"})
        response = curriculo_Vazio.updt(id, dados)
    except:
        return jsonify({"status": "erro", "mensagem": str(Exception)}), 400
    return jsonify(response),200

@app.route('curriculo/delete/<int:id>', methods=['DELETE'])
def del_curr(id):
    try:
        response = curriculo_Vazio.remove(id)
    except:
        return jsonify({"status": "erro", "mensagem": str(Exception)}), 400
    return jsonify(response),200
