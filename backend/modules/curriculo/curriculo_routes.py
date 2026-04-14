from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity, verify_jwt_in_request
from functools import wraps
from modules.curriculo.curr import Curriculo

curriculo_bp = Blueprint('curriculo_bp', __name__, url_prefix='/curriculo')
curriculo_obj = Curriculo()


def check_role_curr(cargo):
    def wrapper(f):
        @wraps(f)
        def checker_role_curr(*args, **kwargs):
            verify_jwt_in_request()
            jwt = get_jwt()
            if jwt.get("role") != cargo:
                return jsonify({"status": "Acesso negado"}), 403
            return f(*args, **kwargs)
        return checker_role_curr
    return wrapper


def user_or_admin_curr():
    def wrapper(f):
        @wraps(f)
        def checker_curr(*args, **kwargs):
            verify_jwt_in_request()
            id_url = kwargs.get("url_id")
            jwt = get_jwt()
            user_id = get_jwt_identity()
            if jwt.get("role") != "admin" and str(user_id) != str(id_url):
                return jsonify({"status": "Acesso negado"}), 403
            return f(*args, **kwargs)
        return checker_curr
    return wrapper


@curriculo_bp.route('', methods=['POST'])
@jwt_required()
def cria_curr():
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "JSON inválido ou ausente"}), 400
    try:
        curriculo_obj.post(dados)
        return jsonify({"status": "sucesso"}), 201
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 400


@curriculo_bp.route('', methods=['GET'])
@check_role_curr("admin")
def lista_curr():
    try:
        response = curriculo_obj.get()
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 400


@curriculo_bp.route('/<int:url_id>', methods=['GET'])
@user_or_admin_curr()
def lista_self_curr(url_id):
    try:
        response = curriculo_obj.get_self(url_id)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 400


@curriculo_bp.route('/<int:url_id>', methods=['PUT'])
@user_or_admin_curr()
def updt_curr_route(url_id):
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "JSON inválido ou ausente"}), 400
    try:
        curriculo_obj.updt(url_id, dados)
        return jsonify({"status": "sucesso"}), 200
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 400


@curriculo_bp.route('/<int:url_id>', methods=['DELETE'])
@check_role_curr("admin")
def del_curr_route(url_id):
    try:
        curriculo_obj.remove(url_id)
        return jsonify({"status": "sucesso"}), 200
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 400
