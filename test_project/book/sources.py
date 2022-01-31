import http

from flask import Blueprint, jsonify, request
from flask.views import MethodView

from test_project.models import BookModel, AuthorModel, db
from test_project.schemes import ListBookModelScheme, BookScheme, ListBookWithAuthorsModelScheme
from test_project.utils.validate_request import validate_request

bp = Blueprint("book", __name__, url_prefix="/book")


class BookApi(MethodView):

    def get(self):
        with_authors = request.args.get('with_authors', False)
        books_objects = BookModel.query.filter_by(is_deleted=False).all()

        if not books_objects:
            return jsonify({"items": []}), http.HTTPStatus.OK

        if with_authors:
            books = ListBookWithAuthorsModelScheme(items=books_objects)
        else:
            books = ListBookModelScheme(items=books_objects)

        return books.json(), http.HTTPStatus.OK

    def post(self):
        new_book_scheme = validate_request(BookScheme)

        authors_objects = AuthorModel.query.filter(AuthorModel.id.in_(new_book_scheme.authors)).all()

        if not authors_objects:
            return jsonify(message=http.HTTPStatus.BAD_REQUEST.phrase), http.HTTPStatus.BAD_REQUEST

        new_book_model = BookModel(
            name=new_book_scheme.name,
            number_pages=new_book_scheme.number_pages,
            authors=authors_objects
        )

        db.session.add(new_book_model)
        db.session.commit()

        return jsonify(message=http.HTTPStatus.CREATED.phrase), http.HTTPStatus.CREATED

    def put(self, id):
        update_data_scheme = validate_request(BookScheme)
        book_object = BookModel.query.filter_by(
            id=id,
            is_deleted=False
        ).first_or_404()

        new_authors_objects = AuthorModel.query.filter(AuthorModel.id.in_(update_data_scheme.authors)).all()

        if not new_authors_objects:
            return jsonify(message=http.HTTPStatus.BAD_REQUEST.phrase), http.HTTPStatus.BAD_REQUEST

        book_object.name = update_data_scheme.name
        book_object.number_pages = update_data_scheme.number_pages
        book_object.authors = new_authors_objects

        db.session.commit()

        return jsonify(message=http.HTTPStatus.OK.phrase), http.HTTPStatus.OK

    def delete(self, id):
        book_object = BookModel.query.filter_by(
            id=id,
            is_deleted=False
        ).first_or_404()

        book_object.is_deleted = True

        db.session.commit()

        return jsonify(message=http.HTTPStatus.OK.phrase), http.HTTPStatus.OK


bp.add_url_rule(
    "/books", view_func=BookApi.as_view("books"), methods=["GET", "POST"]
)

bp.add_url_rule(
    "/<id>",
    view_func=BookApi.as_view("book"),
    methods=["PUT", "DELETE"],
)
