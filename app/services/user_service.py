from typing import Optional
from uuid import UUID
from fastapi import HTTPException, status
from app.schemas.user_schema import UserAuth
from app.models.user_model import User
from app.core.security import get_password, varify_password

class UserService:
    @staticmethod
    async def create_user(user : UserAuth):

        existing_user = await User.by_email(user.email)

        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email is already exist')
        
        existing_user = await User.find_one(User.username == user.username)

        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User name is already exist')
        
        user_in = User(
            username = user.username,
            email = user.email,
            hashed_password=get_password(user.password)
        )
        await user_in.save()
        return user_in
    
    @staticmethod
    async def authenticate(username: str, password: str) -> Optional[User]:
        user = await UserService.get_user_by_username(username)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found with this username')
        if not varify_password(password, user.hashed_password):
            return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect password')
        return user
    
    @staticmethod
    async def get_user_by_username(username: str) -> Optional[User]:
        return await User.find_one(User.username == username)
    
    @staticmethod
    async def get_user_by_id(user_id: UUID) -> Optional[User]:
        return await User.find_one(User.user_id == user_id)
    