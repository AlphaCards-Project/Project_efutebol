#!/usr/bin/env python3
"""
Script de teste de conexão com banco de dados Supabase
Valida estrutura de tabelas do CREATE_TABLES.sql
"""

import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

def test_connection():
    """Testa conexão com Supabase"""
    print("="*70)
    print("🗄️  TESTE DE CONEXÃO COM BANCO DE DADOS SUPABASE")
    print("="*70)
    print()
    
    # Verificar variáveis de ambiente
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    if not supabase_url or not supabase_key:
        print("❌ ERRO: Variáveis de ambiente não configuradas!")
        print("   Por favor, configure SUPABASE_URL e SUPABASE_KEY no arquivo .env")
        return False
    
    print(f"📍 URL do Supabase: {supabase_url}")
    print(f"🔑 API Key: {supabase_key[:20]}...{supabase_key[-10:]}")
    print()
    
    try:
        # Conectar ao Supabase
        supabase: Client = create_client(supabase_url, supabase_key)
        print("✅ Conexão estabelecida com sucesso!")
        print()
        
        # Tabelas esperadas do CREATE_TABLES.sql
        tabelas_esperadas = [
            ('users', 'Usuários do sistema'),
            ('cards', 'Cartas/Jogadores do eFootball'),
            ('builds', 'Builds de cartas (distribuição de pontos)'),
            ('gameplay_tips', 'Dicas de gameplay'),
            ('ai_cache', 'Cache de respostas da IA')
        ]
        
        print("📊 VERIFICANDO ESTRUTURA DO BANCO DE DADOS")
        print("-" * 70)
        
        tabelas_ok = 0
        tabelas_erro = 0
        
        for tabela, descricao in tabelas_esperadas:
            try:
                # Tentar consultar a tabela
                response = supabase.table(tabela).select("*").limit(1).execute()
                registros = len(response.data)
                
                print(f"✅ {tabela:20s} | {descricao:35s} | {registros} registro(s)")
                tabelas_ok += 1
                
            except Exception as e:
                error_msg = str(e)
                if "does not exist" in error_msg or "relation" in error_msg:
                    print(f"❌ {tabela:20s} | {descricao:35s} | NÃO EXISTE")
                else:
                    print(f"⚠️  {tabela:20s} | {descricao:35s} | ERRO: {error_msg[:30]}...")
                tabelas_erro += 1
        
        print("-" * 70)
        print(f"\n📈 RESULTADO: {tabelas_ok}/{len(tabelas_esperadas)} tabelas encontradas")
        print()
        
        # Verificar ENUMs
        print("🔧 VERIFICANDO TIPOS ENUM")
        print("-" * 70)
        
        enums_esperados = [
            ('user_platform', ['console', 'pc', 'mobile']),
            ('user_role', ['admin', 'premium', 'free'])
        ]
        
        # Nota: Supabase não permite consulta direta de ENUMs via API REST
        # Precisaria usar função RPC ou consulta SQL direta
        print("ℹ️  Verificação de ENUMs requer acesso SQL direto")
        print("   Verifique manualmente no Supabase Dashboard > SQL Editor")
        print()
        
        # Status final
        if tabelas_erro == 0:
            print("="*70)
            print("🎉 SUCESSO! Todas as tabelas estão criadas corretamente!")
            print("="*70)
            print()
            print("✨ PRÓXIMOS PASSOS:")
            print("   1. Preencher tabela 'cards' com jogadores")
            print("   2. Preencher tabela 'builds' com builds meta")
            print("   3. Preencher tabela 'gameplay_tips' com dicas")
            print("   4. Executar a API: python main.py")
            print()
            return True
        else:
            print("="*70)
            print("⚠️  ATENÇÃO! Algumas tabelas não foram encontradas!")
            print("="*70)
            print()
            print("📋 INSTRUÇÕES PARA CRIAR AS TABELAS:")
            print("-" * 70)
            print("1. Acesse: https://supabase.com/dashboard")
            print("2. Selecione seu projeto")
            print("3. Clique em: SQL Editor (menu lateral)")
            print("4. Clique em: New Query")
            print("5. Abra o arquivo: database/CREATE_TABLES.sql")
            print("6. Copie TODO o conteúdo do arquivo")
            print("7. Cole no SQL Editor do Supabase")
            print("8. Clique em: Run (botão verde)")
            print("9. Aguarde a execução (pode levar 1-2 minutos)")
            print("10. Execute novamente este script: python test_database_connection.py")
            print("-" * 70)
            print()
            return False
            
    except Exception as e:
        print(f"❌ ERRO ao conectar com Supabase: {e}")
        print()
        print("🔍 POSSÍVEIS CAUSAS:")
        print("   • URL ou API Key incorretas no arquivo .env")
        print("   • Projeto Supabase não existe ou foi deletado")
        print("   • Problemas de rede/firewall")
        print("   • API Key expirada ou sem permissões")
        print()
        return False


def test_sample_queries():
    """Testa queries básicas nas tabelas"""
    print("="*70)
    print("🧪 TESTANDO QUERIES BÁSICAS")
    print("="*70)
    print()
    
    try:
        supabase: Client = create_client(
            os.getenv("SUPABASE_URL"),
            os.getenv("SUPABASE_KEY")
        )
        
        # Teste 1: Contar usuários
        try:
            response = supabase.table('users').select('*', count='exact').execute()
            print(f"✅ Total de usuários: {response.count}")
        except:
            print("⚠️  Não foi possível contar usuários")
        
        # Teste 2: Contar cartas
        try:
            response = supabase.table('cards').select('*', count='exact').execute()
            print(f"✅ Total de cartas cadastradas: {response.count}")
        except:
            print("⚠️  Não foi possível contar cartas")
        
        # Teste 3: Contar builds
        try:
            response = supabase.table('builds').select('*', count='exact').execute()
            print(f"✅ Total de builds cadastradas: {response.count}")
        except:
            print("⚠️  Não foi possível contar builds")
        
        # Teste 4: Contar dicas de gameplay
        try:
            response = supabase.table('gameplay_tips').select('*', count='exact').execute()
            print(f"✅ Total de dicas de gameplay: {response.count}")
        except:
            print("⚠️  Não foi possível contar dicas")
        
        print()
        
    except Exception as e:
        print(f"❌ Erro ao executar queries: {e}")
        print()


if __name__ == "__main__":
    # Executar teste de conexão
    connection_ok = test_connection()
    
    # Se conexão OK, testar queries
    if connection_ok:
        test_sample_queries()
    
    print("="*70)
    print("Teste finalizado!")
    print("="*70)
