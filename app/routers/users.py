from fastapi import APIRouter

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

@router.get("/")
def all_users():
    pass  # Реализация будет позже

@router.get("/{user_id}")
def user_by_id(user_id: int):
    pass  # Реализация будет позже

@router.post("/create")
def create_user():
    pass  # Реализация будет позже

@router.put("/update")
def update_user():
    pass  # Реализация будет позже

@router.delete("/delete")
def delete_user():
    pass  # Реализация будет позже
