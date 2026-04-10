import os
from dotenv import load_dotenv

load_dotenv()

codigo_server = os.getenv("MYSQL_HOST", "localhost")
porta = os.getenv("MYSQL_PORT", "3306")
user = os.getenv("MYSQL_USER", "root")
senha = os.getenv("MYSQL_PASSWORD", "senha_nao_e_toor")
banco = os.getenv("MYSQL_DATABASE", "db_rtp")