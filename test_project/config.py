import os
from flask import cli


basedir = os.path.abspath(os.path.dirname(__file__))

cli.load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")

JSON_SORT_KEYS = False
JSONIFY_MIMETYPE = "application/json"
DEBUG = os.environ.get("DEBUG", True)
CORS = os.environ.get("CORS", False)

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = os.environ.get("POSTGRES_URI")
DEFAULT_PASSWORD = os.environ.get("DEFAULT_PASSWORD")
