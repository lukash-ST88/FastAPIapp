from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_users import FastAPIUsers
from redis import asyncio as aioredis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth.base_config import auth_backend, fastapi_users
from fastapi.staticfiles import StaticFiles
from auth.schemas import UserRead, UserCreate

from operations.router import router as router_operations

from pages.router import router as router_pages
from tasks.router import router as router_tasks
from chat.router import router as router_chat
from config import REDIS_HOST, REDIS_PORT


myapp = FastAPI(
    title='FastAPIApp'
)

origins = [
    "http://localhost",
    "http://localhost:8080",
]

myapp.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)

myapp.mount('/static', StaticFiles(directory='static'), name='static')

myapp.include_router(router_operations)
myapp.include_router(router_pages)
myapp.include_router(router_tasks)
myapp.include_router(router_chat)

myapp.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

myapp.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
current_user = fastapi_users.current_user()


# cache
@myapp.on_event("startup")
async def startup():
    redis = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

# TODO: sqlalchemy result.all() - исправить
# TODO: pytest - исправить
# TODO: tests - исследовать SMTP
# TODO: разобраться с js + websockets(консоль браузера)
# TODO: security FastAPI кастомная аутентификация

