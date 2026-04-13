from flask import Flask
from modules.user.user_routes import user_bp
from modules.curriculo.curriculo_routes import curriculo_bp
from modules import gerador_tabelas

def create_app():
    app = Flask(__name__)
    
    gerador_tabelas.CreateTables()
    
    app.register_blueprint(user_bp)
    app.register_blueprint(curriculo_bp)
    
    return app
