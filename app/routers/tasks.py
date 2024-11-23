from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
from app.models.task import Task
from app.models.user import User
from app.backend.db_depends import get_db
from app.schemas import CreateTask, UpdateTask
from slugify import slugify


router = APIRouter(
    prefix="/task",
    tags=["task"]
)


# Получить все задачи
@router.get("/")
def all_tasks(db: Session = Depends(get_db)):
    """Возвращает список всех задач."""
    tasks = db.execute(select(Task)).scalars().all()
    return tasks

# Получить задачу по ID
@router.get("/{task_id}")
def task_by_id(task_id: int, db: Session = Depends(get_db)):
    """Возвращает задачу по ID."""
    task = db.execute(select(Task).filter(Task.id == task_id)).scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task was not found")
    return task

# Создать задачу
@router.post("/create")
def create_task(task: CreateTask, user_id: int, db: Session = Depends(get_db)):
    """Создаёт новую задачу для пользователя."""
    user = db.execute(select(User).filter(User.id == user_id)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")

    # Генерация slug на основе названия задачи (title)
    task_slug = slugify(task.title)
    new_task = Task(
        title=task.title,
        content=task.content,
        slug=task_slug,  # Добавляем слаг
        user_id=user_id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {"status_code": status.HTTP_201_CREATED, "transaction": "Successful"}

# Обновить задачу
@router.put("/update/{task_id}")
def update_task(task_id: int, task: UpdateTask, db: Session = Depends(get_db)):
    """Обновить задачу."""
    stmt = update(Task).where(Task.id == task_id).values(
        title=task.title,
        description=task.description
    )
    result = db.execute(stmt)
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task was not found")
    return {"status_code": status.HTTP_200_OK, "transaction": "Task update is successful!"}

# Удалить задачу
@router.delete("/delete/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Удалить задачу по ID."""
    stmt = delete(Task).where(Task.id == task_id)
    result = db.execute(stmt)
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task was not found")
    return {"status_code": status.HTTP_200_OK, "transaction": "Task deleted successfully"}
