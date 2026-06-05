from sqlalchemy import select
from database.connection import engine_rh, meta_rh


class Colaboradores:
    def __init__(self):
        self.table = meta_rh.tables.get('colaboradores')

    def get_all(self):
        """Retorna lista de colaboradores com os campos solicitados.

        Campos retornados: nome, email_pessoal, telefone, cep, logradouro,
        numero, complemento, bairro, cidade, estado
        """
        if not self.table:
            return []

        cols = [
            self.table.c.nome,
            self.table.c.email_pessoal,
            self.table.c.telefone,
            self.table.c.cep,
            self.table.c.logradouro,
            self.table.c.numero,
            self.table.c.complemento,
            self.table.c.bairro,
            self.table.c.cidade,
            self.table.c.estado,
        ]

        with engine_rh.connect() as conn:
            resultado = conn.execute(select(*cols))
            return [dict(r._mapping) for r in resultado]
