from functools import wraps
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from config import SQLALCHEMY_DATABASE_URL


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={
        "check_same_thread": False
    }
)

if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_async_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    engine = create_async_engine(SQLALCHEMY_DATABASE_URL)

Base = declarative_base()

async_session = AsyncSession(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)


class Transactional:
    def __call__(self, func):
        @wraps(func)
        async def _transactional(*args, **kwargs):
            async with async_session as session:
                if kwargs.get("session"):
                    result = await func(*args, **kwargs)
                    await session.commit()
                    return result
                try:
                    kwargs["session"] = session
                    result = await func(*args, **kwargs)
                    await session.commit()
                except Exception as e:
                    # logger.exception(f"{type(e).__name__} : {str(e)}")
                    await session.rollback()
                    raise e

                return result

        return _transactional
