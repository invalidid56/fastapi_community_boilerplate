from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from endpoint.article import repository, entity
from endpoint.board.service import get_board
from config import SQLALCHEMY_DATABASE_URL


def create_article(board_id: int, title: str, content: str, user_id: int) -> None:
    try:
        repository.create_article({
            'title': title,
            'content': content,
            'board_id': board_id,
            'user_id': user_id
        })
    except IntegrityError as e:
        code = e.code
        msg = e.orig

        if code == 1062 if SQLALCHEMY_DATABASE_URL.startswith('mysql') else 'gkpj':
            raise HTTPException(status_code=403, detail="title must be unique")
        elif code == 1452 if SQLALCHEMY_DATABASE_URL.startswith('mysql') else 1064:
            raise HTTPException(status_code=404, detail="board_id not found")
        else:
            raise HTTPException(status_code=500, detail="unknown internal server error")


def get_article(article_id: int, user_id: int) -> entity.ArticleGet:
    article = repository.get_article(article_id)

    if article is None:
        raise HTTPException(status_code=404, detail="article not found")
    if article.board.user_id is not user_id and not article.board.public:
        raise HTTPException(status_code=403, detail="you can't access this article")

    return article


def get_article_list(board_id: int, per_page: int, page: int, user_id: int) -> list[entity.ArticleGet]:
    _ = get_board(board_id=board_id, user_id=user_id)   # Check if Accessible

    articles = repository.get_articles(board_id=board_id,
                                       per_page=per_page,
                                       page=page)

    if articles is None:
        raise HTTPException(status_code=404, detail="article not found")

    return articles


def update_article(article_id: int, title: str, content: str, user_id: int) -> None:
    article = repository.get_article(article_id)

    if article is None:
        raise HTTPException(status_code=404, detail="article not found")
    if article.user_id != user_id:
        raise HTTPException(status_code=403, detail="you can't access this article")

    try:
        repository.update_article(article_id, {
            'title': title,
            'content': content
        })
    except IntegrityError:
        raise HTTPException(status_code=403, detail="title must be unique")


def delete_article(article_id: int, user_id: int) -> None:
    article = repository.get_article(article_id)

    if article is None:
        raise HTTPException(status_code=404, detail="article not found")
    if article.user_id != user_id:
        raise HTTPException(status_code=403, detail="you can't access this article")

    repository.delete_article(article_id)
