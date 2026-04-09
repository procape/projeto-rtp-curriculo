from sqlalchemy import Table, Column, String, Date, DateTime, Integer, func, Integer, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy import MetaData
import sys
import os
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
raiz_do_projeto = os.path.abspath(os.path.join(diretorio_atual, "../.."))
if raiz_do_projeto not in sys.path:
    sys.path.insert(0, raiz_do_projeto)
from backend.config.settings import *


engine = create_engine(f'mysql+pymysql://{user}:{senha}@{codigo_server}:{porta}/{banco}')
meta = MetaData()

class CreateTables():
    def __init__(self):
        usuario = Table(
            'usuario', meta,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('cpf', String(100), nullable=False, unique=True),
            Column('nome', String(100), nullable=False),
            Column('email', String(100), nullable=False),
            Column('senha', String(100), nullable=False)
        )

        curriculo = Table(
            'curriculo', meta,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('nome_completo', String(100), nullable=False),
            Column('email', String(100), nullable=False, unique=True),
            Column('telefone', Integer, nullable=False),
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
teste = CreateTables()