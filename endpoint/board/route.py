# TODO: list에서 개수 순 정렬 기능 추가
from fastapi import APIRouter
from fastapi import Depends
from starlette import status

from data.db.models import User
from endpoint.board import entity, service
from endpoint.user.service import get_current_user

router = APIRouter(
    prefix="/board",
    tags=["board"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, summary="Create new board")
async def create_board(board_create: entity.BoardCreate,
                       user_id: int = Depends(get_current_user)) -> dict:
    await service.create_board(
        name=board_create.name,
        public=board_create.public,
        user_id=user_id
    )

    return {'message': 'success'}


@router.get("/{board_id}", response_model=entity.BoardGet, summary="Get board")
async def get_board(board_id: int,
                    user_id: int = Depends(get_current_user)) -> entity.BoardGet:
    return await service.get_board(
        board_id=board_id,
        user_id=user_id
    )


@router.get("/", response_model=list[entity.BoardGet], summary="Get board list")
async def get_board_list(per_page: int = 10,
                         page: int = 1,
                         order_by_artile: bool = True,
                         user_id: int = Depends(get_current_user)) -> list[entity.BoardGet]:
    return await service.get_board_list(
        per_page=per_page,
        page=page,
        user_id=user_id,
        order_by_artile=order_by_artile
    )


@router.put("/{board_id}", status_code=status.HTTP_200_OK, summary="Update board")
async def update_board(board_id: int,
                       board_update: entity.BoardCreate,
                       user_id: int = Depends(get_current_user)) -> dict:
    await service.update_board(
        board_id=board_update.id,
        name=board_update.name,
        public=board_update.public,
        user_id=user_id
    )

    return {'message': 'success'}


@router.delete("/{board_id}", status_code=status.HTTP_200_OK, summary="Delete board")
async def delete_board(board_id: int,
                       user: User = Depends(get_current_user)) -> dict:
    await service.delete_board(
        board_id=board_id,
        user_id=user.id
    )

    return {'message': 'success'}
