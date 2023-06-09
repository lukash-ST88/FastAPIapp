from typing import AsyncGenerator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker
from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
# создание модели таблицы user
Base: DeclarativeMeta = declarative_base()

engine = create_async_engine(DATABASE_URL)  # точка входа sqlalchemy в приложение
# временные сессии(соединения) с бд
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

metadata = MetaData()  # аккумулированная информация о созданных таблицах императивным методом


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

# class User(SQLAlchemyBaseUserTable[int], Base):
# #     # все field берутся из SQLAlchemyBaseUserTable[int], пункта else, они неявно уже встроены, здесь для наглядности делаем их явными
# #     email = Column(String, nullable=False)
# #     hashed_password: str = Column(String(length=1024), nullable=False)
# #     is_active: bool = Column(Boolean, default=True, nullable=False)
# #     is_superuser: bool = Column(Boolean, default=False, nullable=False)
# #     is_verified: bool = Column(Boolean, default=False, nullable=False)
# #     # далее пользовательские fields
# #     id = Column(Integer, primary_key=True)
# #     username = Column(String, nullable=False)
# #     registered_at = Column(TIMESTAMP, default=datetime.utcnow) # время регистрации пользователя
# #     role_id = Column(Integer, ForeignKey(role.c.id))

# async def get_user_db(session: AsyncSession = Depends(get_async_session)):
#     yield SQLAlchemyUserDatabase(session, User)
