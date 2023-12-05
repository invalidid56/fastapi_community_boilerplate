from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from data.db.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    password = Column(String)


class Board(Base):
    __tablename__ = "board"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    public = Column(Boolean, default=True)

    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", backref="boards")


class Article(Base):
    __tablename__ = "article"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    content = Column(String)

    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", backref="articles")

    board_id = Column(Integer, ForeignKey("board.id"))
    board = relationship("Board", backref="articles")
