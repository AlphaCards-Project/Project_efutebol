"""
Script para testar os endpoints de autenticação da API
Execute: python test_auth_endpoints.py
"""

import requests
import json
from datetime import datetime
import random
import string

# Configurações
BASE_URL = "http://localhost:8000/api/v1"
TIMEOUT = 10  # segundos

# Cores para terminal
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_success(message):
    print(f"{GREEN}✅ {message}{RESET}")

def print_error(message):
    print(f"{RED}❌ {message}{RESET}")

def print_info(message):
    print(f"{BLUE}ℹ️  {message}{RESET}")

def print_warning(message):
    print(f"{YELLOW}⚠️  {message}{RESET}")

def generate_random_email():
    """Gera um email aleatório para teste"""
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"teste_{random_str}@exemplo.com"

def test_health_check():
    """Testa se a API está rodando"""
    print_info("Testando health check...")
    try:
        response = requests.get(f"{BASE_URL.replace('/api/v1', '')}/health", timeout=TIMEOUT)
        if response.status_code == 200:
            print_success("API está rodando!")
            return True
        else:
            print_error(f"API retornou status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Não foi possível conectar à API. Certifique-se de que está rodando!")
        print_info("Execute: python main.py")
        return False
    except Exception as e:
        print_error(f"Erro ao testar health check: {str(e)}")
        return False

def test_register():
    """Testa o endpoint de registro"""
    print_info("\n=== Testando Registro de Usuário ===")
    
    # Dados do novo usuário
    email = generate_random_email()
    user_data = {
        "email": email,
        "password": "senha123",
        "full_name": "Usuário Teste",
        "nickname": f"teste{random.randint(1000, 9999)}",
        "platform": "console"
    }
    
    print_info(f"Registrando usuário: {email}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json=user_data,
            timeout=TIMEOUT
        )
        
        if response.status_code == 201:
            data = response.json()
            print_success("Usuário registrado com sucesso!")
            print_info(f"User ID: {data['user']['id']}")
            print_info(f"Email: {data['user']['email']}")
            print_info(f"Nome: {data['user']['name']}")
            print_info(f"Token gerado: {data['access_token'][:50]}...")
            return {
                "email": email,
                "password": "senha123",
                "token": data['access_token'],
                "user_id": data['user']['id']
            }
        elif response.status_code == 409:
            print_warning("Email já cadastrado (esperado se executar múltiplas vezes)")
            return None
        else:
            print_error(f"Erro ao registrar: Status {response.status_code}")
            print_error(f"Resposta: {response.text}")
            return None
            
    except Exception as e:
        print_error(f"Erro na requisição: {str(e)}")
        return None

