from data.db.database import Transactional
from data.db.models import Article
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession


@Transactional()
async def create_article(article_req: dict, session: AsyncSession = None) -> None:
    _article: Article = Article(**article_req)

    session.add(_article)
    await session.commit()
    await session.refresh(_article)


@Transactional()
async def get_article(article_id: int, session: AsyncSession = None) -> Article:
    stmt = (
        select(Article)
        .where(Article.id == article_id)
    )
    res = await session.execute(stmt)

    return res.scalars().first()


@Transactional()
async def get_articles(board_id: int, per_page: int, page: int, session: AsyncSession = None) -> list[Article]:
    stmt = (
        select(Article)
        .where(Article.board_id == board_id)
        .limit(per_page).offset((page - 1) * per_page)
    )

    res = await session.execute(stmt)

    return res.scalars().all()


@Transactional()
async def update_article(article_id: int, article_req: dict, session: AsyncSession = None) -> None:
    stmt = (
        update(Article)
        .where(Article.id == article_id)
        .values(**article_req)
    )

    await session.execute(stmt)


@Transactional()
async def delete_article(article_id: int, session: AsyncSession = None) -> None:
    stmt = (
        delete(Article)
        .where(Article.id == article_id)
    )

    await session.execute(stmt)
