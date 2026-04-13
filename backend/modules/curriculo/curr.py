from sqlalchemy import create_engine, MetaData, insert, select, update, delete
from database.connection import engine, meta

class Curriculo():
    def __init__(self):
        self.curr = meta.tables.get('curriculo')
    
    def post(self, dados):
        with engine.begin() as conn:
            conn.execute(insert(self.curr), dados)
    
    def get(self):
        with engine.begin() as conn:
            lista = conn.execute(select(self.curr))
            curr_list = [dict(r._mapping) for r in lista]
            return curr_list
    def get_self(self, id_curr):
        with engine.connect() as conn:
            lista = conn.execute(select(self.curr).where(self.curr.c.id == id_curr))
            return lista
    def updt(self, id_curriculo, dados):
        with engine.begin() as conn:
            info = (update(self.curr)
                    .where(self.curr.c.id == id_curriculo)
                    .values(dados))
            conn.execute(info)
            
    def remove(self, id_curr):
        with engine.begin() as conn:
            info = (delete(self.curr).where(self.curr.c.id == id_curr))
            conn.execute(info)