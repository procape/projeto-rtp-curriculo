from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from sqlalchemy import select
from datetime import datetime, timedelta
from database.connection import engine
from modules.gerador_tabelas import tabelas
from modules.user.user import User
from modules.forgot.send_token import create_token, send_email
from extensions import bcrypt

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
user_obj = User()
tokenSaved = {}


@auth_bp.route('/login', methods=["POST"])
def login():
    dados = request.get_json()
    tabela = tabelas.usuario
    query = select(tabela).where(tabela.c.email == dados.get("email"))
    with engine.connect() as conn:
        user = conn.execute(query).fetchone()

    if user and bcrypt.check_password_hash(user.senha, dados.get("senha")):
        token = create_access_token(
            identity=str(user.id),
            additional_claims={"role": user.cargo},
        )
        return jsonify(access_token=token), 200
    return jsonify({"status": "Erro de login"}), 401


@auth_bp.route('/forgot-password', methods=["POST"])
def forgot_password():
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


@auth_bp.route('/reset-password', methods=["PUT"])
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