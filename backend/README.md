# 🎮 eFootball Coach - Backend API

Backend FastAPI com integração Gemini Flash para consultoria de gameplay e builds.

## 🚀 Setup Rápido

### 1. Criar ambiente virtual
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 2. Instalar dependências
```bash
pip install -r requirements.txt
```

### 3. Configurar variáveis de ambiente
```bash
cp .env.example .env
# Edite o .env com suas credenciais
```

### 4. Configurar Supabase

Crie um projeto no [Supabase](https://supabase.com) e execute este SQL:

```sql
-- Tabela de usuários
CREATE TABLE users (
    id UUID PRIMARY KEY REFERENCES auth.users(id),
    email TEXT UNIQUE NOT NULL,
    full_name TEXT,
    is_premium BOOLEAN DEFAULT FALSE,
    daily_questions_used INTEGER DEFAULT 0,
    last_reset TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_premium ON users(is_premium);
```

### 5. Configurar Redis (opcional para cache)
```bash
# Docker
docker run -d -p 6379:6379 redis:alpine

# Ou instale localmente
# Ubuntu: sudo apt install redis-server
# Mac: brew install redis
```

### 6. Rodar servidor
```bash
python main.py
# ou
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Acesse: **http://localhost:8000/api/v1/docs**

## 📁 Estrutura

```
backend/
├── app/
│   ├── api/           # Endpoints REST
│   │   ├── auth.py    # Login/Registro
│   │   ├── builds.py  # Consulta de builds
│   │   ├── gameplay.py # Dicas de gameplay
│   │   └── users.py   # Perfil e quota
│   ├── core/
│   │   ├── config.py  # Configurações
│   │   └── security.py # JWT e auth
│   ├── models/
│   │   └── schemas.py # Pydantic models
│   └── services/
│       ├── gemini_service.py  # IA
│       ├── rag_service.py     # Base conhecimento
│       ├── cache_service.py   # Redis cache
│       └── supabase_service.py # Database
├── knowledge_base/
│   ├── builds/        # Planilhas do Pro Player
│   └── gameplay/      # FAQs
├── main.py           # Entry point
└── requirements.txt
```

## 🔑 Endpoints Principais

### Autenticação
- `POST /api/v1/auth/register` - Criar conta
- `POST /api/v1/auth/login` - Login
- `GET /api/v1/auth/me` - Usuário atual

### Builds
- `POST /api/v1/builds/` - Consultar build
  ```json
  {
    "player_name": "Neymar Jr",
    "position": "CF"
  }
  ```

### Gameplay
- `POST /api/v1/gameplay/ask` - Perguntar sobre gameplay
  ```json
  {
    "question": "Como fazer finesse shot?"
  }
  ```

### Usuário
- `GET /api/v1/users/quota` - Ver perguntas restantes
- `GET /api/v1/users/me` - Perfil completo

## 🧪 Testar API

### 1. Registrar usuário
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "teste@email.com",
    "password": "senha123",
    "full_name": "Teste"
  }'
```

### 2. Fazer login
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "teste@email.com",
    "password": "senha123"
  }'
```

### 3. Consultar build (use o token recebido)
```bash
curl -X POST "http://localhost:8000/api/v1/builds/" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "player_name": "Neymar Jr",
    "position": "CF"
  }'
```

## 📝 Base de Conhecimento

### Adicionar Novo Jogador
Edite `knowledge_base/builds/builds_guide.json`:

```json
{
  "name": "Nome do Jogador",
  "positions": {
    "CF": {
      "priority_points": [
        {"skill": "Finishing", "points": 10}
      ],
      "playstyle": "Goal Poacher",
      "tips": "Dica tática aqui"
    }
  }
}
```

### Adicionar FAQ de Gameplay
Edite `knowledge_base/gameplay/tactics_faq.json`:

```json
{
  "category": "Ataque",
  "question": "Como fazer X?",
  "answer": "Passo 1...\nPasso 2...",
  "video_url": "youtube.com/..."
}
```

## 🔧 Variáveis de Ambiente

```env
# Obrigatórias
GOOGLE_API_KEY=       # Console Google Cloud
SUPABASE_URL=         # Dashboard Supabase
SUPABASE_KEY=         # Dashboard Supabase
SECRET_KEY=           # openssl rand -hex 32

# Opcionais
REDIS_HOST=localhost
FREE_TIER_DAILY_LIMIT=5
PREMIUM_TIER_DAILY_LIMIT=100
```

## 🎯 Próximos Passos

1. ✅ Setup básico completo
2. ⏳ Implementar ChromaDB (cache semântico)
3. ⏳ Scraper de dados (eFootballHub)
4. ⏳ Sistema de pagamento (Stripe)
5. ⏳ Analytics e tracking

## 📊 Performance

- **Cache hit rate esperado**: 60-80%
- **Tempo resposta sem cache**: ~2-3s
- **Tempo resposta com cache**: ~100-200ms
- **Custo por pergunta**: ~R$ 0,001

## 🐛 Debug

```bash
# Logs detalhados
DEBUG=True uvicorn main:app --reload --log-level debug

# Verificar Redis
redis-cli ping

# Verificar Supabase
curl "https://seu-projeto.supabase.co/rest/v1/users" \
  -H "apikey: SUA_KEY"
```

---

**Versão**: 1.0.0  
**Autor**: eFootball Coach Team
