import pytest
from flask import Flask
from app.core.extensions import db
from app.models.user import User
import datetime

@pytest.fixture
def app():
    """App Flask de test avec DB en mémoire."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = True

    db.init_app(app)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def sample_user(app):
    """Utilisateur déjà présent en base."""
    user = User(
        first_name="Bob",
        last_name="Dubois",
        email="bob.dubois@example.com",
        birth_date=datetime.date(2000, 1, 1)
    )
    db.session.add(user)
    db.session.commit()
    return user