from datetime import datetime

from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr

class UserList(BaseModel):
    users : list[UserPublic]


class BookSchema(BaseModel):
    ano: int
    titulo: str
    romancista_id: int


class BookResponse(BaseModel):
    id: int
    ano: int
    titulo: str
    romancista_id: int
    created_at: str
    updated_at: str


class BookListResponse(BaseModel):
    books: list[BookResponse]


class TokenData(BaseModel):
    access_token: str
    token_type: str


class TokenResresh(BaseModel):
    token: str


class RomancistSchema(BaseModel):
    nome: str


class RomancistResponse(BaseModel):
    id: int
    nome: str
    created_at: datetime
    updated_at: datetime


class RomancistListResponse(BaseModel):
    romancists: list[RomancistResponse]
