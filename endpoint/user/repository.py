from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from data.db.database import Transactional
from data.db.models import User


@Transactional()
async def get_user(session: AsyncSession, username: str) -> User:
    stmt = select(User).where(User.username == username)
    result = await session.execute(stmt)
    return result.scalars().first()


@Transactional()
async def create_user(session: AsyncSession, user_req: dict) -> None:
    _user = User(**user_req)

    session.add(_user)

    await session.commit()
    await session.refresh(_user)


@Transactional()
async def update_user(session: AsyncSession, username: str, user_req: dict) -> None:
    stmt = update(User).where(User.username == username).values(**user_req)
    await session.execute(stmt)


@Transactional()
async def delete_user(session: AsyncSession, username: str) -> None:
    stmt = delete(User).where(User.username == username)
    await session.execute(stmt)

