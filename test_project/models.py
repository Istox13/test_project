import uuid

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from test_project.extensions import db


association_table = sa.Table(
    'association_books_to_authors',
    db.Model.metadata,
    sa.Column('book_id', sa.ForeignKey('books.id'), primary_key=True),
    sa.Column('author_id', sa.ForeignKey('authors.id'), primary_key=True)
)


class BaseModel(db.Model):
    __abstract__ = True

    id = sa.Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=uuid.uuid4,
        comment="Идентификатор",
    )

    is_deleted = sa.Column(
        sa.Boolean,
        nullable=False,
        default=False,
        comment="Удалено?",
    )

    created_at = sa.Column(
        sa.DateTime,
        nullable=False,
        default=sa.func.current_timestamp(),
        comment="Дата создания",
    )

    updated_at = sa.Column(
        sa.DateTime,
        nullable=False,
        default=sa.func.current_timestamp(),
        onupdate=sa.func.current_timestamp(),
        comment="Дата обновления",
    )


class AuthorModel(BaseModel):
    __tablename__ = "authors"

    full_name = sa.Column(
        sa.String(256),
        nullable=False,
        default="",
        comment="ФИО автора"
    )


class BookModel(BaseModel):
    __tablename__ = "books"

    name = sa.Column(
        sa.String(512),
        nullable=False,
        default="",
        comment="Название книги"
    )

    number_pages = sa.Column(
        sa.Integer,
        nullable=False,
        default=0,
        comment="Колличество страниц"
    )

    authors = db.relationship(
        "AuthorModel",
        secondary=association_table
    )
