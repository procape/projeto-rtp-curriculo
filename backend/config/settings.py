import os
from dotenv import load_dotenv
from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt, get_jwt_identity, verify_jwt_in_request

load_dotenv()

codigo_server = os.getenv("MYSQL_HOST", "localhost")
porta = os.getenv("MYSQL_PORT", "3306")
user = os.getenv("MYSQL_USER", "root")
senha = os.getenv("MYSQL_PASSWORD", "senha_nao_e_toor")
banco = os.getenv("MYSQL_DATABASE", "db_rtp")


##Configuração de acesso das rotas
