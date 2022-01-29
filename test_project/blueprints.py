from flask import Blueprint

from test_project.book.sources import bp as bp_book
from test_project.author.sources import bp as bp_author
from test_project.index import bp as bp_index


bp_api_v1 = Blueprint("api_v1", __name__, url_prefix="/api/v1")


def init_blueprint(app):
    bp_api_v1.register_blueprint(bp_book)
    bp_api_v1.register_blueprint(bp_author)

    app.register_blueprint(bp_api_v1)
    app.register_blueprint(bp_index)

    return app


__all__ = ("init_blueprint",)
