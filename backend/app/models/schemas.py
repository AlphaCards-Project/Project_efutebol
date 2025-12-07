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


# Build Create Schemas (para adicionar builds pelo frontend)
class BuildCreate(BaseModel):
    card_id: int = Field(..., description="ID da carta do jogador")
    title: str = Field(..., min_length=3, max_length=100, description="Título da build (ex: 'Meta CF', 'False 9')")
    shooting: int = Field(0, ge=0, le=99, description="Pontos em Shooting (0-99)")
    passing: int = Field(0, ge=0, le=99, description="Pontos em Passing (0-99)")
    dribbling: int = Field(0, ge=0, le=99, description="Pontos em Dribbling (0-99)")
    dexterity: int = Field(0, ge=0, le=99, description="Pontos em Dexterity (0-99)")
    lower_body_strength: int = Field(0, ge=0, le=99, description="Pontos em Lower Body Strength (0-99)")
    aerial_strength: int = Field(0, ge=0, le=99, description="Pontos em Aerial Strength (0-99)")
    defending: int = Field(0, ge=0, le=99, description="Pontos em Defending (0-99)")
    gk_1: int = Field(0, ge=0, le=99, description="Pontos em GK Ability 1 (0-99)")
    gk_2: int = Field(0, ge=0, le=99, description="Pontos em GK Ability 2 (0-99)")
    gk_3: int = Field(0, ge=0, le=99, description="Pontos em GK Ability 3 (0-99)")
    overall_rating: Optional[int] = Field(None, description="Overall final da build")
    is_official_meta: bool = Field(False, description="Se é uma build oficial/meta")
    meta_content: Optional[Dict] = Field(None, description="Conteúdo adicional (dicas, playstyle, etc)")
    
    class Config:
        schema_extra = {
            "example": {
                "card_id": 1,
                "title": "Meta CF - Goal Poacher",
                "shooting": 15,
                "passing": 5,
                "dribbling": 10,
                "dexterity": 8,
                "lower_body_strength": 12,
                "aerial_strength": 8,
                "defending": 0,
                "gk_1": 0,
                "gk_2": 0,
                "gk_3": 0,
                "overall_rating": 98,
                "is_official_meta": True,
                "meta_content": {
                    "playstyle": "Goal Poacher",
                    "dicas": "Fique na área. Finalize rápido.",
                    "posicao_ideal": "CF"
                }
            }
        }


class BuildUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    shooting: Optional[int] = Field(None, ge=0, le=99)
    passing: Optional[int] = Field(None, ge=0, le=99)
    dribbling: Optional[int] = Field(None, ge=0, le=99)
    dexterity: Optional[int] = Field(None, ge=0, le=99)
    lower_body_strength: Optional[int] = Field(None, ge=0, le=99)
    aerial_strength: Optional[int] = Field(None, ge=0, le=99)
    defending: Optional[int] = Field(None, ge=0, le=99)
    gk_1: Optional[int] = Field(None, ge=0, le=99)
    gk_2: Optional[int] = Field(None, ge=0, le=99)
    gk_3: Optional[int] = Field(None, ge=0, le=99)
    overall_rating: Optional[int] = None
    is_official_meta: Optional[bool] = None
    meta_content: Optional[Dict] = None


class BuildResponseDB(BaseModel):
    id: int
    user_id: str
    card_id: int
    title: str
    shooting: int
    passing: int
    dribbling: int
    dexterity: int
    lower_body_strength: int
    aerial_strength: int
    defending: int
    gk_1: int
    gk_2: int
    gk_3: int
    overall_rating: Optional[int]
    is_official_meta: bool
    meta_content: Optional[Dict]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "card_id": 1,
                "title": "Meta CF - Goal Poacher",
                "shooting": 15,
                "passing": 5,
                "dribbling": 10,
                "dexterity": 8,
                "lower_body_strength": 12,
                "aerial_strength": 8,
                "defending": 0,
                "gk_1": 0,
                "gk_2": 0,
                "gk_3": 0,
                "overall_rating": 98,
                "is_official_meta": True,
                "meta_content": {
                    "playstyle": "Goal Poacher",
                    "dicas": "Fique na área"
                },
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-01T00:00:00"
            }
        }
