from beanie import Document, Indexed, Link, before_event, Replace, Insert
from uuid import UUID, uuid4
from pydantic import Field, EmailStr
from datetime import datetime
from typing import Optional
from .user_model import User



class Todo(Document):
    todo_id : UUID = Field(default_factory=uuid4, unique = True)
    status : bool = False
    title : Indexed(str) # type: ignore
    description : str
    created_at : datetime = Field(default_factory=datetime.utcnow)
    updated_at : datetime = Field(default_factory=datetime.utcnow)
    owner : Link[User]

    def __repr__(self) -> str:
        return f"<User {self.title}>"
    
    def __str__(self) -> str:
        return self.title
    
    def __eq__(self, value: object) -> bool:
        if isinstance(value, Todo):
            return self.todo_id == value.todo_id
        return False
    
    def __hash__(self) -> int:
        return hash(self.title)
    
    @before_event([Replace, Insert])
    def update_updated_at(self):
        self.updated_at = datetime.utcnow()

    


