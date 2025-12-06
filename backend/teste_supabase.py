import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

print("🗄️  Testando conexão com Supabase...\n")

try:
    # Conectar ao Supabase
    supabase: Client = create_client(
        os.getenv("SUPABASE_URL"),
        os.getenv("SUPABASE_KEY")
    )
    
    print(f"✅ Conectado ao Supabase: {os.getenv('SUPABASE_URL')}\n")
    
    # Testar se as tabelas existem
    print("📊 Verificando tabelas...\n")
    
    # Tentar consultar cada tabela
    tabelas = ['users', 'builds', 'builds_meta', 'gameplay_tips', 'user_interactions']
    
    for tabela in tabelas:
        try:
            response = supabase.table(tabela).select("*").limit(1).execute()
            print(f"   ✅ Tabela '{tabela}' existe (registros: {len(response.data)})")
        except Exception as e:
            print(f"   ❌ Tabela '{tabela}' não encontrada ou erro: {str(e)[:50]}...")
    
    print("\n" + "="*60)
    print("📋 INSTRUÇÕES PARA CRIAR AS TABELAS:")
    print("="*60)
    print("1. Acesse: https://supabase.com/dashboard")
    print("2. Selecione seu projeto")
    print("3. Vá em: SQL Editor (menu lateral)")
    print("4. Clique em: New Query")
    print("5. Copie e cole o conteúdo de: database/CREATE_TABLES.sql")
    print("6. Clique em: Run")
    print("7. Aguarde a execução (pode levar 1-2 minutos)")
    print("8. Execute novamente este script para verificar")
    print("="*60 + "\n")
    
except Exception as e:
    print(f"❌ Erro ao conectar com Supabase: {e}\n")
    print("Verifique se a URL e a KEY estão corretas no arquivo .env")
