from flask import Blueprint, request, jsonify
from modules.curriculo.curr import Curriculo

curriculo_bp = Blueprint('curriculo_bp', __name__, url_prefix='/curriculo')
curriculo_obj = Curriculo()

@curriculo_bp.route('/post', methods=['POST'])
def cria_curr():
    dados = request.get_json()
    if not dados:
        return jsonify({"Erro": "JSON inválido ou ausente"}), 400
    try:
        curriculo_obj.post(dados)
        return jsonify({"status": "sucesso"}), 201
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 400

@curriculo_bp.route('/get', methods=['GET'])
def lista_curr():
    try:
        response = curriculo_obj.get()
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 400

@curriculo_bp.route('/put/<int:id>', methods=['PUT'])
def updt_curr_route(id):
    dados = request.get_json()
    if not dados:
        return jsonify({"Erro": "JSON inválido ou ausente"}), 400
    try:
        curriculo_obj.updt(id, dados)
        return jsonify({"status": "sucesso"}), 200
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 400

@curriculo_bp.route('/delete/<int:id>', methods=['DELETE'])
def del_curr_route(id):
    try:
        curriculo_obj.remove(id)
        return jsonify({"status": "sucesso"}), 200
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 400
