from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from endpoint.board import repository, entity
from config import DB_CONFIG


async def create_board(name: str, public: bool, user_id: int) -> None:
    try:
        await repository.create_board({
            'name': name,
            'public': public,
            'user_id': user_id
        })
    except IntegrityError as e:
        if DB_CONFIG['rdb'].startswith('postgres'):
            code: int = int(e.orig.pgcode)
        elif DB_CONFIG['rdb'].startswith('mysql'):
            code: int = int(e.orig.args[0])
        else:
            raise HTTPException(status_code=500, detail="unknown internal server error")
        if code == 23505 or code == 1062:
            raise HTTPException(status_code=403, detail="title must be unique")
        elif code == 23503 or code == 1452:
            raise HTTPException(status_code=404, detail="user id not found")
        else:

            raise HTTPException(status_code=500, detail=f"{e.orig.pgcode}: {e.orig}")


async def get_board(board_id: int, user_id: int) -> entity.BoardGet:
    board = await repository.get_board(board_id)

    if board is None:
        raise HTTPException(status_code=404, detail="board not found")
    if not board.public and board.user_id != user_id:
        raise HTTPException(status_code=403, detail="you can't access this board")

    return board


async def get_board_list(per_page: int, page: int, user_id: int, order_by_artile: bool) -> list[entity.BoardGet]:
    boards = await repository.get_boards(user_id=user_id,
                                         per_page=per_page,
                                         page=page,
                                         order_by_article=order_by_artile)

    if boards is None:
        raise HTTPException(status_code=404, detail="board not found")

    return boards


async def update_board(board_id: int, name: str, public: bool, user_id: int) -> None:
    board = await repository.get_board(board_id)

    if board is None:
        raise HTTPException(status_code=404, detail="board not found")
    if board.user_id != user_id:
        raise HTTPException(status_code=403, detail="you can't access this board")

    try:
        await repository.update_board(board_id, {
            'name': name,
            'public': public
        })
    except IntegrityError:
        raise HTTPException(status_code=403, detail="name must be unique")


async def delete_board(board_id: int, user_id: int) -> None:
    board = await repository.get_board(board_id)

    if board is None:
        raise HTTPException(status_code=404, detail="board not found")
    if board.user_id != user_id:
        raise HTTPException(status_code=403, detail="you can't access this board")

    await repository.delete_board(board_id)
