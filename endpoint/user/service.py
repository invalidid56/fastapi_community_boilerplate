from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, delete, update
from endpoint.user.entity import UserCreate
from data.db.models import User

# TODO: Exception: 중복 id 생성 방지, 없는 id 조회 방지, 없는 id 삭제 방지, 없는 id 수정 방지
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(session: Session, user_create: UserCreate):
    stmt = (
        insert(User)
        .values(
            username=user_create.username,
            password=pwd_context.hash(user_create.password1),
            email=user_create.email
        )
    )
    try:
        res = session.execute(stmt)
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
        raise e

    return res


def get_user(session: Session, username: str):
    stmt = (
        select(User)
        .where(User.username == username)
    )

    res = session.execute(stmt)

    return res.scalars().first()


def update_user(session: Session, username: str, user_create: UserCreate):
    stmt = (
        update(User)
        .where(User.username == username)
        .values(
            username=user_create.username,
            password=pwd_context.hash(user_create.password1),
            email=user_create.email
        )
    )

    res = session.execute(stmt)
    session.commit()

    return res


def delete_user(session: Session, username: str):
    stmt = (
        delete(User)
        .where(User.username == username)
    )

    res = session.execute(stmt)
    session.commit()

    return res
