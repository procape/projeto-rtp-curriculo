from sqlalchemy import insert, select, update, delete
from database.connection import engine, meta
from extensions import bcrypt


class User():
    def __init__(self):
        self.user = meta.tables.get('usuario')

    def post(self, dados):
        dados = dict(dados)
        dados['senha'] = bcrypt.generate_password_hash(dados['senha']).decode('utf-8')
        with engine.begin() as conn:
            conn.execute(insert(self.user), dados)

    def get(self):
        with engine.connect() as conn:
            lista = conn.execute(select(self.user))
            return [dict(r._mapping) for r in lista]

    def get_self(self, id_user):
        with engine.connect() as conn:
            resultado = conn.execute(
                select(self.user).where(self.user.c.id == id_user)
            ).fetchone()
            return dict(resultado._mapping) if resultado else None

    def updt(self, id_user, dados):
        with engine.begin() as conn:
            conn.execute(
                update(self.user).where(self.user.c.id == id_user).values(dados)
            )

    def remove(self, id_user):
        with engine.begin() as conn:
            conn.execute(delete(self.user).where(self.user.c.id == id_user))

    def get_by_email(self, email):
        with engine.connect() as conn:
            resultado = conn.execute(
                select(self.user).where(self.user.c.email == email)
            ).fetchone()
            return dict(resultado._mapping) if resultado else None

    def update_password_by_email(self, email, new_password):
        hashed = bcrypt.generate_password_hash(new_password).decode('utf-8')
        with engine.begin() as conn:
            conn.execute(
                update(self.user).where(self.user.c.email == email).values(senha=hashed)
            )