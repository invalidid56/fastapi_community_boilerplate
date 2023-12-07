from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from endpoint.article import repository, entity
from endpoint.board.service import get_board
from data.db.models import Article
from config import DB_CONFIG


async def create_article(board_id: int, title: str, content: str, user_id: int) -> None:
    try:
        await repository.create_article({
            'title': title,
            'content': content,
            'board_id': board_id,
            'user_id': user_id
        })
    except IntegrityError as e:
        if DB_CONFIG['rdb'].startswith('postgres'):
            code: int = int(e.orig.pgcode)
        elif DB_CONFIG['rdb'].startswith('mysql'):
            code: int = e.orig.args[0]
        else:
            raise HTTPException(status_code=500, detail="unknown internal server error")

        if code == 23505 or code == 1062:
            raise HTTPException(status_code=403, detail="title must be unique")
        elif code == 23503 or code == 1452:
            raise HTTPException(status_code=404, detail="board_id not found")
        else:
            raise HTTPException(status_code=500, detail="unknown internal server error")


async def get_article(article_id: int, user_id: int) -> entity.ArticleGet:
    article: Article = await repository.get_article(article_id)

    if article is None:
        raise HTTPException(status_code=404, detail="article not found")
    if article.board.user_id is not user_id and not article.board.public:
        raise HTTPException(status_code=403, detail="you can't access this article")

    return article


async def get_article_list(board_id: int, per_page: int, page: int, user_id: int) -> list[entity.ArticleGet]:
    _ = await get_board(board_id=board_id, user_id=user_id)  # Check if Accessible

    articles: list[Article] = await repository.get_articles(board_id=board_id,
                                                            per_page=per_page,
                                                            page=page)

    if articles is None:
        raise HTTPException(status_code=404, detail="article not found")

    return articles


async def update_article(article_id: int, title: str, content: str, user_id: int) -> None:
    article: Article = await repository.get_article(article_id)

    if article is None:
        raise HTTPException(status_code=404, detail="article not found")
    if article.user_id != user_id:
        raise HTTPException(status_code=403, detail="you can't access this article")

    try:
        await repository.update_article(article_id, {
            'title': title,
            'content': content
        })
    except IntegrityError:
        raise HTTPException(status_code=403, detail="title must be unique")


async def delete_article(article_id: int, user_id: int) -> None:
    article: Article = await repository.get_article(article_id)

    if article is None:
        raise HTTPException(status_code=404, detail="article not found")
    if article.user_id != user_id:
        raise HTTPException(status_code=403, detail="you can't access this article")

    await repository.delete_article(article_id)
