import os
from sqlalchemy import create_engine, MetaData
from config.settings import codigo_server, porta, user, senha, banco

db_uri = os.getenv(
    "DATABASE_URI",
    f"mysql+pymysql://{user}:{senha}@{codigo_server}:{porta}/{banco}?charset=utf8mb4"
)

engine = create_engine(db_uri, pool_pre_ping=True)
meta = MetaData()

try:
    meta.reflect(bind=engine)
    print("Banco conectado com sucesso.")
except Exception as e:
    print(f"Erro ao conectar no banco: {e}")