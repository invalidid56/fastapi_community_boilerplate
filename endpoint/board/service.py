from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from endpoint.board import repository, entity
from config import SQLALCHEMY_DATABASE_URL


def create_board(name: str, public: bool, user_id: int) -> None:
    try:
        repository.create_board({
            'name': name,
            'public': public,
            'user_id': user_id
        })
    except IntegrityError as e:
        code = e.code
        msg = e.orig

        if code == 1062 if SQLALCHEMY_DATABASE_URL.startswith('mysql') else 'gkpj':
            raise HTTPException(status_code=403, detail="name must be unique")
        elif code == 1452 if SQLALCHEMY_DATABASE_URL.startswith('mysql') else 1064:
            raise HTTPException(status_code=404, detail="user_id not found")
        else:
            raise HTTPException(status_code=500, detail="unknown internal server error")


def get_board(board_id: int, user_id: int) -> entity.BoardGet:
    board = repository.get_board(board_id)

    if board is None:
        raise HTTPException(status_code=404, detail="board not found")
    if not board.public and board.user_id != user_id:
        raise HTTPException(status_code=403, detail="you can't access this board")

    return board


def get_board_list(per_page: int, page: int, user_id: int) -> list[entity.BoardGet]:
    boards = repository.get_boards(user_id=user_id,
                                   per_page=per_page,
                                   page=page)

    if boards is None:
        raise HTTPException(status_code=404, detail="board not found")

    return boards


def update_board(board_id: int, name: str, public: bool, user_id: int) -> None:
    board = repository.get_board(board_id)

    if board is None:
        raise HTTPException(status_code=404, detail="board not found")
    if board.user_id != user_id:
        raise HTTPException(status_code=403, detail="you can't access this board")

    try:
        repository.update_board(board_id, {
            'name': name,
            'public': public
        })
    except IntegrityError:
        raise HTTPException(status_code=403, detail="name must be unique")


def delete_board(board_id: int, user_id: int) -> None:
    board = repository.get_board(board_id)

    if board is None:
        raise HTTPException(status_code=404, detail="board not found")
    if board.user_id != user_id:
        raise HTTPException(status_code=403, detail="you can't access this board")

    repository.delete_board(board_id)
