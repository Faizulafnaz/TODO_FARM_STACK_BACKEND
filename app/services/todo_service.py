from typing import List
from app.models.user_model import User
from app.models.todo_model import Todo
from app.schemas.todo_schema import *


class TodoService:
    @staticmethod
    async def list_todos(user: User) -> List[Todo]:
        todo = await Todo.find_many(Todo.owner.id == user.id).to_list()
        return todo
    
    @staticmethod
    async def create_todo(user: User, data: TodoCreate) -> Todo:
        todo = Todo(**data.dict(), owner=user)
        return await todo.insert()
    
    @staticmethod
    async def retieve_todo(todo_id : UUID, user : User):
        todo = await Todo.find_one(Todo.todo_id == todo_id, Todo.owner.id == user.id)
        return todo
    
    @staticmethod
    async def update_todo(todo_id : UUID, user : User, data):
        todo = await TodoService.retieve_todo(todo_id=todo_id, user=user)
        await todo.update({"$set" : data.dict(exclude_unset=True)})
        await todo.save()
    
    @staticmethod
    async def delete_todo(todo_id : UUID, user : User):
        todo = await TodoService.retieve_todo(todo_id=todo_id, user=user)
        if todo:
            await todo.delete()
        return None

