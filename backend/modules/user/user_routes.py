from flask import Blueprint, request, jsonify
from modules.user.user import User

user_bp = Blueprint('user_bp', __name__, url_prefix='/user')
user_obj = User()

@user_bp.route('/post', methods=['POST'])
def cria_user():
    dados = request.get_json()
    if not dados:
        return jsonify({"Erro": "JSON inválido ou ausente"}), 400
    try:
        user_obj.post(dados)
        return jsonify({"status": "sucesso"}), 201
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 400

@user_bp.route('/get', methods=['GET'])
def lista_user():
    try:
        response = user_obj.get()
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 400

@user_bp.route('/put/<int:id>', methods=['PUT'])
def updt_user_route(id):
    dados = request.get_json()
    if not dados:
        return jsonify({"Erro": "JSON inválido ou ausente"}), 400
    try:
        user_obj.updt(id, dados)
        return jsonify({"status": "sucesso"}), 200
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 400

@user_bp.route('/delete/<int:id>', methods=['DELETE'])
def del_user_route(id):
    try:
        user_obj.remove(id)
        return jsonify({"status": "sucesso"}), 200
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 400
