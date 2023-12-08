from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from data.db.models import Board, Article
from data.db.database import Transactional


@Transactional()
async def create_board(board_req: dict, session: AsyncSession = None) -> None:
    _board: Board = Board(**board_req)

    session.add(_board)
    await session.commit()
    await session.refresh(_board)


@Transactional()
async def get_board(board_id: int, session: AsyncSession = None):
    stmt = (
        select(Board)
        .where(Board.id == board_id)
    )
    res = await session.execute(stmt)

    return res.scalars().first()


@Transactional()
async def get_boards(
        user_id: int, per_page: int, page: int, order_by_article: bool = True, session: AsyncSession = None
):
    if order_by_article:
        stmt = (
            select(Board,
                   func.count(Article.id).label('article_count'))
            .where((Board.user_id == user_id) | (Board.public is True))
            .outerjoin(Article, Board.id == Article.board_id)
            .group_by(Board.id)
            .order_by(func.count(Article.id).desc())
            .limit(per_page).offset((page - 1) * per_page)
        )
    else:
        stmt = (
            select(Board)
            .where((Board.user_id == user_id) | (Board.public is True))
            .limit(per_page).offset((page - 1) * per_page)
        )

    res = await session.execute(stmt)

    return res.scalars().all()


@Transactional()
async def update_board(board_id: int, board_req: dict, session: AsyncSession = None) -> None:
    stmt = (
        update(Board)
        .where(Board.id == board_id)
        .values(**board_req)
    )

    await session.execute(stmt)


@Transactional()
async def delete_board(board_id: int, session: AsyncSession = None) -> None:
    stmt = (
        delete(Board)
        .where(Board.id == board_id)
    )

    await session.execute(stmt)
