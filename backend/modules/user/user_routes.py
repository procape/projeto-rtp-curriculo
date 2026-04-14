from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity, verify_jwt_in_request
from functools import wraps
from modules.user.user import User

user_bp = Blueprint('user_bp', __name__, url_prefix='/user')
user_obj = User()


def check_role_user(cargo):
    def wrapper(f):
        @wraps(f)
        def checker_role_user(*args, **kwargs):
            verify_jwt_in_request()
            jwt = get_jwt()
            if jwt.get("role") != cargo:
                return jsonify({"status": "Acesso negado"}), 403
            return f(*args, **kwargs)
        return checker_role_user
    return wrapper


def user_or_admin_user():
    def wrapper(f):
        @wraps(f)
        def checker_user(*args, **kwargs):
            verify_jwt_in_request()
            id_url = kwargs.get("url_id")
            jwt = get_jwt()
            user_id = get_jwt_identity()
            if jwt.get("role") != "admin" and str(user_id) != str(id_url):
                return jsonify({"status": "Acesso negado"}), 403
            return f(*args, **kwargs)
        return checker_user
    return wrapper


@user_bp.route('', methods=['POST'])
def cria_user():
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "JSON inválido ou ausente"}), 400
    for campo in ["cpf", "nome", "email", "senha"]:
        if not dados.get(campo):
            return jsonify({"erro": f"Campo '{campo}' é obrigatório"}), 400
    dados["cargo"] = "usuario"
    if user_obj.get_by_email(dados["email"]):
        return jsonify({"erro": "E-mail já cadastrado"}), 409
    try:
        user_obj.post(dados)
        return jsonify({"status": "sucesso"}), 201
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 400


@user_bp.route('/<int:url_id>', methods=['GET'])
@jwt_required()
def get_self(url_id):
    try:
        response = user_obj.get_self(url_id)
        if not response:
            return jsonify({"status": "erro", "mensagem": "Usuário não encontrado"}), 404
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 400


@user_bp.route('/<int:url_id>', methods=['PUT'])
@user_or_admin_user()
def updt_user_route(url_id):
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "JSON inválido ou ausente"}), 400
    try:
        user_obj.updt(url_id, dados)
        return jsonify({"status": "sucesso"}), 200
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 400


@user_bp.route('/<int:url_id>', methods=['DELETE'])
@check_role_user("admin")
def del_user_route(url_id):
    try:
        user_obj.remove(url_id)
        return jsonify({"status": "sucesso"}), 200
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 400