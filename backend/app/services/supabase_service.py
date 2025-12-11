from supabase import create_client, Client
from datetime import datetime, timezone, timedelta
from app.core.config import settings
from app.core.security import get_password_hash, verify_password
from typing import Optional, Dict


class SupabaseService:
    def __init__(self):
        self.client: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    
    async def create_user(
        self, 
        email: str, 
        password: str, 
        full_name: Optional[str] = None, 
        platform: Optional[str] = None
    ) -> Dict:
        """Cria um novo usuário"""
        try:
            # Criar no Supabase Auth com metadata
            auth_response = self.client.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": {
                        "full_name": full_name,
                        "platform": platform
                    }
                }
            })
            
            if auth_response.user:
                # Criar perfil adicional na tabela users (UUID sincronizado)
                user_data = {
                    "id": str(auth_response.user.id),
                    "email": email,
                    "name": full_name,
                    "platform": platform,
                    "role": "free",
                    "daily_questions_used": 0,
                    "last_reset": datetime.now(timezone.utc).isoformat(),
                    "created_at": datetime.now(timezone.utc).isoformat()
                }
                
                try:
                    self.client.table("users").insert(user_data).execute()
                except Exception as e:
                    error_msg = str(e).lower()
                    if "could not find the 'platform' column" in error_msg:
                        print("⚠️  Coluna 'platform' não encontrada. Tentando inserir sem ela...")
                        user_data.pop("platform", None)
                        self.client.table("users").insert(user_data).execute()
                    else:
                        raise e
                
                return {
                    "id": str(auth_response.user.id),
                    "email": email,
                    "name": full_name,
                    "platform": platform,
                    "role": "free",
                    "daily_questions_used": 0,
                    "created_at": user_data["created_at"]
                }
            
            raise Exception("Erro ao criar usuário no Supabase Auth")
        except Exception as e:
            print(f"❌ Erro ao criar usuário: {e}")
            raise Exception(f"Erro ao registrar: {str(e)}")
    
    async def authenticate_user(self, email: str, password: str) -> Optional[Dict]:
        """Autentica usuário"""
        try:
            auth_response = self.client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if auth_response.user:
                user_id = str(auth_response.user.id)
                
                # Tentar buscar role da tabela users
                try:
                    user_data = self.client.table("users").select("role, platform, name").eq("id", user_id).execute()
                    if user_data.data and len(user_data.data) > 0:
                        user_record = user_data.data[0]
                        return {
                            "id": user_id,
                            "email": auth_response.user.email or email,
                            "name": user_record.get("name") or auth_response.user.user_metadata.get("full_name") if auth_response.user.user_metadata else None,
                            "platform": user_record.get("platform"),
                            "role": user_record.get("role", "free"),
                            "daily_questions_used": 0,
                            "created_at": str(auth_response.user.created_at) if auth_response.user.created_at else str(datetime.now(timezone.utc))
                        }
                except Exception as e:
                    print(f"⚠️ Não foi possível buscar role da tabela users: {e}")
                
                # Fallback se não conseguir buscar da tabela users
                return {
                    "id": user_id,
                    "email": auth_response.user.email or email,
                    "name": auth_response.user.user_metadata.get("full_name") if auth_response.user.user_metadata else None,
                    "platform": None,
                    "role": "free",
                    "daily_questions_used": 0,
                    "created_at": str(auth_response.user.created_at) if auth_response.user.created_at else str(datetime.now(timezone.utc))
                }
            
            return None
        except Exception as e:
            print(f"❌ Erro ao autenticar: {e}")
            # Retornar None em vez de exception para melhor UX
            return None
    
    async def get_user(self, user_id: str) -> Optional[Dict]:
        """Busca usuário por ID"""
        response = self.client.table("users").select("*").eq("id", user_id).execute()
        return response.data[0] if response.data else None
    
    async def check_and_increment_quota(self, user_id: str) -> bool:
        """
        Verifica e incrementa quota de perguntas
        Como a tabela users pode não existir, sempre retorna True (sem limite)
        TODO: Implementar sistema de quota com Redis ou outra tabela
        """
        # Temporariamente sem limite até configurar tabela users corretamente
        return True
    
    async def get_quota_info(self, user_id: str) -> Dict:
        """
        Retorna informações de quota
        Como a tabela users pode não existir, retorna quota ilimitada
        """
        # Retornar dados padrão sem depender da tabela users
        return {
            "daily_limit": settings.FREE_TIER_DAILY_LIMIT,
            "questions_used": 0,
            "questions_remaining": settings.FREE_TIER_DAILY_LIMIT,
            "role": "free",
            "reset_time": (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()
        }


supabase_service = SupabaseService()
