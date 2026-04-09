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
            Column('cidade', String(150), nullable=False),
            Column('estado', String(2), nullable=False),
            Column('linkedin', String(100), unique=True),
            Column('portfolio', String(100)),
            Column('objetivo', String(100)),
            Column('observacoes', String(255)),
            Column('data_cad', DateTime, server_default=func.now()),
            Column('data_updt', DateTime, onupdate=func.now()),
            Column('user_id', Integer, ForeignKey('usuario.id'), nullable=False)
        )
        
        formacoes = Table(
            'formacoes', meta,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('curso', String(45), nullable=False),
            Column('instituicao', String(45), nullable=False),
            Column('nivel', String(45), nullable=False),
            Column('inicio', Date, nullable=False),
            Column('fim', Date),
            Column('status', String(45))
        )
        
        habilidades = Table(
            'habilidades', meta,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('habilidades', String(45), nullable=False),
            Column('nivel', String(45), nullable=False)
        )
        
        experiencias = Table(
            'experiencias', meta,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('empresa', String(45), nullable=False),
            Column('cargo', String(45), nullable=False),
            Column('inicio', Date, nullable=False),
            Column('fim', Date),
            Column('status', String(45), nullable=False)
        )
        
        residente_formacoes = Table(
            'residente_formacoes', meta,
            Column('res_id', Integer, ForeignKey('curriculo.id'), nullable=False),
            Column('form_id', Integer, ForeignKey('formacoes.id'), nullable=False)
        )
        
        residente_habilidades = Table(
            'residente_habilidades', meta,
            Column('res_id', Integer, ForeignKey('curriculo.id'), nullable=False),
            Column('hab_id', Integer, ForeignKey('habilidades.id'), nullable=False)
        )
        
        residente_experiencias = Table(
            'residente_experiencias', meta,
            Column('res_id', Integer, ForeignKey('curriculo.id'), nullable=False),
            Column('exp_id', Integer, ForeignKey('experiencias.id'), nullable=False)
        )
        
        meta.create_all(engine)
teste = CreateTables()