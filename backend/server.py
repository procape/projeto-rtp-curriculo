from flask import Flask
from flask_jwt_extended import JWTManager
from modules.user.user_routes import user_bp
from modules.curriculo.curriculo_routes import curriculo_bp
from modules.auth.auth import auth_bp
from modules import gerador_tabelas
import os
from dotenv import load_dotenv
from flask_cors import CORS
load_dotenv()
def create_app():
    app = Flask(__name__)
    CORS(app, origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ])
    gerador_tabelas.CreateTables()
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_KEY")
    jwt = JWTManager(app)
    app.register_blueprint(user_bp)
    app.register_blueprint(curriculo_bp)
    app.register_blueprint(auth_bp)
    
    return app
