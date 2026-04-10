from flask_jwt_extended import get_jwt, verify_jwt_in_request, jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify
from modules.user.user import User
from functools import wraps

user_bp = Blueprint('user_bp', __name__, url_prefix='/user')
user_obj = User()

def check_role(cargo):
    def wrapper(fn):
        @wraps(fn)
        def checker(*args, **kwargs):
            verify_jwt_in_request()
            jwt = get_jwt()
            if jwt.get("cargo") != cargo:
                return jsonify({"Acesso negado"})
            return fn(*args, **kwargs)
        return checker
    return wrapper

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
@check_role("admin")
def lista_user():
    try:
        response = user_obj.get()
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 400

@user_bp.route('/getself/<int:url_id>', methods=['GET'])
@jwt_required()
def get_self(url_id):
    try:
        response = user_obj.get_self(url_id)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)})

@user_bp.route('/put/<int:url_id>', methods=['PUT'])
@jwt_required
def updt_user_route(url_id):
    user_id = get_jwt_identity()
    jwt = get_jwt()
    if jwt.get("cargo") != "admin" or str(user_id) != str(url_id):
        return jsonify({"Acesso negado"})
    else:
        dados = request.get_json()
        if not dados:
            return jsonify({"Erro": "JSON inválido ou ausente"}), 400
        try:
            user_obj.updt(url_id, dados)
            return jsonify({"status": "sucesso"}), 200
        except Exception as e:
            return jsonify({"status": "erro", "mensagem": str(e)}), 400

@user_bp.route('/delete/<int:url_id>', methods=['DELETE'])
@check_role("admin")
def del_user_route(url_id):
    try:
        user_obj.remove(url_id)
        return jsonify({"status": "sucesso"}), 200
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 400
