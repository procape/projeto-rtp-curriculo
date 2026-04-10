from flask import Flask
from modules.user.user_routes import user_bp
from modules.curriculo.curriculo_routes import curriculo_bp

def create_app():
    app = Flask(__name__)
    
    app.register_blueprint(user_bp)
    app.register_blueprint(curriculo_bp)
    
    return app
