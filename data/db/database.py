from functools import wraps
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import SQLALCHEMY_DATABASE_URL


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={
        "check_same_thread": False
    }
)

if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Transactional:
    def __call__(self, func):
        @wraps(func)
        def _transactional(*args, **kwargs):
            with SessionLocal() as session:
                if kwargs.get("session"):
                    result = func(*args, **kwargs)
                    session.commit()
                    return result
                try:
                    kwargs["session"] = session
                    result = func(*args, **kwargs)
                    session.commit()
                except Exception as e:
                    # logger.exception(f"{type(e).__name__} : {str(e)}")
                    session.rollback()
                    raise e

                return result
        return _transactional
