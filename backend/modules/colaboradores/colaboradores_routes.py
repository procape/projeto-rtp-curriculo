import traceback
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import select, func
from database.connection import engine, meta

colab_bp = Blueprint('colab_bp', __name__, url_prefix='/colaboradores')


def normalize_cpf(cpf):
    if cpf is None:
        return None
    return ''.join([c for c in str(cpf) if c.isdigit()])


@colab_bp.route('/me', methods=['GET'])
@jwt_required()
def get_me():

    try:
        user_id_jwt = get_jwt_identity()
        try:
            user_id_jwt = int(user_id_jwt)
        except (TypeError, ValueError):
            pass
        usuario_table = meta.tables.get('usuario')
        if usuario_table is None:
            return jsonify({'erro': 'Tabela usuario não encontrada'}), 500

        with engine.connect() as conn:
            res = conn.execute(select(usuario_table.c.cpf).where(usuario_table.c.id == user_id_jwt)).fetchone()
            if not res:
                return jsonify({'erro': 'Usuário não encontrado'}), 404
            cpf = normalize_cpf(res[0])

            col_table = meta.tables.get('colaboradores')
            if col_table is None:
                return jsonify({'erro': 'Tabela colaboradores não encontrada'}), 500

            cpf_col = func.replace(func.replace(func.replace(func.replace(func.replace(col_table.c.cpf, '.', ''), '-', ''), '/', ''), ' ', ''), '(', '')
            cpf_col = func.replace(cpf_col, ')', '')
            col = conn.execute(select(col_table).where(cpf_col == cpf)).fetchone()
            if not col:
                return jsonify({'erro': 'Colaborador não encontrado'}), 404
            mapped = dict(col._mapping)
            keys_keep = ['nome', 'email_pessoal', 'telefone', 'cep', 'logradouro', 'numero', 'complemento', 'bairro', 'cidade', 'estado']
            out = {k: mapped.get(k) for k in keys_keep}
            return jsonify(out), 200
    except Exception as e:
        trace = traceback.format_exc()
        print('Error in /colaboradores/me:', str(e))
        print(trace)
        return jsonify({'erro': str(e), 'trace': trace}), 400
