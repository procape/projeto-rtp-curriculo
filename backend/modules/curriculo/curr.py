from collections import defaultdict
from sqlalchemy import insert, select, update, delete
from database.connection import engine, meta


class Curriculo():
    def __init__(self):
        self.curr = meta.tables.get('curriculo')
        self.cursos = meta.tables.get('lista_cursos')

    def _format_date(self, value):
        if value is None:
            return None
        if hasattr(value, 'isoformat'):
            return value.isoformat()
        return value

    def post(self, dados, cursos=None):
        with engine.begin() as conn:
            result = conn.execute(insert(self.curr), dados)
            curriculo_id = result.inserted_primary_key[0]
            if cursos:
                cursos_to_insert = [
                    {
                        'curriculo_id': curriculo_id,
                        'curso': c.get('curso'),
                        'data_conclusao': c.get('data_conclusao')
                    }
                    for c in cursos if c.get('curso')
                ]
                if cursos_to_insert:
                    conn.execute(insert(self.cursos), cursos_to_insert)

    def get(self):
        with engine.connect() as conn:
            lista = [dict(r._mapping) for r in conn.execute(select(self.curr))]
            if not self.cursos:
                return lista

            cursos_rows = [dict(r._mapping) for r in conn.execute(select(self.cursos))]
            cursos_por_curr = defaultdict(list)
            for curso in cursos_rows:
                cursos_por_curr[curso['curriculo_id']].append({
                    'curso': curso['curso'],
                    'data_conclusao': self._format_date(curso['data_conclusao'])
                })

            for curr in lista:
                curr['cursos'] = cursos_por_curr.get(curr['id'], [])
            return lista

    def get_self(self, user_id):
        with engine.connect() as conn:
            lista = [
                dict(r._mapping)
                for r in conn.execute(select(self.curr).where(self.curr.c.user_id == user_id))
            ]
            if not lista or not self.cursos:
                return lista

            for curr in lista:
                cursos = [
                    dict(r._mapping)
                    for r in conn.execute(select(self.cursos).where(self.cursos.c.curriculo_id == curr['id']))
                ]
                curr['cursos'] = [
                    {
                        'curso': c['curso'],
                        'data_conclusao': self._format_date(c['data_conclusao'])
                    }
                    for c in cursos
                ]
            return lista

    def updt(self, user_id, dados, cursos=None):
        with engine.begin() as conn:
            conn.execute(
                update(self.curr).where(self.curr.c.user_id == user_id).values(dados)
            )
            if cursos is not None and self.cursos:
                curriculo_row = conn.execute(
                    select(self.curr.c.id).where(self.curr.c.user_id == user_id)
                ).first()
                if curriculo_row:
                    curriculo_id = curriculo_row._mapping['id']
                    conn.execute(delete(self.cursos).where(self.cursos.c.curriculo_id == curriculo_id))
                    cursos_to_insert = [
                        {
                            'curriculo_id': curriculo_id,
                            'curso': c.get('curso'),
                            'data_conclusao': c.get('data_conclusao')
                        }
                        for c in cursos if c.get('curso')
                    ]
                    if cursos_to_insert:
                        conn.execute(insert(self.cursos), cursos_to_insert)

    def remove(self, id_curr):
        with engine.begin() as conn:
            if self.cursos:
                conn.execute(delete(self.cursos).where(self.cursos.c.curriculo_id == id_curr))
            conn.execute(delete(self.curr).where(self.curr.c.id == id_curr))