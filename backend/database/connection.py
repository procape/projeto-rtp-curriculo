from sqlalchemy import create_engine, MetaData
from config.settings import (
    codigo_server,
    porta,
    user,
    senha,
    banco,
    codigo_server_2,
    porta_2,
    user_2,
    senha_2,
    banco_2,
)
import os


def build_mysql_uri(host, port, username, password, database):
    return f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"

# Conexão principal do projeto
primary_db_uri = os.getenv(
    "DATABASE_URI",
    build_mysql_uri(codigo_server, porta, user, senha, banco),
)
engine = create_engine(primary_db_uri)
meta = MetaData()

# Segunda conexão para o banco remoto RH
secondary_db_uri = os.getenv(
    "DATABASE2_URI",
    build_mysql_uri(codigo_server_2, porta_2, user_2, senha_2, banco_2),
)
engine_rh = create_engine(secondary_db_uri)
meta_rh = MetaData()

try:
    meta.reflect(bind=engine)
except Exception as e:
    print(f"Aviso: Não foi possível conectar ao banco principal. Detalhe: {e}")

try:
    meta_rh.reflect(bind=engine_rh)
except Exception as e:
    print(f"Aviso: Não foi possível conectar ao banco secundário. Detalhe: {e}")

