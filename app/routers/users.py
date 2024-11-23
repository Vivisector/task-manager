from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Annotated
from app.schemas import CreateUser, UpdateUser, UserResponse
from app.models.user import User  # Модель базы данных
from app.backend.db_depends import get_db  # Зависимость для подключения к БД
from slugify import slugify
from sqlalchemy import insert, update, delete


# Создаём роутер
router = APIRouter(prefix="/user", tags=["user"])
# router = APIRouter()

@router.get("/", response_model=list[UserResponse])
async def all_users(db: Annotated[Session, Depends(get_db)]):
    # Выполняем запрос к БД
    query = select(User)
    result = db.scalars(query).all()
    return result

# @router.get("/", response_model=list[UserResponse])
# async def all_users(db: Annotated[Session, Depends(get_db)]):
#     # Выполняем запрос к БД
#     query = select(User)
#     result = db.scalars(query).all()
#     return result

##############################
# @router.get("/{user_id}")
# def user_by_id(user_id: int):
#     pass  # Реализация будет позже
@router.get("/{user_id}", response_model=UserResponse)
async def user_by_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    query = select(User).where(User.id == user_id)
    result = db.scalar(query)
    if result is None:
        raise HTTPException(status_code=404, detail="User was not found")
    return result

##########################
# @router.post("/create")
# def create_user():
#     pass  # Реализация будет позже

@router.post("/create", response_model=dict)
async def create_user(user_data: CreateUser, db: Annotated[Session, Depends(get_db)]):
    # Генерация slug на основе имени пользователя
    slug = slugify(user_data.username)

    # Попытка вставить запись в базу данных
    stmt = insert(User).values(
        username=user_data.username,
        firstname=user_data.firstname,
        lastname=user_data.lastname,
        age=user_data.age,
        slug=slug
    )
    db.execute(stmt)
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}

# @router.post('/create')
# async def create_user(db: Annotated[Session, Depends(get_db)], create_user: CreateUser):
#     db.execute(insert(User).values(name = create_user.username,
#                                    firstname = create_user.firstname,
#                                    lastname = create_user.lastname,
#                                    age = create_user.age,
#                                    slug = slugify(create_user.username)))
#     db.commit()
#     return {
#         'status_code': status.HTTP_201_CREATED,
#         'transaction': 'Successful'
#     }

# async def create_user(db: Annotated[Session, Depends(get_db)], create_user: CreateUser):

####################
# @router.put("/update")
# def update_user():
#     pass  # Реализация будет позже

@router.put("/update/{user_id}")
async def update_user(user_id: int, user_data: UpdateUser, db: Annotated[Session, Depends(get_db)]):
    # Попытка обновить запись
    upd_query = (
        update(User)
        .where(User.id == user_id)
        .values(
            firstname=user_data.firstname,
            lastname=user_data.lastname,
            age=user_data.age
        )
    )
    result = db.execute(upd_query)
    db.commit()

    # Проверяем, обновилась ли запись
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="User was not found")

    return {'status_code': status.HTTP_200_OK, 'transaction': 'User update is successful!'}


# @router.delete("/delete")
# def delete_user():
#     pass  # Реализация будет позже

@router.delete("/delete/{user_id}")
async def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    # Попытка удалить запись
    stmt = delete(User).where(User.id == user_id)
    result = db.execute(stmt)
    db.commit()

    # Проверяем, удалена ли запись
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="User was not found")

    return {'status_code': status.HTTP_200_OK, 'transaction': 'User deletion is successful!'}
