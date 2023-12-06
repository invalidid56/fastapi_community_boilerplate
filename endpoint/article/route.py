from fastapi import APIRouter
from fastapi import Depends
from starlette import status

from data.db.models import User
from endpoint.article import entity, service
from endpoint.user.route import get_current_user

router = APIRouter(
    prefix="/article",
    tags=["article"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, summary="Create new article")
def create_article(article_create: entity.ArticleCreate,
                   user: User = Depends(get_current_user)) -> dict:
    service.create_article(
        title=article_create.title,
        content=article_create.content,
        board_id=article_create.board_id,
        user_id=user.id
    )

    return {'message': 'success'}


@router.get("/{article_id}", response_model=entity.ArticleGet, summary="Get article")
def get_article(article_id: int,
                user: User = Depends(get_current_user)) -> entity.ArticleGet:
    return service.get_article(
        article_id=article_id,
        user_id=user.id
    )


@router.get("/", response_model=list[entity.ArticleGet], summary="Get article list")
def get_article_list(board_id: int,
                     per_page: int = 10,
                     page: int = 1,
                     user: User = Depends(get_current_user)) -> list[entity.ArticleGet]:
    return service.get_article_list(
        board_id=board_id,
        per_page=per_page,
        page=page,
        user_id=user.id
    )


@router.put("/{article_id}", status_code=status.HTTP_200_OK, summary="Update article")
def update_article(article_id: int,
                   article_update: entity.ArticleUpdate,
                   user: User = Depends(get_current_user)) -> dict:
    service.update_article(
        article_id=article_id,
        title=article_update.title,
        content=article_update.content,
        user_id=user.id
    )

    return {'message': 'success'}


@router.delete("/{article_id}", status_code=status.HTTP_200_OK, summary="Delete article")
def delete_article(article_id: int,
                   user: User = Depends(get_current_user)) -> dict:
    service.delete_article(
        article_id=article_id,
        user_id=user.id
    )

    return {'message': 'success'}
