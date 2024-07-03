from typing import Any
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.services.user_service import UserService
from app.core.security import create_access_token, create_refresh_token
from app.schemas.auth_schema import TokenSchema

auth_router = APIRouter()

@auth_router.post('/login', summary='Create access and refresh tokens for user', response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    user = await UserService.authenticate(username = form_data.username, password = form_data.password)
    return {
        'access_token':create_access_token(user.user_id),
        'refresh_token':create_refresh_token(user.user_id)
    }