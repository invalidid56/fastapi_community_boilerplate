import random
from datetime import datetime
from passlib.context import CryptContext
from endpoint.user import repository, entity
from sqlalchemy.exc import IntegrityError, NoResultFound
from fastapi import HTTPException, Depends, Request, status
from fastapi.security import HTTPBasicCredentials, HTTPBasic, OAuth2PasswordRequestForm
from config import DB_CONFIG
from data.redis.connection import RedisDriver


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
redis_connection: RedisDriver = RedisDriver()


async def create_session(user_id: int) -> str:
    # add session to login_session
    session_id: str = f"{user_id}{datetime.now().timestamp()}{random.randint(0, 1000)}"

    await redis_connection.set(session_id, user_id, ttl=False)
    # login_session[session_id] = user_id

    return session_id


async def authenticate_user(credentials: OAuth2PasswordRequestForm = Depends()) -> int:
    # Validate User, return id if valid
    # from_data = OAuth2PasswordRequestForm(username=username, password=password)
    user = await repository.get_user(credentials.username)

    if user is None or not pwd_context.verify(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

    return user.id


async def get_current_user(request: Request) -> int | None:
    # Validate Token, return user id if valid
    session_id: str = request.cookies.get('session_id')

    try:
        user_id: int = await redis_connection.get(session_id)
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid session ID {e}",
        )

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid session ID",
        )

    return int(user_id)   # user_id


async def get_user(username: str) -> entity.User:
    res = await repository.get_user(username=username)

    if res is None:
        raise HTTPException(status_code=404, detail="user not found")

    return res


async def create_user(username: str, email: str, password1: str, password2: str) -> None:
    if password1 != password2:
        raise HTTPException(status_code=403, detail="password1 and password2 must be same")
    try:
        await repository.create_user({
            'username': username,
            'email': email,
            'password': pwd_context.hash(password1)
        })
    except IntegrityError as e:
        if DB_CONFIG['rdb'].startswith('postgres'):
            code: int = int(e.orig.pgcode)
        elif DB_CONFIG['rdb'].startswith('mysql'):
            code: int = int(e.orig.args[0])
        else:
            raise HTTPException(status_code=500, detail="unknown database")

        if code == 23505 or code == 1062:
            raise HTTPException(status_code=403, detail="username or email must be unique")
        else:
            raise HTTPException(status_code=500, detail=f"unknown internal server error {e.orig}")


async def update_user(username: str, email: str, password: str) -> None:
    try:
        await repository.update_user({
            'username': username,
            'email': email,
            'password': pwd_context.hash(password)
        })
    except IntegrityError as e:
        if DB_CONFIG['rdb'].startswith('postgres'):
            code: int = int(e.orig.pgcode)
        elif DB_CONFIG['rdb'].startswith('mysql'):
            code: int = int(e.orig.args[0])
        else:
            raise HTTPException(status_code=500, detail="unknown database")

        if code == 23505 or code == 1062:
            raise HTTPException(status_code=403, detail="username must be unique")
        elif code == 23503 or code == 1452:
            raise HTTPException(status_code=404, detail="user_id not found")
        else:
            raise HTTPException(status_code=500, detail=f"Unknown Error: {e.orig}")


async def delete_user(username) -> None:
    try:
        await repository.delete_user(username)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="user_id not found")
