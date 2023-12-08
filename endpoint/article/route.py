from fastapi import APIRouter
from fastapi import Depends
from starlette import status

from data.db.models import User
from endpoint.article import entity, service
from endpoint.user.service import get_current_user

router = APIRouter(
    prefix="/article",
    tags=["article"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, summary="Create new article")
async def create_article(article_create: entity.ArticleCreate,
                         user_id: int = Depends(get_current_user)) -> dict:
    await service.create_article(
        title=article_create.title,
        content=article_create.content,
        board_id=article_create.board_id,
        user_id=user_id
    )

    return {'message': 'success'}


@router.get("/{article_id}", response_model=entity.ArticleGet, summary="Get article")
async def get_article(article_id: int,
                      user_id: int = Depends(get_current_user)) -> entity.ArticleGet:
    return await service.get_article(
        article_id=article_id,
        user_id=user_id
    )


@router.get("/", response_model=list[entity.ArticleGet], summary="Get article list")
async def get_article_list(board_id: int,
                           per_page: int = 10,
                           page: int = 1,
                           user_id: int = Depends(get_current_user)) -> list[entity.ArticleGet]:
    return await service.get_article_list(
        board_id=board_id,
        per_page=per_page,
        page=page,
        user_id=user_id
    )


@router.put("/{article_id}", status_code=status.HTTP_200_OK, summary="Update article")
async def update_article(article_id: int,
                         article_update: entity.ArticleUpdate,
                         user_id: int = Depends(get_current_user)) -> dict:
    await service.update_article(
        article_id=article_id,
        title=article_update.title,
        content=article_update.content,
        user_id=user_id
    )

    return {'message': 'success'}


@router.delete("/{article_id}", status_code=status.HTTP_200_OK, summary="Delete article")
async def delete_article(article_id: int,
                         user_id: int = Depends(get_current_user)) -> dict:
    await service.delete_article(
        article_id=article_id,
        user_id=user_id
    )

    return {'message': 'success'}
