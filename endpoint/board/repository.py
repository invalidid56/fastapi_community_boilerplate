from sqlalchemy import insert, select, update, delete
from sqlalchemy.orm import Session, joinedload
from data.db.models import Board
from data.db.database import Transactional


@Transactional()
def create_board(board_req: dict, session: Session = None) -> None:
    _board = Board(**board_req)

    session.add(_board)
    session.commit()
    session.refresh(_board)


@Transactional()
def get_board(board_id: int, session: Session = None):
    stmt = (
        select(Board)
        .where(Board.id == board_id)
    )
    res = session.execute(stmt)

    return res.scalars().first()


@Transactional()
def get_boards(user_id: int, per_page: int, page: int, session: Session = None):
    stmt = (
        select(Board)
        .where((Board.user_id == user_id) | (Board.public == True))
        .limit(per_page).offset((page - 1) * per_page)
    )

    res = session.execute(stmt)

    return res.scalars().all()


@Transactional()
def update_board(board_id: int, board_req: dict, session: Session = None) -> None:
    stmt = (
        update(Board)
        .where(Board.id == board_id)
        .values(**board_req)
    )

    session.execute(stmt)


@Transactional()
def delete_board(board_id: int, session: Session = None) -> None:
    stmt = (
        delete(Board)
        .where(Board.id == board_id)
    )

    session.execute(stmt)
