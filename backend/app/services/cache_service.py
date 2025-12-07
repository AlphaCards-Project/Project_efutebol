import json
from typing import Optional, Dict
from datetime import datetime, timedelta
from app.core.config import settings

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False


class CacheService:
    def __init__(self):
        self.memory_cache: Dict[str, tuple] = {}  # (value, expire_time)
        self.redis_client = None
        
        if REDIS_AVAILABLE:
            try:
                self.redis_client = redis.Redis(
                    host=settings.REDIS_HOST,
                    port=settings.REDIS_PORT,
                    db=settings.REDIS_DB,
                    decode_responses=True,
                    socket_connect_timeout=2
                )
                self.redis_client.ping()
                print("✅ Redis conectado")
            except Exception as e:
                print(f"⚠️  Redis não disponível, usando cache em memória: {e}")
                self.redis_client = None
    
    def get(self, key: str) -> Optional[dict]:
        """Busca valor no cache (Redis ou memória)"""
        # Tentar Redis primeiro
        if self.redis_client:
            try:
                data = self.redis_client.get(key)
                return json.loads(data) if data else None
            except Exception:
                pass
        
        # Fallback para memória
        if key in self.memory_cache:
            value, expire_time = self.memory_cache[key]
            if datetime.now() < expire_time:
                return value
            else:
                del self.memory_cache[key]
        
        return None
    
    def set(self, key: str, value: dict, expire: int = 3600) -> bool:
        """Salva valor no cache (Redis ou memória)"""
        # Tentar Redis primeiro
        if self.redis_client:
            try:
                self.redis_client.setex(key, expire, json.dumps(value))
                return True
            except Exception:
                pass
        
        # Fallback para memória
        expire_time = datetime.now() + timedelta(seconds=expire)
        self.memory_cache[key] = (value, expire_time)
        
        # Limpar cache antigo (máximo 1000 itens)
        if len(self.memory_cache) > 1000:
            now = datetime.now()
            self.memory_cache = {
                k: v for k, v in self.memory_cache.items()
                if v[1] > now
            }
        
        return True
    
    def delete(self, key: str) -> bool:
        """Remove valor do cache"""
        if self.redis_client:
            try:
                self.redis_client.delete(key)
            except Exception:
                pass
        
        if key in self.memory_cache:
            del self.memory_cache[key]
        
        return True
    
    def generate_build_key(self, player_name: str, position: str) -> str:
        """Gera chave de cache para build"""
        return f"build:{player_name.lower().strip()}:{position.upper()}"
    
    def generate_gameplay_key(self, question: str) -> str:
        """Gera chave de cache para gameplay (primeiros 100 chars)"""
        clean_question = question.lower().strip()[:100]
        return f"gameplay:{hash(clean_question)}"


cache_service = CacheService()
