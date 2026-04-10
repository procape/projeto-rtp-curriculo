from sqlalchemy import Table, Column, String, Date, DateTime, Integer, func, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from database.connection import engine, meta

class CreateTables():
    def __init__(self):
        usuario = Table(
            'usuario', meta,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('cpf', String(100), nullable=False, unique=True),
            Column('nome', String(100), nullable=False),
            Column('email', String(100), nullable=False),
            Column('senha', String(100), nullable=False),
            Column('cargo', String(20), nullable=False, server_default="usuario"),
        )

        curriculo = Table(
            'curriculo', meta,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('nome_completo', String(100), nullable=False),
            Column('email', String(100), nullable=False, unique=True),
            Column('telefone', String(20), nullable=False),
            Column('rua_logradouro', String(200), nullable=False),
            Column('bairro', String(100), nullable=False),
            Column('cidade', String(100), nullable=False),
            Column('escolaridade', String(100), nullable=False),
            Column('experiencia', String(50), nullable=True),
            Column('atuacao', String(150), nullable=False),
            Column('habilidades', String(255), nullable=False),
            Column('observacoes', String(255)),
            Column('data_cad', DateTime, server_default=func.now()),
            Column('data_updt', DateTime, onupdate=func.now()),
            Column('user_id', Integer, ForeignKey('usuario.id', ondelete='SET NULL'), nullable=True)
        )
        meta.create_all(engine)
tabelas = CreateTables()