from fastapi import APIRouter

router = APIRouter(
    prefix="/task",
    tags=["task"]
)


@router.get("/")
def all_tasks():
    pass  # Реализация будет позже

@router.get("/{task_id}")
def task_by_id(task_id: int):
    pass  # Реализация будет позже

@router.post("/create")
def create_task():
    pass  # Реализация будет позже

@router.put("/update")
def update_task():
    pass  # Реализация будет позже

@router.delete("/delete")
def delete_task():
    pass  # Реализация будет позже
