#!/usr/bin/env python3
"""
Script rápido para criar admin via linha de comando
Uso: python quick_admin.py email@example.com senha123 [nome] [nickname]
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.supabase_service import supabase_service
from datetime import datetime


def quick_create_admin(email, password, name=None, nickname=None):
    """Cria admin rapidamente via linha de comando"""
    try:
        print(f"⏳ Criando admin: {email}")
        
        # Criar usuário no Supabase Auth
        auth_response = supabase_service.client.auth.sign_up({
            "email": email,
            "password": password
        })
        
        if not auth_response.user:
            print("❌ Erro ao criar usuário!")
            return False
        
        user_id = str(auth_response.user.id)
        
        # Criar perfil admin
        user_data = {
            "id": user_id,
            "email": email,
            "name": name,
            "nickname": nickname,
            "role": "admin",
            "is_premium": True,
            "daily_questions_used": 0,
            "last_reset": datetime.utcnow().isoformat(),
            "created_at": datetime.utcnow().isoformat()
        }
        
        supabase_service.client.table("users").insert(user_data).execute()
        
        # Criar stats
        try:
            stats_data = {
                "user_id": user_id,
                "total_questions": 0,
                "builds_consulted": 0,
                "gameplay_questions": 0,
                "last_active": datetime.utcnow().isoformat()
            }
            supabase_service.client.table("user_stats").insert(stats_data).execute()
        except:
            pass  # Ignorar se tabela não existe
        
        print(f"✅ Admin criado com sucesso!")
        print(f"   Email: {email}")
        print(f"   ID: {user_id}")
        print(f"   Tipo: ADMIN")
        return True
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("❌ Uso: python quick_admin.py EMAIL SENHA [NOME] [NICKNAME]")
        print("\n📖 Exemplos:")
        print("  python quick_admin.py admin@test.com senha123")
        print("  python quick_admin.py admin@test.com senha123 'João Silva'")
        print("  python quick_admin.py admin@test.com senha123 'João Silva' joao_pro")
        sys.exit(1)
    
    email = sys.argv[1]
    password = sys.argv[2]
    name = sys.argv[3] if len(sys.argv) > 3 else None
    nickname = sys.argv[4] if len(sys.argv) > 4 else None
    
    if len(password) < 6:
        print("❌ Senha deve ter pelo menos 6 caracteres!")
        sys.exit(1)
    
    success = quick_create_admin(email, password, name, nickname)
    sys.exit(0 if success else 1)
