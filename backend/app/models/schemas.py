from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict
from datetime import datetime


# User Schemas
class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: str
    email: str
    full_name: Optional[str]
    is_premium: bool = False
    daily_questions_used: int = 0
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


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
