from data.db.database import Transactional
from data.db.models import Article
from sqlalchemy import select, insert, update, delete


@Transactional()
def create_article(article_req: dict, session=None) -> None:
    _article = Article(**article_req)

    session.add(_article)
    session.commit()
    session.refresh(_article)


@Transactional()
def get_article(article_id: int, session=None):
    stmt = (
        select(Article)
        .where(Article.id == article_id)
    )
    res = session.execute(stmt)

    return res.scalars().first()


@Transactional()
def get_articles(board_id: int, per_page: int, page: int, session=None):
    stmt = (
        select(Article)
        .where(Article.board_id == board_id)
        .limit(per_page).offset((page - 1) * per_page)
    )

    res = session.execute(stmt)

    return res.scalars().all()


@Transactional()
def update_article(article_id: int, article_req: dict, session=None) -> None:
    stmt = (
        update(Article)
        .where(Article.id == article_id)
        .values(**article_req)
    )

    session.execute(stmt)


@Transactional()
def delete_article(article_id: int, session=None) -> None:
    stmt = (
        delete(Article)
        .where(Article.id == article_id)
    )

    session.execute(stmt)
