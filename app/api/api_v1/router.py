from fastapi import APIRouter
from .handler import user, todo
from app.api.auth.jwt import auth_router

router = APIRouter()

router.include_router(user.user_router, prefix='/users', tags=['users'])
router.include_router(auth_router, prefix='/auth', tags=['auth'])
router.include_router(todo.todo_router, prefix='/todo', tags=['todo'])
