from supabase import create_client, Client
from datetime import datetime, timedelta
from app.core.config import settings
from app.core.security import get_password_hash, verify_password
from typing import Optional, Dict


class SupabaseService:
    def __init__(self):
        self.client: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    
    async def create_user(self, email: str, password: str, full_name: Optional[str] = None) -> Dict:
        """Cria um novo usuário"""
        # Criar no Supabase Auth
        auth_response = self.client.auth.sign_up({
            "email": email,
            "password": password
        })
        
        if auth_response.user:
            # Criar perfil adicional na tabela users
            user_data = {
                "id": auth_response.user.id,
                "email": email,
                "full_name": full_name,
                "is_premium": False,
                "daily_questions_used": 0,
                "last_reset": datetime.utcnow().isoformat()
            }
            
            self.client.table("users").insert(user_data).execute()
            return user_data
        
        raise Exception("Erro ao criar usuário")
    
    async def authenticate_user(self, email: str, password: str) -> Optional[Dict]:
        """Autentica usuário"""
        auth_response = self.client.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        
        if auth_response.user:
            # Buscar dados completos do usuário
            user_response = self.client.table("users").select("*").eq("id", auth_response.user.id).execute()
            if user_response.data:
                return user_response.data[0]
        
        return None
    
    async def get_user(self, user_id: str) -> Optional[Dict]:
        """Busca usuário por ID"""
        response = self.client.table("users").select("*").eq("id", user_id).execute()
        return response.data[0] if response.data else None
    
    async def check_and_increment_quota(self, user_id: str) -> bool:
        """Verifica e incrementa quota de perguntas"""
        user = await self.get_user(user_id)
        if not user:
            return False
        
        # Reset diário
        last_reset = datetime.fromisoformat(user["last_reset"])
        if datetime.utcnow() - last_reset > timedelta(days=1):
            self.client.table("users").update({
                "daily_questions_used": 0,
                "last_reset": datetime.utcnow().isoformat()
            }).eq("id", user_id).execute()
            user["daily_questions_used"] = 0
        
        # Verificar limite
        limit = settings.PREMIUM_TIER_DAILY_LIMIT if user["is_premium"] else settings.FREE_TIER_DAILY_LIMIT
        
        if user["daily_questions_used"] >= limit:
            return False
        
        # Incrementar
        self.client.table("users").update({
            "daily_questions_used": user["daily_questions_used"] + 1
        }).eq("id", user_id).execute()
        
        return True
    
    async def get_quota_info(self, user_id: str) -> Dict:
        """Retorna informações de quota"""
        user = await self.get_user(user_id)
        if not user:
            raise Exception("Usuário não encontrado")
        
        # Reset diário se necessário
        last_reset = datetime.fromisoformat(user["last_reset"])
        if datetime.utcnow() - last_reset > timedelta(days=1):
            user["daily_questions_used"] = 0
            user["last_reset"] = datetime.utcnow().isoformat()
        
        limit = settings.PREMIUM_TIER_DAILY_LIMIT if user["is_premium"] else settings.FREE_TIER_DAILY_LIMIT
        
        return {
            "daily_limit": limit,
            "questions_used": user["daily_questions_used"],
            "questions_remaining": limit - user["daily_questions_used"],
            "is_premium": user["is_premium"],
            "reset_time": (datetime.fromisoformat(user["last_reset"]) + timedelta(days=1))
        }


supabase_service = SupabaseService()
