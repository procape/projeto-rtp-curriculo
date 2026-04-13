from flask import Flask
from flask_jwt_extended import JWTManager
from modules.user.user_routes import user_bp
from modules.curriculo.curriculo_routes import curriculo_bp
import os
from dotenv import load_dotenv
jwt = JWTManager()
load_dotenv()

def create_Router():
    router = Flask(__name__)
    router.config["JWT_SECRET_KEY"] = os.getenv("JWT_KEY")
    jwt.init_app(router)
    router.register_blueprint(user_bp)
    router.register_blueprint(curriculo_bp)