from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.backend.db import Base  # Импортируем базовый класс Base
from app.models.task import Task

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    slug = Column(String, unique=True, index=True)

    tasks = relationship("Task", back_populates="user")

# from sqlalchemy.schema import CreateTable
# print(CreateTable(User.__table__))