from flask import Flask
from app.api.routes.users import users_bp
from app.api.routes.properties import properties_bp

def register_routes(app: Flask):
    app.register_blueprint(users_bp)
    app.register_blueprint(properties_bp)