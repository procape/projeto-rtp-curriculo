from flask import Blueprint, jsonify
from .rh import Colaboradores
from flask_jwt_extended import jwt_required

rh_bp = Blueprint('rh', __name__, url_prefix='/rh')
colab_obj = Colaboradores()


@rh_bp.route('/colaboradores', methods=['GET'])
@jwt_required()
def listar_colaboradores():
    try:
        # se a tabela não foi refletida no metadata, retornar 404
        if not colab_obj.table:
            return jsonify({"erro": "Tabela 'colaboradores' não encontrada no banco RH."}), 404

        dados = colab_obj.get_all()

        if not dados:
            return jsonify({"mensagem": "Nenhum colaborador encontrado."}), 404

        return jsonify(dados), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
