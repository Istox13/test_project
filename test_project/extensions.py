from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate(compare_type=True)


def init_extensions(app):
    CORS(app)
    db.init_app(app)

    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()

    return app
