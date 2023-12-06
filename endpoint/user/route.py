from datetime import timedelta, datetime

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from starlette import status

from endpoint.user import entity, service
from endpoint.user.service import pwd_context
from data.db.models import User

from config import CREDENTIAL_ALGORITHM

ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 4
SECRET_KEY: str = CREDENTIAL_ALGORITHM
ALGORITHM: str = CREDENTIAL_ALGORITHM
oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="/user/login")


router: APIRouter = APIRouter(
    prefix="/user"
)


@router.post("/signup",
             status_code=status.HTTP_200_OK,
             summary="Sign up new user")
async def user_create(_user_create: entity.UserCreate) -> None:
    await service.create_user(username=_user_create.username,
                              email=_user_create.email,
                              password=_user_create.password)


@router.post("/login",
             response_model=entity.Token,
             summary="Login user, return access token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> dict:
    # from_data = OAuth2PasswordRequestForm(username=username, password=password)
    user: User = await service.get_user(form_data.username)

    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect Username or PW',
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Make Access Token (JWT) : username, expire time
    data: dict = {
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    access_token: str = jwt.encode(
        data, SECRET_KEY, algorithm=ALGORITHM
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username
    }


def get_current_user(token: str = Depends(oauth2_scheme)) -> User | None:
    # Validate Token, return user if valid
    credentials_exception: HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload: dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    else:
        user: User = service.get_user(username=username)
        if user is None:
            raise credentials_exception
        return user
