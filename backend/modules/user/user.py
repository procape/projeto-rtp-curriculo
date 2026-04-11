from sqlalchemy import create_engine, MetaData, insert, select,update, delete
from database.connection import engine, meta

class User():
    def __init__(self):
        self.user = meta.tables.get('usuario')
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

    def update_password_by_email(self, email, new_password):
        with engine.begin() as conn:
            stmt = (
                update(self.user)
                .where(self.user.c.email == email)
                .values(senha=new_password)
            )
            conn.execute(stmt)