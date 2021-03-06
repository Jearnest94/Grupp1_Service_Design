"""
Flask API main file
"""
import os

from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from dotenv import load_dotenv
from models import db


load_dotenv('.env')

# Swagger specific items
SWAGGER_URL = '/documentation'
SWAGGER_JSON = '/static/swagger.json'
SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    SWAGGER_JSON,
    config={
        'app_name': 'IMDB Top 1000 films api'
    }
)


def create_app():
    """
    :return: Returns the flask app
    """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '123secret'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    uri = os.getenv("DATABASE_URL")

    # if uri.startswith("postgres://"):
    #     uri = uri.replace("postgres://", "postgresql://", 1)

    app.config['SQLALCHEMY_DATABASE_URI'] = uri

    db.init_app(app)

    from blueprints.open import bp_open
    app.register_blueprint(bp_open, url_prefix='/api/v1.0')

    from blueprints.movie import bp_movie
    app.register_blueprint(bp_movie, url_prefix='/api/v1.0')

    from blueprints.review import bp_review
    app.register_blueprint(bp_review, url_prefix='/api/v1.0')

    from blueprints.user import bp_user
    app.register_blueprint(bp_user, url_prefix='/api/v1.0')

    app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix=SWAGGER_URL)

    return app


app = create_app()
