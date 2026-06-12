from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from sqlalchemy import text
from database.connection import engine

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
    with engine.connect() as conn:
        colaborador = conn.execute(
            text("""
                SELECT
                    id,
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

    # 3. Define cargo padrão
    cargo = "usuario"

    # CPFs administradores
    if cpf in ["cpf do adm"]:
        cargo = "admin"

    # 4. Gera token
    token = create_access_token(
        identity=str(colaborador["id"]),
        additional_claims={"role": cargo, "cpf": cpf},
    )

    return jsonify({
        "access_token": token,
        "user_id": colaborador["id"],
        "cargo": cargo,
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