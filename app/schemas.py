from pydantic import BaseModel


# Схемы для пользователей
class CreateUser(BaseModel):
    username: str
    firstname: str
    lastname: str
    age: int


class UpdateUser(BaseModel):
    firstname: str
    lastname: str
    age: int

class UserResponse(BaseModel):
    id: int
    username: str
    firstname: str
    lastname: str
    age: int
    slug: str

    class Config:
        orm_mode = True

# Схемы для задач
class CreateTask(BaseModel):
    title: str
    content: str
    priority: int


class UpdateTask(BaseModel):
    title: str
    content: str
    priority: int
