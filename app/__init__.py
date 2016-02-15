import os
from flask import Flask, Blueprint
from flask.ext.bootstrap import Bootstrap

app_blueprint = Blueprint('app', __name__)
bootstrap = Bootstrap()


from . import view, error


def create_app(config_name):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY', 'temp')

    bootstrap.init_app(app)

    app.register_blueprint(app_blueprint)

    return app
