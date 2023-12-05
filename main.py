from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from endpoint.user import route as user_router


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router.router)
