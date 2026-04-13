from flask_jwt_extended import jwt_required
from flask import Blueprint, request, jsonify
from datetime import timedelta, datetime
from modules.user.user import User
from modules.forgot.send_token import *
from config. settings import *
from functools import wraps
user_bp = Blueprint('user_bp', __name__, url_prefix='/user')
user_obj = User()

tokenSaved= {}

def check_role_user(cargo):
    def wrapper(f):
        @wraps(f)
        def checker_role_user(*args, **kwargs):
            verify_jwt_in_request()
            jwt = get_jwt()
            if jwt.get("cargo") != cargo:
                return jsonify({"Acesso negado"})
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
            if jwt.get("cargo") != "admin" or str(user_id) != str(id_url):
                return jsonify({"Acesso negado"})
            return f(*args, **kwargs)
        return checker_user
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
@check_role_user("admin")
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
@user_or_admin_user()
@jwt_required()
def updt_user_route(url_id):
    dados = request.get_json()
    if not dados:
        return jsonify({"Erro": "JSON inválido ou ausente"}), 400
    try:
        user_obj.updt(url_id, dados)
        return jsonify({"status": "sucesso"}), 200
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 400

@user_bp.route('/delete/<int:url_id>', methods=['DELETE'])
@check_role_user("admin")
def del_user_route(url_id):
    try:
        user_obj.remove(url_id)
        return jsonify({"status": "sucesso"}), 200
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 400
    
@user_bp.route('/send-token', methods=['POST'])
def send_token():
    dados = request.get_json()
    email = dados.get("email")

    if not email:
        return jsonify({"erro": "Email obrigatório"}), 400

    try:
        user = user_obj.get_by_email(email)
        if not user:
            return jsonify({"erro": "Usuário não encontrado"}), 404

        token = create_token()

        tokenSaved[email] = {
            "token": token,
            "expira": datetime.now() + timedelta(minutes=10)
        }

        send_email(email, token)

        return jsonify({"status": "Token enviado"}), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 400
    
@user_bp.route('/reset-password', methods=['PUT'])
def reset_password():
    dados = request.get_json()

    email = dados.get("email")
    token = dados.get("token")
    new_password = dados.get("senha")

    if not email or not token or not new_password:
        return jsonify({"erro": "Dados incompletos"}), 400

    registro = tokenSaved.get(email)

    if not registro:
        return jsonify({"erro": "Token não encontrado"}), 400

    if registro["token"] != token:
        return jsonify({"erro": "Token inválido"}), 400

    if datetime.now() > registro["expira"]:
        return jsonify({"erro": "Token expirado"}), 400

    try:
        user_obj.update_password_by_email(email, new_password)
        del tokenSaved[email]
        return jsonify({"status": "Senha atualizada com sucesso"}), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 400    

# @user_bp.route('/ping', methods=["GET"])
# def ping():
#     return jsonify({"status": "Funcionou esssa bagaça"}), 200