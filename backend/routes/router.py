from flask import Flask
from flask_jwt_extended import JWTManager
from modules.user.user_routes import user_bp
from modules.curriculo.curriculo_routes import curriculo_bp
import os
from dotenv import load_dotenv
from flask_cors import CORS
jwt = JWTManager()
load_dotenv()

def create_Router():
    router = Flask(__name__)
    CORS(router, origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ])
    router.config["JWT_SECRET_KEY"] = os.getenv("JWT_KEY")
    jwt.init_app(router)
    router.register_blueprint(user_bp)
    router.register_blueprint(curriculo_bp)