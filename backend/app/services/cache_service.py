import redis
import json
from typing import Optional
from app.core.config import settings


class CacheService:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=True
        )
    
    def get(self, key: str) -> Optional[dict]:
        """Busca valor no cache"""
        try:
            data = self.redis_client.get(key)
            return json.loads(data) if data else None
        except Exception as e:
            print(f"Cache get error: {e}")
            return None
    
    def set(self, key: str, value: dict, expire: int = 3600) -> bool:
        """Salva valor no cache com expiração (padrão 1 hora)"""
        try:
            self.redis_client.setex(key, expire, json.dumps(value))
            return True
        except Exception as e:
            print(f"Cache set error: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """Remove valor do cache"""
        try:
            self.redis_client.delete(key)
            return True
        except Exception as e:
            print(f"Cache delete error: {e}")
            return False
    
    def generate_build_key(self, player_name: str, position: str) -> str:
        """Gera chave de cache para build"""
        return f"build:{player_name.lower().strip()}:{position.upper()}"
    
    def generate_gameplay_key(self, question: str) -> str:
        """Gera chave de cache para gameplay (primeiros 100 chars)"""
        clean_question = question.lower().strip()[:100]
        return f"gameplay:{hash(clean_question)}"


cache_service = CacheService()
