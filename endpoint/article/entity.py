from pydantic import BaseModel


class ArticleCreate(BaseModel):
    title: str
    content: str
    board_id: int

    class Config:
        orm_mode = True


class ArticleGet(BaseModel):
    title: str
    content: str
    board_id: int
    user_id: int

    class Config:
        orm_mode = True


class ArticleUpdate(BaseModel):
    title: str
    content: str

    class Config:
        orm_mode = True
