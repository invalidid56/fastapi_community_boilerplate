from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str

    class Config:
        orm_mode = True


class UserCreate(User):
    username: str
    email: str
    password1: str
    password2: str

    class Config:
        orm_mode = True


class UserGet(User):
    username: str
    email: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
    username: str
