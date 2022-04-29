"""
Flask API main file
"""

from flask import Flask

from models import db


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '123secret'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    from blueprints.open import bp_open
    app.register_blueprint(bp_open)

    from blueprints.filter import blueprint
    app.register_blueprint(blueprint)

    from blueprints.movie import bp_movie
    app.register_blueprint(bp_movie)

    # from blueprints.user import bp_user
    # app.register_blueprint(bp_user)

    return app


app = create_app()
