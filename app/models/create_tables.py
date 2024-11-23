from sqlalchemy import create_engine
from sqlalchemy.schema import CreateTable
from app.models.user import User
from app.models.task import Task
from app.backend.db import Base

# Создаём SQLite-базу (или используйте другую)
engine = create_engine('sqlite:///test.db', echo=True)

# Генерация схемы (физическое создание таблиц в базе данных)
Base.metadata.create_all(engine)

# Печатаем SQL-запросы для создания таблиц
print(str(CreateTable(User.__table__)))
print(str(CreateTable(Task.__table__)))
