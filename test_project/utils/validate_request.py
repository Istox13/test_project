import http

from flask import abort, request
from pydantic import ValidationError


def validate_request(scheme):
    data = request.get_json()

    if not data:
        abort(http.HTTPStatus.BAD_REQUEST)

    try:
        parsed_data = scheme.parse_obj(data)
    except ValidationError as validation_error:
        abort(http.HTTPStatus.BAD_REQUEST, validation_error.json())

    return parsed_data