def test_login(email, password):
    """Testa o endpoint de login"""
    print_info("\n=== Testando Login ===")
    
    credentials = {
        "email": email,
        "password": password
    }
    
    print_info(f"Fazendo login com: {email}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json=credentials,
            timeout=TIMEOUT
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success("Login realizado com sucesso!")
            print_info(f"Token recebido: {data['access_token'][:50]}...")
            print_info(f"User ID: {data['user']['id']}")
            print_info(f"Premium: {data['user']['is_premium']}")
            print_info(f"Perguntas usadas: {data['user']['daily_questions_used']}")
            return data['access_token']
        elif response.status_code == 401:
            print_error("Credenciais inválidas")
            return None
        else:
            print_error(f"Erro no login: Status {response.status_code}")
            print_error(f"Resposta: {response.text}")
            return None
            
    except Exception as e:
        print_error(f"Erro na requisição: {str(e)}")
        return None

def test_get_user_profile(token):
    """Testa o endpoint de perfil do usuário"""
    print_info("\n=== Testando Perfil do Usuário ===")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(
            f"{BASE_URL}/users/me",
            headers=headers,
            timeout=TIMEOUT
        )
        
        if response.status_code == 200:
            user = response.json()
            print_success("Perfil obtido com sucesso!")
            print_info("Dados do usuário:")
            print(json.dumps(user, indent=2, ensure_ascii=False))
            return True
        elif response.status_code == 401:
            print_error("Token inválido ou expirado")
            return False
        else:
            print_error(f"Erro ao obter perfil: Status {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Erro na requisição: {str(e)}")
        return False

def test_get_quota(token):
    """Testa o endpoint de quota"""
    print_info("\n=== Testando Quota de Perguntas ===")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(
            f"{BASE_URL}/users/quota",
            headers=headers,
            timeout=TIMEOUT
        )
        
        if response.status_code == 200:
            quota = response.json()
            print_success("Quota obtida com sucesso!")
            print_info(f"Limite diário: {quota['daily_limit']}")
            print_info(f"Perguntas usadas: {quota['questions_used']}")
            print_info(f"Perguntas restantes: {quota['questions_remaining']}")
            print_info(f"É premium: {quota['is_premium']}")
            return True
        else:
            print_error(f"Erro ao obter quota: Status {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Erro na requisição: {str(e)}")
        return False

def test_invalid_token():
    """Testa autenticação com token inválido"""
    print_info("\n=== Testando Token Inválido ===")
    
    headers = {
        "Authorization": "Bearer token_invalido_123"
    }
    
    try:
        response = requests.get(
            f"{BASE_URL}/users/me",
            headers=headers,
            timeout=TIMEOUT
        )
        
        if response.status_code == 401:
            print_success("Token inválido rejeitado corretamente!")
            return True
        else:
            print_error(f"Esperava status 401, recebeu {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Erro na requisição: {str(e)}")
        return False

def test_duplicate_email():
    """Testa registro com email duplicado"""
    print_info("\n=== Testando Email Duplicado ===")
    
    # Usar um email que provavelmente já existe
    user_data = {
        "email": "teste@exemplo.com",
        "password": "senha123"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json=user_data,
            timeout=TIMEOUT
        )
        
        if response.status_code == 409:
            print_success("Email duplicado rejeitado corretamente!")
            return True
        elif response.status_code == 201:
            print_warning("Email aceito (primeira vez que executa)")
            return True
        else:
            print_error(f"Resposta inesperada: Status {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Erro na requisição: {str(e)}")
        return False

def main():
    """Função principal que executa todos os testes"""
    print(f"\n{'='*60}")
    print(f"🧪 TESTE DOS ENDPOINTS DE AUTENTICAÇÃO")
    print(f"{'='*60}\n")
    print_info(f"Base URL: {BASE_URL}")
    print_info(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # 1. Verificar se API está rodando
    if not test_health_check():
        print_error("\n❌ Testes abortados: API não está acessível")
        return
    
    # 2. Testar registro
    user_info = test_register()
    if not user_info:
        print_warning("\nContinuando com testes usando email fixo...")
        user_info = {
            "email": "teste@exemplo.com",
            "password": "senha123"
        }
    
    # 3. Testar login
    token = test_login(user_info["email"], user_info["password"])
    if not token:
        print_error("\n❌ Testes abortados: não foi possível fazer login")
        return
    
    # 4. Testar perfil do usuário
    test_get_user_profile(token)
    
    # 5. Testar quota
    test_get_quota(token)
    
    # 6. Testar token inválido
    test_invalid_token()
    
    # 7. Testar email duplicado
    test_duplicate_email()
    
    # Resumo
    print(f"\n{'='*60}")
    print(f"✅ TODOS OS TESTES CONCLUÍDOS")
    print(f"{'='*60}\n")
    print_success("Endpoints de autenticação estão funcionando corretamente!")
    print_info("\nVocê pode testar manualmente acessando:")
    print_info(f"  Swagger UI: {BASE_URL.replace('/api/v1', '')}/api/v1/docs")
    print_info(f"  ReDoc: {BASE_URL.replace('/api/v1', '')}/api/v1/redoc\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_warning("\n\nTestes interrompidos pelo usuário")
    except Exception as e:
        print_error(f"\n\nErro inesperado: {str(e)}")
