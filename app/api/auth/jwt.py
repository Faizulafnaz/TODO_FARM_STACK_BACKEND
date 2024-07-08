from typing import Any
from datetime import datetime
from fastapi import APIRouter, Depends, status, Body, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.services.user_service import UserService
from app.core.security import create_access_token, create_refresh_token
from app.schemas.auth_schema import TokenSchema
from app.api.dependencies.user_dependencies import get_current_user
from app.models.user_model import User
from fastapi.security import OAuth2PasswordBearer
from app.core.configure import settings
from pydantic import ValidationError
from app.schemas.auth_schema import TokenPayload
from jose import jwt

auth_router = APIRouter()

@auth_router.post('/login', summary='Create access and refresh tokens for user', response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    user = await UserService.authenticate(username = form_data.username, password = form_data.password)
    return {
        'access_token':create_access_token(user.user_id),
        'refresh_token':create_refresh_token(user.user_id)
    }

@auth_router.post('/test-token', summary='Test if the access token is valid')
async def test_token(user : User =  Depends(get_current_user)):
    return user

@auth_router.post('/refresh', summary='Refresh token', response_model=TokenSchema)
async def refresh_token(refresh_token : str = Body(...)):
    try:
        payload = jwt.decode(
            refresh_token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail = 'Token expired'
            )

    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Could not validate credentials'
        )
    
    user = await UserService.get_user_by_id(token_data.sub)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Could not found user'
        )
    
    return {
        'access_token':create_access_token(user.user_id),
        'refresh_token':create_refresh_token(user.user_id)
    }

