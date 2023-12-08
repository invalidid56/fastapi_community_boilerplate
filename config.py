import os
from dotenv import load_dotenv

load_dotenv()

CREDENTIAL_SECRET_KEY = os.getenv("CREDENTIAL_SECRET_KEY", "")
CREDENTIAL_ALGORITHM = os.getenv("CREDENTIAL_ALGORITHM", "")

DB_CONFIG = {
    "rdb": os.getenv("RDB", "postgresql+asyncpg"),
    "db_user": os.getenv("DB_USER", ""),
    "db_password": os.getenv("DB_PASSWORD", ""),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5433"),
    "db": os.getenv("DB", ""),
}


REDIS_CONFIG = {
    "host": os.getenv("REDIS_HOST", "localhost"),
    "port": os.getenv("REDIS_PORT", "6379"),
    "db": os.getenv("REDIS_DB", "0"),
    "password": os.getenv("REDIS_PASSWORD", ""),
}
