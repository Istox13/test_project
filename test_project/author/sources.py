import http

from flask import Blueprint, jsonify
from flask.views import MethodView

from test_project.utils.validate_request import validate_request
from test_project.schemes import AuthorScheme, ListAuthorModelScheme
from test_project.models import AuthorModel, db


bp = Blueprint("author", __name__, url_prefix="/author")


class AuthorApi(MethodView):

    def get(self):
        authors_objects = AuthorModel.query.filter_by(is_deleted=False).all()

        if not authors_objects:
            return jsonify({"items": []}), http.HTTPStatus.OK

        authors_scheme = ListAuthorModelScheme(items=authors_objects)

        return authors_scheme.json(), http.HTTPStatus.OK

    def post(self):
        new_author_scheme = validate_request(AuthorScheme)

        new_author_object = AuthorModel(
            full_name=new_author_scheme.full_name
        )

        db.session.add(new_author_object)
        db.session.commit()

        return jsonify(message=http.HTTPStatus.CREATED.phrase), http.HTTPStatus.CREATED

    def put(self, id):
        update_data_scheme = validate_request(AuthorScheme)
        author_object = AuthorModel.query.filter_by(
            id=id,
            is_deleted=False
        ).first_or_404()

        AuthorModel.query.filter_by(id=id).update(update_data_scheme.dict())
        db.session.commit()

        return jsonify(message=http.HTTPStatus.OK.phrase), http.HTTPStatus.OK

    def delete(self, id):
        author_object = AuthorModel.query.filter_by(
            id=id,
            is_deleted=False
        ).first_or_404()

        author_object.is_deleted = True
        db.session.commit()

        return jsonify(message=http.HTTPStatus.OK.phrase), http.HTTPStatus.OK


bp.add_url_rule(
    "/authors", view_func=AuthorApi.as_view("authors"), methods=["GET", "POST"]
)

bp.add_url_rule(
    "/<id>",
    view_func=AuthorApi.as_view("author"),
    methods=["PUT", "DELETE"],
)
