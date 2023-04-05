import time

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from operations.models import operation
from operations.schemas import OperationCreate

router = APIRouter(
    prefix='/operations',
    tags=['Operations']
)


@router.get("/log_operation")
@cache(expire=30)
async def get_long_op():
    time.sleep(2)
    return 'много данных'


@router.get('/')
async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(operation).where(operation.c.type == operation_type)
        result = await session.execute(query)
        return {
            'status': 'success',
            'data': result.scalars().all()
        }
    except:
        return {
            "status": "error",
            "details": "some error happened"
        }



@router.post('/')
async def add_specific_operations(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)): # OperationCreate - шаблон заполнения бызы данных для пользователя
    statement = insert(operation).values(**new_operation.dict())  # dict для преобразования pydentic модели в словарь
    await session.execute(statement)
    # выполение транзакции в бд
    await session.commit()
    return {'status': 'success'}
