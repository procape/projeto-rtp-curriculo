from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from sqlalchemy import select
from database.connection import engine
from modules.gerador_tabelas import tabelas

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=["POST"])
def login():
    dados = request.get_json()
    tabela = tabelas.usuario
    query = select(tabela).where(tabela.c.email == dados.get("email"))
    with engine.connect() as conn:
        user = conn.execute(query).fetchone()
    
    if user and user.senha == dados.get("senha"):
        cargo = {"role": user.cargo}
        token = create_access_token(
            identity=str(user.id),
            additional_claims=cargo,
        )
        return jsonify(access_token=token), 200
    return jsonify({"Erro de login"}), 401

@auth_bp.route('/ping', methods=["GET"])
def ping():
    return jsonify({"status": "AAAAAAAAAAAAAA"}), 200