# TODO: list에서 개수 순 정렬 기능 추가
from datetime import timedelta, datetime

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status

from data.db.database import get_db
from data.db.models import User
from endpoint.board import entity, service
from endpoint.user.route import get_current_user

from config import CREDENTIAL_ALGORITHM, CREDENTIAL_ALGORITHM

router = APIRouter(
    prefix="/board",
    tags=["board"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, summary="Create new board")
def create_board(board_create: entity.BoardCreate,
                 user: User = Depends(get_current_user)) -> dict:
    service.create_board(
        name=board_create.name,
        public=board_create.public,
        user_id=user.id
    )

    return {'message': 'success'}


@router.get("/{board_id}", response_model=entity.BoardGet, summary="Get board")
def get_board(board_id: int,
              user: User = Depends(get_current_user)) -> entity.BoardGet:
    return service.get_board(
        board_id=board_id,
        user_id=user.id
    )


@router.get("/", response_model=list[entity.BoardGet], summary="Get board list")
def get_board_list(per_page: int = 10,
                   page: int = 1,
                   user: User = Depends(get_current_user)) -> list[entity.BoardGet]:  # Query로 개발했음, 의존성 주입 필요
    return service.get_board_list(
        per_page=per_page,
        page=page,
        user_id=user.id
    )


@router.put("/{board_id}", status_code=status.HTTP_200_OK, summary="Update board")
def update_board(board_id: int,
                 board_update: entity.BoardCreate,
                 user: User = Depends(get_current_user)) -> dict:
    service.update_board(
        board_id=board_update.id,
        name=board_update.name,
        public=board_update.public,
        user_id=user.id
    )

    return {'message': 'success'}


@router.delete("/{board_id}", status_code=status.HTTP_200_OK, summary="Delete board")
def delete_board(board_id: int,
                 user: User = Depends(get_current_user)) -> dict:
    service.delete_board(
        board_id=board_id,
        user_id=user.id
    )

    return {'message': 'success'}
