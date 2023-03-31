from datetime import datetime
from enum import Enum
from typing import List, Optional

from fastapi_users import fastapi_users, FastAPIUsers
from pydantic import BaseModel, Field

from fastapi import FastAPI, Request, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ValidationError
from fastapi.responses import JSONResponse

from auth.auth import auth_backend
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate
from auth.database import User

myapp = FastAPI(
    title='FastAPIApp'
)
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

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


@myapp.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"


@myapp.get("/unprotected-route")
def unprotected_route():
    return "Hello, Vasya"


fake_users = [
    {'id': 1, 'role': 'admin', 'name': 'Bob'},
    {'id': 2, 'role': 'investor', 'name': 'John'},
    {'id': 3, 'role': 'trador', 'name': 'Matt'},
    {'id': 4, 'role': 'investor', 'name': 'Homer', 'degree': [
        {'id': 1, 'created_at': '2020-01-01T00:00:00', 'type_degree': 'expert'}
    ]},
]

fake_trades = [
    {'id': 1, 'user_id': 1, 'currency': 'BTC', 'side': 'buy', 'price': 123, 'amount': 2.12},
    {'id': 2, 'user_id': 1, 'currency': 'BTC', 'side': 'sell', 'price': 125, 'amount': 2.12}
]


class DegreeType(Enum):
    newbie = 'newbie'
    expert = 'expert'


class Degree(BaseModel):
    id: int
    created_at: datetime
    type_degree: DegreeType


class User(BaseModel):
    id: int
    role: str
    name: str
    degree: Optional[List[Degree]] = []


@myapp.get('/users/{user_id}', response_model=list[User])
def get_user(user_id: int):
    return [user for user in fake_users if user['id'] == user_id]


@myapp.get('/trades')
def get_trades(limit: int, offset: int = 0):
    return fake_trades[offset:][:limit]


@myapp.post('/users/{user_id}')
def change_user(user_id: int, new_name: str):
    current_user = list(filter(lambda user: user['id'] == user_id, fake_users))[0]
    current_user['name'] = new_name
    return {'status': 200, 'data': current_user}


class Trade(BaseModel):
    id: int
    user_id: int
    currency: str = Field(max_length=5)
    side: str
    price: float = Field(ge=0)
    amount: float


@myapp.post('/trades')
def add_trades(trades: list[Trade]):
    fake_trades.extend(trades)
    return {'status': 200, 'data': fake_trades}


@myapp.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()}),
    )
