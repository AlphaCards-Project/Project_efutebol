# 📚 Documentação do Projeto eFootball Coach API

## 📋 Índice
1. [Visão Geral](#visão-geral)
2. [Arquitetura do Sistema](#arquitetura-do-sistema)
3. [Estrutura do Banco de Dados](#estrutura-do-banco-de-dados)
4. [Fluxo de Funcionamento](#fluxo-de-funcionamento)
5. [Endpoints da API](#endpoints-da-api)
6. [Serviços e Componentes](#serviços-e-componentes)
7. [Sistema de Cache](#sistema-de-cache)
8. [Autenticação e Autorização](#autenticação-e-autorização)
9. [Sistema de Quotas](#sistema-de-quotas)
10. [Como Executar](#como-executar)

---

## 🎯 Visão Geral

O **eFootball Coach API** é uma aplicação de consultoria inteligente para jogadores de eFootball que combina:
- 🧠 Inteligência Artificial (Google Gemini)
- 📊 Base de conhecimento estruturada (RAG - Retrieval-Augmented Generation)
- 💾 Banco de dados PostgreSQL (via Supabase)
- ⚡ Sistema de cache (Redis)
- 🔐 Autenticação JWT

### Objetivo Principal
Responder perguntas de jogadores sobre:
1. **Builds de Cartas**: Como distribuir pontos de habilidade para jogadores específicos
2. **Gameplay**: Dicas táticas, comandos, soluções para problemas comuns

---

## 🏗️ Arquitetura do Sistema

```
┌─────────────┐
│   Usuário   │
└──────┬──────┘
       │ Pergunta
       ▼
┌─────────────────────────────────────────────┐
│           FastAPI Backend                    │
│                                              │
│  ┌────────────┐  ┌──────────────┐           │
│  │   Auth     │  │   Endpoints  │           │
│  │  (JWT)     │  │  /builds     │           │
│  └────────────┘  │  /gameplay   │           │
│                  └───────┬──────┘           │
│                          │                   │
│                          ▼                   │
│            ┌─────────────────────┐           │
│            │   RAG Service       │           │
│            │  (Knowledge Base)   │           │
│            └──────────┬──────────┘           │
│                       │                      │
│         ┌─────────────┴─────────────┐        │
│         ▼                           ▼        │
│  ┌────────────┐            ┌──────────────┐ │
│  │  Supabase  │            │   Gemini AI  │ │
│  │ PostgreSQL │            │   (Google)   │ │
│  └────────────┘            └──────────────┘ │
│         ▲                                    │
│         │                                    │
│  ┌──────┴───────┐                            │
│  │ Redis Cache  │                            │
│  └──────────────┘                            │
└─────────────────────────────────────────────┘
```

### Fluxo de Dados
1. **Usuário** envia pergunta via API
2. **FastAPI** valida autenticação JWT
3. **Sistema de Quota** verifica limite diário
4. **Cache Redis** verifica resposta em cache
5. **RAG Service** busca contexto no banco de dados
6. **Gemini AI** gera resposta personalizada
7. **Cache** armazena resposta para futuras consultas
8. **Resposta** retorna ao usuário

---

## 🗄️ Estrutura do Banco de Dados

### Tabelas Principais

#### 1. `users` - Usuários do Sistema
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    nickname VARCHAR(50) UNIQUE, 
    email VARCHAR(255) NOT NULL UNIQUE, 
    password_hash VARCHAR(255) NOT NULL, 
    platform user_platform,                    -- console, pc, mobile
    role user_role NOT NULL DEFAULT 'free',    -- admin, premium, free
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

**Propósito**: Armazena usuários que podem fazer perguntas ao sistema. Profissionais admin preencherão dados.

---

#### 2. `cards` - Cartas de Jogadores
```sql
CREATE TABLE cards (
    id SERIAL PRIMARY KEY,
    konami_id INTEGER UNIQUE,
    name VARCHAR(100) NOT NULL,
    card_type VARCHAR(50),
    position VARCHAR(10)
);
```

**Propósito**: Catálogo de cartas/jogadores do eFootball. Será preenchido por profissionais via interface futura.

**Exemplos de dados**:
- Neymar Jr (LWF, RWF, SS, AMF)
- Cristiano Ronaldo (CF, LWF, SS)
- Messi (RWF, SS, AMF)

---

#### 3. `builds` - Builds de Cartas (Meta Builds)
```sql
CREATE TABLE builds (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    card_id INTEGER NOT NULL REFERENCES cards(id) ON DELETE CASCADE, 
    title VARCHAR(100) NOT NULL,
    
    -- Distribuição de pontos (0-99 cada)
    shooting INTEGER CHECK (shooting BETWEEN 0 AND 99) DEFAULT 0,
    passing INTEGER CHECK (passing BETWEEN 0 AND 99) DEFAULT 0,
    dribbling INTEGER CHECK (dribbling BETWEEN 0 AND 99) DEFAULT 0,
    dexterity INTEGER CHECK (dexterity BETWEEN 0 AND 99) DEFAULT 0,
    lower_body_strength INTEGER CHECK (lower_body_strength BETWEEN 0 AND 99) DEFAULT 0,
    aerial_strength INTEGER CHECK (aerial_strength BETWEEN 0 AND 99) DEFAULT 0,
    defending INTEGER CHECK (defending BETWEEN 0 AND 99) DEFAULT 0,
    gk_1 INTEGER CHECK (gk_1 BETWEEN 0 AND 99) DEFAULT 0,
    gk_2 INTEGER CHECK (gk_2 BETWEEN 0 AND 99) DEFAULT 0,
    gk_3 INTEGER CHECK (gk_3 BETWEEN 0 AND 99) DEFAULT 0,
    
    overall_rating INTEGER,
    is_official_meta BOOLEAN DEFAULT FALSE,
    meta_content JSONB,  -- Informações extras (playstyle, dicas, etc)
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

**Propósito**: Armazena builds **oficiais e aprovadas** por profissionais. A IA busca aqui para dar respostas precisas.

**Exemplo de `meta_content` JSON**:
```json
{
  "playstyle": "Prolific Winger",
  "dicas_taticas": [
    "Use Double Touch em 1v1",
    "Finalize de fora da área com finesse shot"
  ],
  "quando_usar": "Contra defesas lentas",
  "pro_player": "ZeCoxinha"
}
```

---

#### 4. `gameplay_tips` - Dicas de Gameplay
```sql
CREATE TABLE gameplay_tips (
    id SERIAL PRIMARY KEY,
    category VARCHAR(50) NOT NULL,              -- "defesa", "ataque", "passe", etc
    title VARCHAR(255) NOT NULL,
    pain_description TEXT,                      -- "Estou tomando muitos gols de contra-ataque"
    solution TEXT NOT NULL,                     -- Solução passo-a-passo
    created_by_user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

**Propósito**: Base de conhecimento de problemas e soluções. Profissionais cadastram aqui.

**Exemplo de registro**:
```
category: "defesa"
title: "Como parar contra-ataques rápidos"
pain_description: "Tomo muito gol quando erro ataque e adversário sai no contra"
solution: "1. Use Team Press (D-pad para cima)
           2. Segure R1+X para pressionar com 2 jogadores
           3. Mantenha sempre um volante como 'Anchor Man'
           4. Configure tática Defensive no Management"
```

---

#### 5. `ai_cache` - Cache de Respostas da IA
```sql
CREATE TABLE ai_cache (
    id SERIAL PRIMARY KEY,
    prompt_hash VARCHAR(64) NOT NULL UNIQUE,    -- SHA256 da pergunta
    response_text TEXT NOT NULL,                -- Resposta completa da IA
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE         -- Expiração opcional
);
```

**Propósito**: **Economia de custos** e **performance**. Armazena respostas já geradas para não reconsultar a API do Gemini.

**Como funciona**:
1. Usuário pergunta "Como fazer finesse shot?"
2. Sistema calcula hash SHA256 da pergunta
3. Busca no cache → Se encontrar, retorna imediatamente
4. Se não encontrar → Consulta IA → Salva no cache

---

### Índices (Performance)
```sql
-- Acelera busca de builds por usuário/carta
CREATE INDEX idx_builds_user_id ON builds(user_id);
CREATE INDEX idx_builds_card_id ON builds(card_id);

-- Acelera busca de dicas por categoria
CREATE INDEX idx_gameplay_tips_category ON gameplay_tips(category);

-- Acelera busca no cache
CREATE INDEX idx_ai_cache_prompt_hash ON ai_cache(prompt_hash);

-- Acelera buscas dentro do JSON meta_content
CREATE INDEX idx_builds_meta_content ON builds USING GIN (meta_content);
```

---

## 🔄 Fluxo de Funcionamento

### Fluxo Completo de uma Pergunta

#### Cenário 1: Pergunta sobre Build
```
Usuário: "Qual a melhor build para Neymar como LWF?"
    │
    ▼
[1] FastAPI valida JWT token
    │
    ▼
[2] Verifica quota diária (free: 5/dia, premium: 100/dia)
    │
    ▼
[3] Gera hash da pergunta: SHA256("neymar + lwf")
    │
    ▼
[4] Busca no Redis Cache
    │
    ├─ Cache HIT → Retorna resposta imediatamente ✅
    │
    └─ Cache MISS → Continua...
        │
        ▼
    [5] RAG Service busca contexto no Supabase:
        - Busca em `builds` WHERE card_id = Neymar AND position = LWF
        - Retorna distribuição de pontos + meta_content
        │
        ▼
    [6] Monta prompt enriquecido para Gemini:
        """
        Você é especialista em eFootball.
        
        Jogador: Neymar Jr
        Posição: LWF
        
        Build oficial do Pro Player:
        - Dribbling: 10 pontos
        - Speed: 8 pontos
        - Finishing: 10 pontos
        Playstyle: Prolific Winger
        
        Forneça resposta detalhada...
        """
        │
        ▼
    [7] Gemini processa e gera resposta personalizada
        │
        ▼
    [8] Salva resposta no cache (Redis + Supabase ai_cache)
        │
        ▼
    [9] Retorna resposta ao usuário
```

---

#### Cenário 2: Pergunta sobre Gameplay
```
Usuário: "Como fazer finesse shot?"
    │
    ▼
[1-4] Mesmos passos de autenticação, quota e cache
    │
    ▼
[5] RAG Service busca em `gameplay_tips`:
    - WHERE category = 'finalizacao'
    - Busca por palavras-chave: "finesse", "shot", "finalizar"
    - Retorna registro:
        title: "Como fazer finesse shot perfeito"
        solution: "1. Segure L2 + R2 + botão de chute
                   2. Direcione para o canto oposto..."
    │
    ▼
[6] Monta prompt para Gemini com contexto do banco
    │
    ▼
[7-9] Gemini processa, salva cache, retorna
```

---

## 🌐 Endpoints da API

### Base URL
```
http://localhost:8000/api/v1
```

---

### 🔐 Autenticação

#### `POST /auth/register`
Registra novo usuário
```json
Request:
{
  "email": "jogador@email.com",
  "password": "senha123",
  "full_name": "João Silva"
}

Response:
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "email": "jogador@email.com",
    "is_premium": false
  }
}
```

#### `POST /auth/login`
Faz login
```json
Request:
{
  "email": "jogador@email.com",
  "password": "senha123"
}

Response:
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

---

### ⚽ Builds

#### `POST /builds/`
Consulta build de jogador
```json
Request:
{
  "player_name": "Neymar Jr",
  "position": "LWF"
}

Response:
{
  "player_name": "Neymar Jr",
  "position": "LWF",
  "priority_points": [
    {"skill": "Dribbling", "points": 10},
    {"skill": "Speed", "points": 8},
    {"skill": "Finishing", "points": 10}
  ],
  "playstyle": "Prolific Winger",
  "tips": "Use Double Touch em 1v1, finalize de fora...",
  "from_cache": false
}
```

#### `GET /builds/popular`
Lista builds mais consultadas
```json
Response:
{
  "popular_builds": [
    {"player": "Messi", "position": "RWF", "queries": 1523},
    {"player": "Ronaldo", "position": "CF", "queries": 1445}
  ]
}
```

---

### 🎮 Gameplay

#### `POST /gameplay/ask`
Faz pergunta sobre gameplay
```json
Request:
{
  "question": "Como fazer finesse shot?"
}

Response:
{
  "question": "Como fazer finesse shot?",
  "answer": "Para fazer finesse shot: 1. Segure L2+R2...",
  "category": "Finalizacao",
  "video_url": null,
  "from_cache": false
}
```

#### `GET /gameplay/categories`
Lista categorias de dúvidas
```json
Response:
{
  "categories": [
    {"name": "Ataque", "icon": "⚽", "questions_count": 15},
    {"name": "Defesa", "icon": "🛡️", "questions_count": 12}
  ]
}
```

---

### 👤 Usuários

#### `GET /users/quota`
Verifica quota de perguntas
```json
Response:
{
  "daily_limit": 5,
  "questions_used": 2,
  "questions_remaining": 3,
  "is_premium": false,
  "reset_time": "2024-12-07T00:00:00Z"
}
```

---

## 🧩 Serviços e Componentes

### 1. RAG Service (`rag_service.py`)
**Responsabilidade**: Buscar contexto na base de conhecimento antes de consultar IA

**Métodos principais**:
- `find_build_context(player_name, position)` → Busca builds no banco
- `find_gameplay_context(question)` → Busca dicas de gameplay
- `reload_knowledge_base()` → Recarrega dados após atualizações

**Sistema de camadas**:
1. Cartas Meta específicas (exceções)
2. Regras por posição (padrões gerais)
3. Arquivos JSON locais (fallback)

---

### 2. Gemini Service (`gemini_service.py`)
**Responsabilidade**: Interface com Google Gemini AI

**Métodos**:
- `generate_build_response(player, position, context)` → Gera resposta sobre builds
- `generate_gameplay_response(question, context)` → Gera resposta sobre gameplay
- `simple_query(prompt)` → Query genérica

**Configuração**:
```python
model = genai.GenerativeModel('gemini-1.5-flash')
```

---

### 3. Supabase Service (`supabase_service.py`)
**Responsabilidade**: Interface com PostgreSQL via Supabase

**Métodos principais**:
- `create_user()` → Cria usuário
- `authenticate_user()` → Autentica
- `check_and_increment_quota()` → Gerencia limites diários
- `get_quota_info()` → Retorna info de quota

---

### 4. Cache Service (`cache_service.py`)
**Responsabilidade**: Sistema de cache Redis + PostgreSQL

**Estratégia de cache**:
- **Redis**: Cache rápido em memória (TTL curto)
- **PostgreSQL (`ai_cache`)**: Cache persistente (economia de API)

**Tempos de expiração**:
- Builds: 7 dias (604800s)
- Gameplay: 24 horas (86400s)

---

## 🔐 Autenticação e Autorização

### Sistema JWT
```python
# Token válido por 24 horas
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

# Algoritmo de encriptação
ALGORITHM = "HS256"
```

### Decorador de Proteção
```python
@router.post("/builds/")
async def endpoint(current_user: dict = Depends(get_current_user)):
    # Apenas usuários autenticados podem acessar
    pass
```

---

## 📊 Sistema de Quotas

### Limites Diários
```python
FREE_TIER_DAILY_LIMIT = 5      # Usuários grátis
PREMIUM_TIER_DAILY_LIMIT = 100 # Usuários premium
```

### Reset Automático
- Reset diário às 00:00 UTC
- Campo `last_reset` na tabela `users`

### Verificação
```python
# Verifica e incrementa quota antes de processar
has_quota = await supabase_service.check_and_increment_quota(user_id)
if not has_quota:
    raise HTTPException(429, "Limite atingido")
```

---

## 🚀 Como Executar

### Pré-requisitos
```bash
# Python 3.12+
# PostgreSQL (via Supabase)
# Redis (opcional, para cache local)
```

### 1. Configurar Ambiente
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

### 2. Configurar `.env`
```bash
# Supabase
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua_anon_key
SUPABASE_SERVICE_KEY=sua_service_key

# Google Gemini
GOOGLE_API_KEY=sua_api_key_gemini

# JWT
SECRET_KEY=gere_um_secret_key_seguro

# Redis (opcional)
REDIS_HOST=localhost
REDIS_PORT=6379

# CORS
ALLOWED_ORIGINS=http://localhost:3000
```

### 3. Criar Tabelas no Banco
```bash
# Conecte no Supabase SQL Editor
# Execute o arquivo: database/CREATE_TABLES.sql
```

### 4. Executar API
```bash
python main.py
# ou
uvicorn main:app --reload --port 8000
```

### 5. Acessar Documentação
```
http://localhost:8000/api/v1/docs
```

---

## 📝 Preenchimento de Dados (Para Profissionais)

### Interface Futura (Em Desenvolvimento)
Os profissionais poderão cadastrar:

1. **Cartas** (`cards` table)
   - Adicionar novos jogadores
   - Definir posições possíveis

2. **Builds** (`builds` table)
   - Criar builds meta oficiais
   - Definir distribuição de pontos
   - Adicionar dicas táticas no `meta_content`

3. **Dicas de Gameplay** (`gameplay_tips` table)
   - Cadastrar problemas comuns
   - Definir soluções passo-a-passo
   - Categorizar por tipo

### Exemplo de Inserção Manual (SQL)
```sql
-- Inserir carta
INSERT INTO cards (konami_id, name, card_type, position)
VALUES (12345, 'Neymar Jr', 'Legendary', 'LWF');

-- Inserir build
INSERT INTO builds (
    user_id, card_id, title, 
    shooting, passing, dribbling, dexterity,
    is_official_meta, meta_content
) VALUES (
    1, 123, 'Neymar LWF Meta',
    10, 7, 10, 8,
    true,
    '{"playstyle": "Prolific Winger", "dicas": ["Use Double Touch"]}'::jsonb
);

-- Inserir dica de gameplay
INSERT INTO gameplay_tips (category, title, pain_description, solution)
VALUES (
    'finalizacao',
    'Como fazer finesse shot',
    'Meus chutes vão sempre para fora',
    '1. Segure L2+R2 ao chutar\n2. Direcione para canto oposto\n3. Use 70% de força'
);
```

---

## 🎯 Benefícios do Sistema

1. **Economia de Custos**: Cache evita chamadas repetidas à API do Gemini
2. **Respostas Precisas**: RAG usa dados verificados por profissionais
3. **Performance**: Redis + índices PostgreSQL = respostas rápidas
4. **Escalável**: Sistema de quotas controla uso
5. **Manutenível**: Base de conhecimento centralizada no banco

---

## 🔮 Próximos Passos

- [ ] Interface de administração para profissionais
- [ ] Sistema de votação de builds (upvote/downvote)
- [ ] Analytics de perguntas mais comuns
- [ ] Integração com scraping automático de sites
- [ ] Sistema de notificações de novas builds meta
- [ ] API de webhook para atualização de dados

---

## 📞 Contato

Para dúvidas sobre o sistema, contate o time de desenvolvimento.

**Versão**: 1.0.0  
**Última atualização**: Dezembro 2024
