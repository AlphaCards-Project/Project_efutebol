from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict
from datetime import datetime


# User Schemas
class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, description="Senha com no mínimo 6 caracteres")
    full_name: Optional[str] = Field(None, max_length=100, description="Nome completo do usuário")
    nickname: Optional[str] = Field(None, max_length=50, description="Apelido/gamertag do usuário")
    platform: Optional[str] = Field(None, description="Plataforma: console, pc ou mobile")
    
    class Config:
        schema_extra = {
            "example": {
                "email": "usuario@exemplo.com",
                "password": "senha123",
                "full_name": "João Silva",
                "nickname": "joaogamer",
                "platform": "console"
            }
        }


class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
    class Config:
        schema_extra = {
            "example": {
                "email": "usuario@exemplo.com",
                "password": "senha123"
            }
        }


class UserResponse(BaseModel):
    id: str
    email: str
    name: Optional[str] = None
    nickname: Optional[str] = None
    platform: Optional[str] = None
    role: str = "free"
    is_premium: bool = False
    daily_questions_used: int = 0
    created_at: datetime
    
    class Config:
        schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "usuario@exemplo.com",
                "name": "João Silva",
                "nickname": "joaogamer",
                "platform": "console",
                "role": "free",
                "is_premium": False,
                "daily_questions_used": 0,
                "created_at": "2024-01-01T00:00:00"
            }
        }


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
    
    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "user": {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "email": "usuario@exemplo.com",
                    "name": "João Silva",
                    "is_premium": False,
                    "daily_questions_used": 0,
                    "created_at": "2024-01-01T00:00:00"
                }
            }
        }


# Build Query Schemas
class BuildQuery(BaseModel):
    player_name: str = Field(..., min_length=2, max_length=100)
    position: str = Field(..., min_length=2, max_length=10)


class SkillPoints(BaseModel):
    skill: str
    points: int


class BuildResponse(BaseModel):
    player_name: str
    position: str
    priority_points: List[SkillPoints]
    playstyle: Optional[str]
    tips: str
    from_cache: bool = False


# Gameplay Query Schemas
class GameplayQuery(BaseModel):
    question: str = Field(..., min_length=5, max_length=500)


class GameplayResponse(BaseModel):
    question: str
    answer: str
    category: Optional[str]
    video_url: Optional[str]
    from_cache: bool = False


# Quota Schemas
class QuotaResponse(BaseModel):
    daily_limit: int
    questions_used: int
    questions_remaining: int
    is_premium: bool
    reset_time: datetime


# Generic Response
class MessageResponse(BaseModel):
    message: str
    detail: Optional[str] = None
