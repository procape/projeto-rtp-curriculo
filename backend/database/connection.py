from sqlalchemy import create_engine, MetaData
from config.settings import codigo_server, porta, user, senha, banco
import os

db_uri = os.getenv("DATABASE_URI", f'mysql+pymysql://{user}:{senha}@{codigo_server}:{porta}/{banco}')
engine = create_engine(db_uri)
meta = MetaData()

try:
    meta.reflect(bind=engine)
except Exception as e:
    print(f"Aviso: Não foi possível conectar ao banco. Detalhe: {e}")

