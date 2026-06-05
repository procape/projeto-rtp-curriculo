from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from sqlalchemy import select
from datetime import datetime, timedelta
from database.connection import engine, engine_rh, meta_rh
from modules.gerador_tabelas import tabelas
from modules.user.user import User
from modules.forgot.send_token import create_token, send_email
from extensions import bcrypt

from ldap3 import Server, Connection, ALL

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
user_obj = User()
tokenSaved = {}


@auth_bp.route('/login', methods=["POST"])
def login():
    dados = request.get_json()
    cpf = dados.get('cpf')
    senha = dados.get('senha')

    if not cpf or not senha:
        return jsonify({"erro": "cpf e senha obrigatórios"}), 400

    # Configuração LDAP (ajustar conforme necessário)
    ldap_server = '192.168.150.2'
    ldap_domain = 'huprocape.upe'
    ldap_base_dn = 'DC=huprocape,DC=upe'

    usuario_completo = f"{cpf}@{ldap_domain}"

    # tentativa de bind no LDAP
    try:
        server = Server(ldap_server, get_info=ALL)
        conn = Connection(server, user=usuario_completo, password=senha, auto_bind=False)
        if not conn.bind():
            return jsonify({"erro": "CPF ou Senha inválidos (LDAP)."}), 401

        # opcional: buscar displayName no AD
        nome_completo = None
        try:
            filter_str = f"(&(objectClass=user)(sAMAccountName={cpf}))"
            attributes = ['displayName']
            if conn.search(ldap_base_dn, filter_str, attributes=attributes):
                entries = conn.entries
                if entries and len(entries) > 0 and 'displayName' in entries[0]:
                    nome_completo = str(entries[0].displayName)
        except Exception:
            nome_completo = None

        conn.unbind()

    except Exception as e:
        return jsonify({"erro": f"Erro de comunicação com LDAP: {str(e)}"}), 500

    # Verificar CPF no banco RH (segundo DB)
    colab_table = meta_rh.tables.get('colaboradores')
    if not colab_table:
        return jsonify({"erro": "Tabela 'colaboradores' não encontrada no banco RH."}), 404

    # localizar coluna cpf no schema do RH
    cpf_col = None
    for name in ['cpf', 'CPF', 'documento', 'numcpf', 'nr_cpf']:
        if name in colab_table.c:
            cpf_col = getattr(colab_table.c, name)
            break

    if cpf_col is None:
        return jsonify({"erro": "Coluna CPF não encontrada na tabela 'colaboradores' do RH."}), 500

    with engine_rh.connect() as conn_rh:
        rh_record = conn_rh.execute(select(colab_table).where(cpf_col == cpf)).fetchone()

    if not rh_record:
        return jsonify({"erro": "Usuário não encontrado no banco RH."}), 404

    # Se passou no LDAP e existe no RH, garantir que usuário local exista e gerar token
    tabela = tabelas.usuario
    query = select(tabela).where(tabela.c.cpf == cpf)
    with engine.connect() as conn:
        user = conn.execute(query).fetchone()

    if not user:
        # criar usuário local (senha irrelevante, pois autenticação será via LDAP)
        nome = nome_completo or (rh_record.nome if 'nome' in rh_record._mapping else cpf)
        email = rh_record._mapping.get('email_pessoal') or rh_record._mapping.get('email') or f'{cpf}@{ldap_domain}'
        novo = {
            'cpf': cpf,
            'nome': nome,
            'email': email,
            'senha': 'ldap-auth',
        }
        try:
            user_obj.post(novo)
        except Exception as e:
            return jsonify({"erro": f"Erro ao criar usuário local: {str(e)}"}), 500

        # recuperar usuário criado
        with engine.connect() as conn2:
            user = conn2.execute(select(tabela).where(tabela.c.cpf == cpf)).fetchone()

    token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.cargo},
    )
    return jsonify(access_token=token, user_id=user.id, cargo=user.cargo), 200


@auth_bp.route('/forgot-password', methods=["POST"])
def forgot_password():
    dados = request.get_json()
    cpf = dados.get("cpf")

    if not cpf:
        return jsonify({"erro": "cpf obrigatório"}), 400

    try:
        user = user_obj.get_by_cpf(cpf)
        if not user:
            return jsonify({"erro": "Usuário não encontrado"}), 404

        token = create_token()
        tokenSaved[cpf] = {
            "token": token,
            "expira": datetime.now() + timedelta(minutes=10)
        }
        send_email(cpf, token)
        return jsonify({"status": "Token enviado"}), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 400


@auth_bp.route('/reset-password', methods=["PUT"])
def reset_password():
    dados = request.get_json()
    cpf = dados.get("cpf")
    token = dados.get("token")
    new_password = dados.get("senha")

    if not cpf or not token or not new_password:
        return jsonify({"erro": "Dados incompletos"}), 400

    registro = tokenSaved.get(cpf)

    if not registro:
        return jsonify({"erro": "Token não encontrado"}), 400

    if registro["token"] != token:
        return jsonify({"erro": "Token inválido"}), 400

    if datetime.now() > registro["expira"]:
        return jsonify({"erro": "Token expirado"}), 400

    try:
        user_obj.update_password_by_cpf(cpf, new_password)
        del tokenSaved[cpf]
        return jsonify({"status": "Senha atualizada com sucesso"}), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 400