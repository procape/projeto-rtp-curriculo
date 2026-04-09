from sqlalchemy import create_engine, MetaData, insert, select,update, delete
import sys
import os
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
raiz_do_projeto = os.path.abspath(os.path.join(diretorio_atual, "../../.."))
if raiz_do_projeto not in sys.path:
    sys.path.insert(0, raiz_do_projeto)
from backend.config.settings import *


engine = create_engine(f'mysql+pymysql://{user}:{senha}@{codigo_server}:{porta}/{banco}')
meta = MetaData()
meta.reflect(bind=engine)

#GET/POST de usuário
class User():
    def __init__(self):
        self.user = meta.tables['usuario']
    def post(self, dados):    
        with engine.begin() as conn:
            conn.execute(insert(self.user), dados)
    def get(self):
        with engine.connect() as conn:
            lista = conn.execute(select(self.user))
            user_list = [dict(r._mapping) for r in lista]
        return user_list
    def updt(self, id_user, dados):
        with engine.begin() as conn:
            info = (update(self.user)
                    .where(self.user.c.id == id_user)
                    .values(dados))
            conn.execute(info)
            
    def remove(self, id_user):
        with engine.begin() as conn:
            info = (delete(self.user).where(self.user.c.id == id_user))
            conn.execute(info)