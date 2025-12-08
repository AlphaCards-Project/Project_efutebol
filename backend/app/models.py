from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, JSON, Text, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class UserPlatform(str, enum.Enum):
    console = "console"
    pc = "pc"
    mobile = "mobile"

class UserRole(str, enum.Enum):
    admin = "admin"
    premium = "premium"
    free = "free"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    nickname = Column(String, unique=True, nullable=True)
    platform = Column(Enum(UserPlatform), nullable=True)
    role = Column(Enum(UserRole), default=UserRole.free, nullable=False)
    is_premium = Column(Boolean, default=False)
    daily_questions_used = Column(Integer, default=0)
    last_reset = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    builds = relationship("Build", back_populates="user")
    gameplay_tips = relationship("GameplayTip", back_populates="creator")

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    konami_player_id = Column(Integer, unique=True, index=True)
    real_position = Column(String, nullable=True)
    nationality = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    cards = relationship("Card", back_populates="player")

class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"))
    konami_id = Column(Integer, unique=True, index=True)
    name = Column(String, nullable=False)
    version = Column(String, nullable=True)
    card_type = Column(String, nullable=True)
    position = Column(String, nullable=True)
    overall_rating = Column(Integer, nullable=True)
    stats_base = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    player = relationship("Player", back_populates="cards")
    builds = relationship("Build", back_populates="card")

class Build(Base):
    __tablename__ = "builds"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    card_id = Column(Integer, ForeignKey("cards.id"), nullable=False)
    title = Column(String, nullable=False)
    shooting = Column(Integer, default=0)
    passing = Column(Integer, default=0)
    dribbling = Column(Integer, default=0)
    dexterity = Column(Integer, default=0)
    lower_body_strength = Column(Integer, default=0)
    aerial_strength = Column(Integer, default=0)
    defending = Column(Integer, default=0)
    gk_1 = Column(Integer, default=0)
    gk_2 = Column(Integer, default=0)
    gk_3 = Column(Integer, default=0)
    overall_rating = Column(Integer, nullable=True)
    is_official_meta = Column(Boolean, default=False)
    meta_content = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="builds")
    card = relationship("Card", back_populates="builds")

class GameplayTip(Base):
    __tablename__ = "gameplay_tips"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, nullable=False, index=True)
    title = Column(String, nullable=False)
    pain_description = Column(Text, nullable=True)
    solution = Column(Text, nullable=False)
    created_by_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    creator = relationship("User", back_populates="gameplay_tips")

class AICache(Base):
    __tablename__ = "ai_cache"

    id = Column(Integer, primary_key=True, index=True)
    prompt_hash = Column(String(64), unique=True, nullable=False, index=True)
    response_text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)
