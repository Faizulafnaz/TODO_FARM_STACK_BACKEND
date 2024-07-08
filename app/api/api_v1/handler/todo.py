from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends
from app.schemas.todo_schema import TodoOut, TodoCreate, TodoUpdate
from app.models.user_model import User
from app.api.dependencies.user_dependencies import get_current_user
from app.services.todo_service import TodoService
from app.models.todo_model import Todo

todo_router = APIRouter()

@todo_router.get('/', summary="Get all the todos of the user", response_model=List[TodoOut])
async def list(current_user: User = Depends(get_current_user)):
    return await TodoService.list_todos(user=current_user)

@todo_router.post('/create', summary='Create Todo', response_model=TodoOut)
async def create(todo : TodoCreate, current_user: User = Depends(get_current_user)):
    return await TodoService.create_todo(user=current_user, data=todo)

@todo_router.get('/{todo_id}', summary="Get a todo by todo_id", response_model=TodoOut)
async def retrieve(todo_id : UUID, current_user: User = Depends(get_current_user)):
    return await TodoService.retieve_todo(user=current_user, todo_id=todo_id)

@todo_router.put('/{todo_id}', summary="Update todo by id", response_model=TodoOut)
async def update(data : TodoUpdate, todo_id : UUID, current_user: User = Depends(get_current_user)):
    return await TodoService.update_todo(todo_id=todo_id, data=data, user=current_user)

@todo_router.delete('/{todo_id}', summary="Delete todo by id")
async def delete(todo_id : UUID, current_user: User = Depends(get_current_user)):
    await TodoService.delete_todo(todo_id=todo_id, user=current_user)
    return None