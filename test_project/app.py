from flask import Flask

import test_project.config as cnf
from test_project.blueprints import init_blueprint
from test_project.errorhandler import init_errorhandler
from test_project.extensions import init_extensions


def create_app():
    app = Flask(__name__)
    app.config.from_object(cnf)

    init_extensions(app)
    init_blueprint(app)
    init_errorhandler(app)

    return app
