from passlib.context import CryptContext
from endpoint.user import repository, entity
from sqlalchemy.exc import IntegrityError, NoResultFound
from fastapi import HTTPException


# TODO: Exception: 중복 id 생성 방지, 없는 id 조회 방지, 없는 id 삭제 방지, 없는 id 수정 방지
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_user(username: str) -> entity.User:
    res = await repository.get_user(username=username)

    if res is None:
        raise HTTPException(status_code=404, detail="user not found")

    return res


async def create_user(username: str, email: str, password: str) -> None:
    try:
        await repository.create_user({
            'username': username,
            'email': email,
            'password': pwd_context.hash(password)
        })
    except IntegrityError as e:
        code = e.code
        msg = e.orig

        if code == 1062:
            raise HTTPException(status_code=403, detail="username must be unique")
        else:
            raise HTTPException(status_code=500, detail=f"Unknown Error: {msg}")


async def update_user(username: str, email: str, password: str) -> None:
    try:
        await repository.update_user({
            'username': username,
            'email': email,
            'password': pwd_context.hash(password)
        })
    except IntegrityError as e:
        code = e.code
        msg = e.orig

        if code == 1062:
            raise HTTPException(status_code=403, detail="username must be unique")
        elif code == 1452:
            raise HTTPException(status_code=404, detail="user_id not found")
        else:
            raise HTTPException(status_code=500, detail=f"Unknown Error: {msg}")

    except NoResultFound:
        raise HTTPException(status_code=404, detail="user_id not found")


async def delete_user(username) -> None:
    try:
        await repository.delete_user(username)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="user_id not found")
