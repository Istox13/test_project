import datetime
from uuid import UUID
from typing import List

from pydantic import BaseModel


class BaseModelScheme(BaseModel):
    id: UUID
    is_deleted: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True


class AuthorScheme(BaseModel):
    full_name: str


class AuthorModelScheme(BaseModelScheme):
    full_name: str


class ListAuthorModelScheme(BaseModel):
    items: List[AuthorModelScheme]

    class Config:
        orm_mode = True


class BookScheme(BaseModel):
    name: str
    number_pages: int
    authors: List[str]


class BookModelScheme(BaseModelScheme):
    name: str
    number_pages: int


class ListBookModelScheme(BaseModel):
    items: List[BookModelScheme]

    class Config:
        orm_mode = True


class BookWithAuthorsModelScheme(BaseModel):
    name: str
    number_pages: int
    authors: List[AuthorModelScheme]

    class Config:
        orm_mode = True


class ListBookWithAuthorsModelScheme(BaseModel):
    items: List[BookWithAuthorsModelScheme]
