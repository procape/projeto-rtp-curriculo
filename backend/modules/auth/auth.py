from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from sqlalchemy import select, text
from database.connection import engine
from modules.gerador_tabelas import tabelas

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=["POST"])
def login():
    dados = request.get_json()

    cpf = ''.join(filter(str.isdigit, dados.get("cpf", "")))
    senha = dados.get("senha")

    if not cpf or not senha:
        return jsonify({"status": "CPF e senha são obrigatórios"}), 400

    if len(cpf) != 11:
        return jsonify({"status": "CPF inválido"}), 400

    # 1. Valida no LDAP
    from modules.auth.ldap_auth import autenticar_ldap

    resultado_ldap = autenticar_ldap(cpf, senha)

    if not resultado_ldap["autenticado"]:
        return jsonify({"status": "CPF ou senha inválidos no LDAP"}), 401

    # 2. Verifica CPF no banco RH - tabela colaboradores
    from sqlalchemy import text

    with engine.connect() as conn:
        colaborador = conn.execute(
            text("""
                SELECT
                    nome,
                    email_pessoal,
                    telefone,
                    cep,
                    logradouro,
                    numero,
                    complemento,
                    bairro,
                    cidade,
                    estado
                FROM colaboradores
                WHERE REPLACE(REPLACE(cpf,'.',''),'-','') = :cpf
                LIMIT 1
            """),
            {"cpf": cpf}
        ).mappings().first()

    if not colaborador:
        return jsonify({
            "status": "CPF autenticado no LDAP, mas não encontrado no banco RH"
        }), 403

    # 3. Verifica se existe na tabela usuario do sistema
    tabela = tabelas.usuario
    query = select(tabela).where(tabela.c.cpf == cpf)

    with engine.connect() as conn:
        user = conn.execute(query).fetchone()

    if not user:
        return jsonify({
            "status": "CPF encontrado no LDAP e no RH, mas não autorizado no sistema de currículo"
        }), 403

    # 4. Gera token
    token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.cargo},
    )

    return jsonify({
        "access_token": token,
        "user_id": user.id,
        "cargo": user.cargo,
        "cpf": cpf,
        "nome": colaborador["nome"],
        "email": colaborador["email_pessoal"],
        "telefone": colaborador["telefone"],
        "cep": colaborador["cep"],
        "logradouro": colaborador["logradouro"],
        "numero": colaborador["numero"],
        "complemento": colaborador["complemento"],
        "bairro": colaborador["bairro"],
        "cidade": colaborador["cidade"],
        "estado": colaborador["estado"],
        "nome_ldap": resultado_ldap["nome_completo"]
    }), 200
