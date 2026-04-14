from sqlalchemy import insert, select, update, delete
from database.connection import engine, meta


class Curriculo():
    def __init__(self):
        self.curr = meta.tables.get('curriculo')

    def post(self, dados):
        with engine.begin() as conn:
            conn.execute(insert(self.curr), dados)

    def get(self):
        with engine.connect() as conn:
            lista = conn.execute(select(self.curr))
            return [dict(r._mapping) for r in lista]

    def get_self(self, user_id):
        with engine.connect() as conn:
            lista = conn.execute(
                select(self.curr).where(self.curr.c.user_id == user_id)
            )
            return [dict(r._mapping) for r in lista]

    def updt(self, id_curriculo, dados):
        with engine.begin() as conn:
            conn.execute(
                update(self.curr).where(self.curr.c.id == id_curriculo).values(dados)
            )

    def remove(self, id_curr):
        with engine.begin() as conn:
            conn.execute(delete(self.curr).where(self.curr.c.id == id_curr))