from pydantic import BaseModel


class BoardCreate(BaseModel):
    name: str
    public: bool

    class Config:
        orm_mode = True


class BoardGet(BaseModel):
    name: str
    public: bool
    user_id: int
    id: int

    class Config:
        orm_mode = True
