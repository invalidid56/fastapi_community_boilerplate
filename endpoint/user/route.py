from datetime import timedelta, datetime

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status

from data.db.database import get_db
from endpoint.user import entity, service
from endpoint.user.service import pwd_context

from config import CREDENTIAL_ALGORITHM, CREDENTIAL_ALGORITHM

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 4
SECRET_KEY = CREDENTIAL_ALGORITHM
ALGORITHM = CREDENTIAL_ALGORITHM
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

token_blacklist = set()

router = APIRouter(
    prefix="/user"
)


@router.post("/signup",
             status_code=status.HTTP_200_OK,
             summary="Sign up new user")
def user_create(_user_create: entity.UserCreate,
                session: Session = Depends(get_db)):
    service.create_user(session=session,

                        user_create=_user_create)


@router.post("/login",
             response_model=entity.Token,
             summary="Login user, return access token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                           session: Session = Depends(get_db)):
    # from_data = OAuth2PasswordRequestForm(username=username, password=password)
    user = service.get_user(session, form_data.username)

    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect Username or PW',
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Make Access Token (JWT) : username, expire time
    data = {
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    access_token = jwt.encode(
        data, SECRET_KEY, algorithm=ALGORITHM
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username
    }


@router.post("/logout",
             response_model=entity.Token,
             summary="Logout user, deprecate access token")
def logout_for_access_token(token: str = Depends(oauth2_scheme)):
    # Access Token 받아서 로그아웃 시키기
    # TODO: JWT Stateless에 위반됨, Client-Side에서 Token을 지워야 함
    token_blacklist.add(token)
    return {'message': 'Successfully logged out'}


def get_current_user(token: str = Depends(oauth2_scheme),
                     session: Session = Depends(get_db)):
    # Validate Token, return user if valid
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception

        if token in token_blacklist:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    else:
        user = service.get_user(session, username=username)
        if user is None:
            raise credentials_exception
        return user
