from flask import Blueprint, request, jsonify, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity, verify_jwt_in_request
from functools import wraps
from modules.curriculo.curr import Curriculo
import os
from werkzeug.utils import secure_filename

# define upload folder
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'backend', 'uploads', 'curriculos')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

curriculo_bp = Blueprint('curriculo_bp', __name__, url_prefix='/curriculo')
curriculo_obj = Curriculo()


def parse_courses_from_form(form):
    cursos = []
    nomes = form.getlist('curso[]') or form.getlist('curso') or []
    datas = form.getlist('curso_data[]') or form.getlist('curso_data') or []
    for index, nome in enumerate(nomes):
        nome = nome.strip()
        if not nome:
            continue
        cursos.append({
            'curso': nome,
            'data_conclusao': datas[index] if index < len(datas) and datas[index] else None
        })
    return cursos


def filter_curriculo_fields(form):
    return {
        key: value
        for key, value in form.items()
        if key not in ('curso[]', 'curso_data[]', 'curso', 'curso_data')
    }


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
    try:
        cursos = []
        if request.files or request.form:
            form = request.form
            dados = filter_curriculo_fields(form)
            cursos = parse_courses_from_form(form)
            f = request.files.get('arquivo')
            if f and f.filename:
                filename = secure_filename(f.filename)
                f.save(os.path.join(UPLOAD_FOLDER, filename))
                dados['arquivo'] = filename
        else:
            dados = request.get_json() or {}
            cursos_json = dados.pop('cursos', None) or []
            if isinstance(cursos_json, list):
                cursos = [
                    {
                        'curso': curso.get('curso') if isinstance(curso, dict) else curso,
                        'data_conclusao': curso.get('data_conclusao') if isinstance(curso, dict) else None
                    }
                    for curso in cursos_json
                    if (isinstance(curso, dict) and curso.get('curso')) or isinstance(curso, str)
                ]

        if not dados:
            return jsonify({"erro": "JSON inválido ou ausente"}), 400

        curriculo_obj.post(dados, cursos=cursos)
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
        import traceback
        tb = traceback.format_exc()
        print('Error in lista_self_curr:', str(e))
        print(tb)
        return jsonify({"status": "erro", "mensagem": str(e), "trace": tb}), 400


@curriculo_bp.route('/<int:url_id>', methods=['PUT'])
@user_or_admin_curr()
def updt_curr_route(url_id):
    try:
        cursos = []
        if request.files or request.form:
            form = request.form
            dados = filter_curriculo_fields(form)
            cursos = parse_courses_from_form(form)
            f = request.files.get('arquivo')
            if f and f.filename:
                filename = secure_filename(f.filename)
                f.save(os.path.join(UPLOAD_FOLDER, filename))
                dados['arquivo'] = filename
            if form.get('remover_arquivo') in ['true', 'True', '1']:
                dados['arquivo'] = None
        else:
            dados = request.get_json() or {}
            cursos_json = dados.pop('cursos', None) or []
            if isinstance(cursos_json, list):
                cursos = [
                    {
                        'curso': curso.get('curso') if isinstance(curso, dict) else curso,
                        'data_conclusao': curso.get('data_conclusao') if isinstance(curso, dict) else None
                    }
                    for curso in cursos_json
                    if (isinstance(curso, dict) and curso.get('curso')) or isinstance(curso, str)
                ]

        if not dados:
            return jsonify({"erro": "JSON inválido ou ausente"}), 400

        curriculo_obj.updt(url_id, dados, cursos=cursos)
        return jsonify({"status": "sucesso"}), 200
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 400


@curriculo_bp.route('/file/<path:filename>', methods=['GET'])
def serve_file(filename):
    try:
        return send_from_directory(UPLOAD_FOLDER, filename)
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 404


@curriculo_bp.route('/<int:url_id>/file', methods=['DELETE'])
@user_or_admin_curr()
def delete_file(url_id):
    try:
        lista = curriculo_obj.get_self(url_id)
        if not lista:
            return jsonify({"status": "erro", "mensagem": "Currículo não encontrado"}), 404
        curr = lista[0]
        arquivo = curr.get('arquivo')
        if not arquivo:
            return jsonify({"status": "erro", "mensagem": "Nenhum arquivo para remover"}), 400
        path = os.path.join(UPLOAD_FOLDER, arquivo)
        if os.path.exists(path):
            os.remove(path)
        curriculo_obj.updt(url_id, {'arquivo': None})
        return jsonify({"status": "sucesso"}), 200
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 400


@curriculo_bp.route('/<int:url_id>', methods=['DELETE'])
@check_role_curr("admin")
def del_curr_route(url_id):
    try:
        # remove arquivo do filesystem, se existir
        lista = curriculo_obj.get_self(url_id)
        if lista:
            curr = lista[0]
            arquivo = curr.get('arquivo')
            if arquivo:
                path = os.path.join(UPLOAD_FOLDER, arquivo)
                if os.path.exists(path):
                    os.remove(path)

        curriculo_obj.remove(url_id)
        return jsonify({"status": "sucesso"}), 200
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 400
