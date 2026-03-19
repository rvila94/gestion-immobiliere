from flask import Flask
from app.api.routes.users import users_bp

def register_routes(app: Flask):
    app.register_blueprint(users_bp)