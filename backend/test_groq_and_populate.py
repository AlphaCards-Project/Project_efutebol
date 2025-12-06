#!/usr/bin/env python3
"""
Teste de conexão com Groq API e população do banco de dados
"""

import os
from groq import Groq
from supabase import create_client, Client
from dotenv import load_dotenv
import uuid

load_dotenv()

print("="*70)
print("🧪 TESTE DE API GROQ E POPULAÇÃO DO BANCO")
print("="*70)
print()

# =============================================================================
# 1. TESTE DA API GROQ
# =============================================================================
print("1️⃣  TESTANDO API GROQ...")
print("-" * 70)

try:
    groq_key = os.getenv("GROQ_API_KEY") or os.getenv("groq_API_KEY")
    if not groq_key:
        print("❌ GROQ_API_KEY não encontrado no .env")
        exit(1)
    
    client = Groq(api_key=groq_key)
    
    # Teste simples
    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Responda em português: O que é eFootball em uma frase?"
            }
        ],
        model="llama-3.1-8b-instant",
        temperature=0.5,
        max_tokens=100
    )
    
    resposta = response.choices[0].message.content
    
    print("✅ Conexão com Groq OK!")
    print(f"📝 Resposta da IA: {resposta}")
    print()
    
except Exception as e:
    print(f"❌ Erro ao conectar com Groq: {e}")
    exit(1)

# =============================================================================
# 2. POPULAÇÃO DO BANCO DE DADOS
# =============================================================================
print("2️⃣  POPULANDO BANCO DE DADOS...")
print("-" * 70)

