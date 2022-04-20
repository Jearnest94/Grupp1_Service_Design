from flask import Flask


def create_app():
    app = Flask(__name__)

    @app.route('/v1/testing')
    def test():
        return 'Testing'

    return app


app = create_app()
