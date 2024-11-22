from fastapi import FastAPI
from .routers import tasks, users

app = FastAPI()

# Подключаем маршруты
app.include_router(tasks.router)
app.include_router(users.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Taskmanager"}