try:
    supabase: Client = create_client(
        os.getenv("SUPABASE_URL"),
        os.getenv("SUPABASE_SERVICE_KEY")
    )
    
    print("✅ Conectado ao Supabase")
    print()
    
    # ---------------------------------------------------------------------------
    # TABELA: users
    # ---------------------------------------------------------------------------
    print("📊 Inserindo usuário de teste...")
    try:
        user_data = {
            "id": str(uuid.uuid4()), # Generate a UUID for the test user
            "name": "Admin Teste",
            "nickname": "admin_test",
            "email": "admin@efootball.com",
            # "password_hash": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5OwRy7z1dzjIm",  # removido: users é sincronizado com Supabase Auth
            "platform": "pc",
            "role": "admin"
        }
        
        result = supabase.table('users').insert(user_data).execute()
        print(f"   ✅ Usuário inserido: {result.data[0]['email']}")
    except Exception as e:
        if "duplicate" in str(e).lower() or "unique" in str(e).lower():
            print(f"   ℹ️  Usuário já existe: {e}")
        else:
            print(f"   ⚠️  Erro: {str(e)[:50]}...")
    
    # ---------------------------------------------------------------------------
    # TABELA: cards
    # ---------------------------------------------------------------------------
    print("📊 Inserindo carta de jogador...")
    try:
        card_data = {
            "konami_id": 12345,
            "name": "Neymar Jr",
            "card_type": "Legendary",
            "position": "LWF"
        }
        
        result = supabase.table('cards').insert(card_data).execute()
        card_id = result.data[0]['id']
        print(f"   ✅ Carta inserida: {result.data[0]['name']} (ID: {card_id})")
    except Exception as e:
        if "duplicate" in str(e).lower() or "unique" in str(e).lower():
            print(f"   ℹ️  Carta já existe: {e}, buscando ID...")
            result = supabase.table('cards').select('id').eq('konami_id', 12345).execute()
            card_id = result.data[0]['id'] if result.data else 1
        else:
            print(f"   ⚠️  Erro: {str(e)[:50]}...")
            card_id = 1
    
    # ---------------------------------------------------------------------------
    # TABELA: builds
    # ---------------------------------------------------------------------------
    print("📊 Inserindo build meta...")
    try:
        
        # Buscar user_id - prioriza o recém-inserido ou um existente
        user_result = supabase.table('users').select('id').eq('email', 'admin@efootball.com').limit(1).execute()
        user_id = user_result.data[0]['id'] if user_result.data else None
        
        if not user_id:
            print("   ⚠️  Não foi possível obter um user_id válido para builds e dicas. Pulando...")
            exit(1) # Exit the script early if no user_id is available
        
        build_data = {
            "user_id": user_id,
            "card_id": card_id,
            "title": "Neymar LWF Meta Build",
            "shooting": 10,
            "passing": 7,
            "dribbling": 10,
            "dexterity": 8,
            "lower_body_strength": 5,
            "aerial_strength": 0,
            "defending": 0,
            "gk_1": 0,
            "gk_2": 0,
            "gk_3": 0,
            "overall_rating": 95,
            "is_official_meta": True,
            "meta_content": {
                "playstyle": "Prolific Winger",
                "dicas_taticas": [
                    "Use Double Touch em 1v1",
                    "Finalize de fora da área com finesse shot",
                    "Abuse dos dribles no 1v1"
                ],
                "quando_usar": "Contra defesas lentas",
                "pro_player": "Admin Test"
            }
        }
        
        result = supabase.table('builds').insert(build_data).execute()
        print(f"   ✅ Build inserida: {result.data[0]['title']}")
    except Exception as e:
        print(f"   ⚠️  Erro: {str(e)[:100]}...")
    
    # ---------------------------------------------------------------------------
    # TABELA: gameplay_tips
    # ---------------------------------------------------------------------------
    print("📊 Inserindo dica de gameplay...")
    try:
        tip_data = {
            "category": "finalizacao",
            "title": "Como fazer finesse shot perfeito",
            "pain_description": "Meus chutes de finesse sempre vão para fora ou o goleiro defende fácil",
            "solution": """1. Posicione o jogador no ângulo de 45° em relação ao gol
2. Segure L2 + R2 + botão de chute (ou LT + RT + B/Circle)
3. Use 70% de força (não encha a barra completa)
4. Direcione para o canto OPOSTO ao pé do jogador
5. IMPORTANTE: Só funciona bem com jogadores de finalizaçao 85+""",
            "created_by_user_id": user_id
        }
        
        result = supabase.table('gameplay_tips').insert(tip_data).execute()
        print(f"   ✅ Dica inserida: {result.data[0]['title']}")
    except Exception as e:
        print(f"   ⚠️  Erro: {str(e)[:100]}...")
    
    # ---------------------------------------------------------------------------
    # TABELA: ai_cache
    # ---------------------------------------------------------------------------
    print("📊 Inserindo cache de resposta da IA...")
    try:
        import hashlib
        
        prompt = "Como fazer finesse shot?"
        prompt_hash = hashlib.sha256(prompt.encode()).hexdigest()
        
        cache_data = {
            "prompt_hash": prompt_hash,
            "response_text": "Para fazer finesse shot no eFootball: Segure L2+R2 enquanto chuta, use 70% de força e direcione para o canto oposto. Funciona melhor com jogadores de alta finalização.",
            "expires_at": None
        }
        
        result = supabase.table('ai_cache').insert(cache_data).execute()
        print(f"   ✅ Cache inserido (hash: {prompt_hash[:16]}...)")
    except Exception as e:
        if "duplicate" in str(e).lower() or "unique" in str(e).lower():
            print("   ℹ️  Cache já existe")
        else:
            print(f"   ⚠️  Erro: {str(e)[:100]}...")
    
    print()
    print("="*70)
    print("✅ POPULAÇÃO DO BANCO CONCLUÍDA!")
    print("="*70)
    print()
    
    # Mostrar resumo
    print("📈 RESUMO DOS DADOS:")
    print("-" * 70)
    
    users_count = supabase.table('users').select('*', count='exact').execute()
    cards_count = supabase.table('cards').select('*', count='exact').execute()
    builds_count = supabase.table('builds').select('*', count='exact').execute()
    tips_count = supabase.table('gameplay_tips').select('*', count='exact').execute()
    cache_count = supabase.table('ai_cache').select('*', count='exact').execute()
    
    print(f"👥 Usuários: {users_count.count}")
    print(f"🎴 Cartas: {cards_count.count}")
    print(f"⚡ Builds: {builds_count.count}")
    print(f"💡 Dicas: {tips_count.count}")
    print(f"💾 Cache: {cache_count.count}")
    print()
    
except Exception as e:
    print(f"❌ Erro ao popular banco: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print("="*70)
print("🎉 TODOS OS TESTES CONCLUÍDOS COM SUCESSO!")
print("="*70)
