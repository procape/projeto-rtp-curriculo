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

# Segundo banco de dados externo (PHPMyAdmin / MySQL remoto)
codigo_server_2 = os.getenv("MYSQL2_HOST", "192.168.171.93")
porta_2 = os.getenv("MYSQL2_PORT", "3306")
user_2 = os.getenv("MYSQL2_USER", "procape")
senha_2 = os.getenv("MYSQL2_PASSWORD", "huprocape")
banco_2 = os.getenv("MYSQL2_DATABASE", "rh_db")


##Configuração de acesso das rotas
