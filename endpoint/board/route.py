"""
- Create : name, public (boolean) 을 입력 받아 게시판을 생성합니다. name 은 unique 해야합니다. public 이 true 이면 전체 로그인 된 유저에게 공개, public 이 false 이면 생성자에게만 공개되는 게시판입니다.
- Update : 게시판 id, name, public 을 입력 받아 해당 게시판의 name, public 을 수정합니다. 타 유저가 생성한 게시판은 수정할 수 없습니다.
- Delete : 게시판 id 를 입력 받아 해당 게시판을 삭제합니다. 타 유저가 생성한 게시판은 삭제할 수 없습니다.
- Get: 게시판 id 를 입력 받아 게시판을 조회합니다. 본인이 생성하거나, 전체 공개된 게시판을 조회할 수 있습니다.
- List : 게시판 목록을 조회합니다. 본인이 생성하거나, 전체 공개된 게시판을 조회할 수 있습니다. 게시판 목록은 **해당 게시판에 작성된 게시글의 갯수** 순으로 정렬 가능해야 합니다.
"""

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
