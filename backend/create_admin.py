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
from datetime import datetime, timezone


def create_user_profile():
    """Cria um perfil de usuário no banco"""
    print("=" * 50)
    print("🔐 CRIAR PERFIL DE USUÁRIO")
    print("=" * 50)
    print()

    print("Qual tipo de conta deseja criar?")
    print("1. Admin (acesso total)")
    print("2. Free (usuário gratuito)")
    print("3. Premium (usuário pago)")
    role_choice = input("Escolha (1-3, padrão=1): ").strip() or "1"
    
    role_map = {
        "1": "admin",
        "2": "free",
        "3": "premium"
    }
    role = role_map.get(role_choice, "admin")
    is_premium = role in ["admin", "premium"]

    print(f"\nCriando conta do tipo: {role.upper()}\n")
    
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
    print("1. Console (PlayStation/Xbox)")
    print("2. PC")
    print("3. Mobile")
    platform_choice = input("Escolha (1-3, Enter para pular): ").strip()
    
    platform_map = {
        "1": "console",
        "2": "pc", 
        "3": "mobile"
    }
    platform = platform_map.get(platform_choice)
    
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
    
    auth_user = None
    
    try:
        try:
            # Tentar criar usuário
            auth_response = supabase_service.client.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": {
                        "full_name": full_name,
                        "nickname": nickname,
                        "platform": platform
                    }
                }
            })
            auth_user = auth_response.user
        except Exception as e:
            if "already registered" in str(e) or "already exists" in str(e):
                print("⚠️  Usuário já existe no Auth. Tentando login para recuperar ID...")
                try:
                    auth_response = supabase_service.client.auth.sign_in_with_password({
                        "email": email,
                        "password": password
                    })
                    auth_user = auth_response.user
                    print("✅ Login realizado com sucesso! Prosseguindo com criação do perfil...")
                except Exception as login_error:
                    print(f"❌ Falha ao logar com o usuário existente: {login_error}")
                    print("   Certifique-se de usar a senha correta se o usuário já existe.")
                    return
            else:
                raise e
        
        if not auth_user:
            print("❌ Erro ao criar ou autenticar usuário no Auth!")
            return
        
        user_id = str(auth_user.id)
        print(f"✅ ID do Usuário: {user_id}")
        
        # Criar perfil na tabela users
        print("⏳ Criando/Atualizando perfil na tabela users...")
        
        user_data = {
            "id": user_id,
            "email": email,
            "name": full_name,
            "nickname": nickname,
            "platform": platform,
            "role": role,
            "is_premium": is_premium,
            "daily_questions_used": 0,
            "last_reset": datetime.now(timezone.utc).isoformat(),
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        
        # Tentar inserir no banco
        try:
            result = supabase_service.client.table("users").insert(user_data).execute()
            print("✅ Perfil criado com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao inserir na tabela users: {e}")
            print("⚠️  Se o erro for falta de colunas, o banco de dados precisa ser atualizado.")
            return
            
            # Criar estatísticas iniciais
            print("⏳ Criando estatísticas iniciais...")
            stats_data = {
                "user_id": user_id,
                "total_questions": 0,
                "builds_consulted": 0,
                "gameplay_questions": 0,
                "last_active": datetime.now(timezone.utc).isoformat()
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
        create_user_profile()
    except KeyboardInterrupt:
        print("\n\n❌ Operação cancelada pelo usuário!")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {str(e)}")
