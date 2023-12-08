from datetime import timedelta, datetime

from fastapi import APIRouter, HTTPException
from fastapi import Depends, Response
from starlette import status

from endpoint.user import entity, service
from endpoint.user.service import create_session, authenticate_user


router: APIRouter = APIRouter(
    prefix="/user"
)


@router.post("/signup",
             status_code=status.HTTP_200_OK,
             summary="Sign up new user")
async def user_create(_user_create: entity.UserCreate) -> None:
    await service.create_user(username=_user_create.username,
                              email=_user_create.email,
                              password1=_user_create.password1,
                              password2=_user_create.password2)


@router.post("/login",
             summary="Login user, return session id")
async def login_for_access_token(response: Response, user_id: int = Depends(authenticate_user)) -> dict:
    session_id = await create_session(user_id=user_id)

    response.set_cookie(key='session_id', value=session_id)

    return {
        'message': 'login success',
        'session_id': session_id
    }
