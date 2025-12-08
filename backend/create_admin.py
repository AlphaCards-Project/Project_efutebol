#!/usr/bin/env python3
"""
Script para criar perfil de administrador no Supabase
Uso: python create_admin.py
"""

import sys
import os
from getpass import getpass

# Adicionar o diretório do backend ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.supabase_service import supabase_service
from datetime import datetime


def create_admin_profile():
    """Cria um perfil de administrador no banco"""
    print("=" * 50)
    print("🔐 CRIAR PERFIL DE ADMINISTRADOR")
    print("=" * 50)
    print()
    
    # Coletar informações
    email = input("📧 Email: ").strip()
    if not email:
        print("❌ Email é obrigatório!")
        return
    
    password = getpass("🔑 Senha (mínimo 6 caracteres): ")
    if len(password) < 6:
        print("❌ Senha deve ter pelo menos 6 caracteres!")
        return
    
    password_confirm = getpass("🔑 Confirme a senha: ")
    if password != password_confirm:
        print("❌ As senhas não coincidem!")
        return
    
    full_name = input("👤 Nome completo (opcional): ").strip() or None
    nickname = input("🎮 Nickname (opcional): ").strip() or None
    
    print("\n🎯 Plataforma:")
    print("1. PlayStation")
    print("2. Xbox")
    print("3. PC")
    platform_choice = input("Escolha (1-3, Enter para pular): ").strip()
    
    platform_map = {
        "1": "PlayStation",
        "2": "Xbox", 
        "3": "PC"
    }
    platform = platform_map.get(platform_choice)
    
    print("\n👑 Tipo de conta:")
    print("1. Admin (acesso total)")
    print("2. Premium (usuário premium)")
    print("3. Free (usuário gratuito)")
    role_choice = input("Escolha (1-3, padrão=1): ").strip() or "1"
    
    role_map = {
        "1": "admin",
        "2": "premium",
        "3": "free"
    }
    role = role_map.get(role_choice, "admin")
    is_premium = role in ["admin", "premium"]
    
    print("\n" + "=" * 50)
    print("📋 RESUMO")
    print("=" * 50)
    print(f"Email: {email}")
    print(f"Nome: {full_name or 'Não informado'}")
    print(f"Nickname: {nickname or 'Não informado'}")
    print(f"Plataforma: {platform or 'Não informada'}")
    print(f"Tipo: {role.upper()}")
    print("=" * 50)
    
    confirm = input("\n✅ Confirmar criação? (s/N): ").strip().lower()
    if confirm != 's':
        print("❌ Operação cancelada!")
        return
    
    print("\n⏳ Criando usuário no Supabase Auth...")
    
    try:
        # Criar usuário no Supabase Auth
        auth_response = supabase_service.client.auth.sign_up({
            "email": email,
            "password": password
        })
        
        if not auth_response.user:
            print("❌ Erro ao criar usuário no Auth!")
            return
        
        user_id = str(auth_response.user.id)
        print(f"✅ Usuário criado no Auth! ID: {user_id}")
        
        # Criar perfil na tabela users
        print("⏳ Criando perfil na tabela users...")
        
        user_data = {
            "id": user_id,
            "email": email,
            "name": full_name,
            "nickname": nickname,
            "platform": platform,
            "role": role,
            "is_premium": is_premium,
            "daily_questions_used": 0,
            "last_reset": datetime.utcnow().isoformat(),
            "created_at": datetime.utcnow().isoformat()
        }
        
        result = supabase_service.client.table("users").insert(user_data).execute()
        
        if result.data:
            print("✅ Perfil criado com sucesso!")
            
            # Criar estatísticas iniciais
            print("⏳ Criando estatísticas iniciais...")
            stats_data = {
                "user_id": user_id,
                "total_questions": 0,
                "builds_consulted": 0,
                "gameplay_questions": 0,
                "last_active": datetime.utcnow().isoformat()
            }
            
            try:
                supabase_service.client.table("user_stats").insert(stats_data).execute()
                print("✅ Estatísticas criadas!")
            except Exception as e:
                print(f"⚠️  Não foi possível criar estatísticas: {e}")
                print("   (A tabela user_stats pode não existir)")
            
            print("\n" + "=" * 50)
            print("🎉 SUCESSO!")
            print("=" * 50)
            print(f"✉️  Email: {email}")
            print(f"🆔 ID: {user_id}")
            print(f"👑 Tipo: {role.upper()}")
            print(f"💎 Premium: {'Sim' if is_premium else 'Não'}")
            print()
            print("🔗 Você pode fazer login agora no sistema!")
            print("=" * 50)
            
        else:
            print("❌ Erro ao criar perfil!")
            
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        print("\n💡 Dicas:")
        print("  - Verifique se o arquivo .env está configurado")
        print("  - Verifique se as credenciais do Supabase estão corretas")
        print("  - Verifique se o email já não está cadastrado")


if __name__ == "__main__":
    try:
        create_admin_profile()
    except KeyboardInterrupt:
        print("\n\n❌ Operação cancelada pelo usuário!")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {str(e)}")
