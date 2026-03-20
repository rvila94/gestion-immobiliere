from flask import Flask
from app.api.api import register_routes
from app.core.extensions import db, ma
from app.core.config import Config
import app.models

app = Flask(__name__)
app.config.from_object(Config)

# init extensions
db.init_app(app)
ma.init_app(app)

# register routes
register_routes(app)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)