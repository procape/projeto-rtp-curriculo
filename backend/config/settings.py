import os
from dotenv import load_dotenv

load_dotenv()

codigo_server = os.getenv("MYSQL_HOST", "localhost")
porta = os.getenv("MYSQL_PORT", "3306")
user = os.getenv("MYSQL_USER", "procape")
senha = os.getenv("MYSQL_PASSWORD", "huprocape")
banco = os.getenv("MYSQL_DATABASE", "rh_db")


##Configuração de acesso das rotas
