# 🎮 eFootball Coach - IA para Consultoria de Gameplay

## 📋 Visão Geral

Assistente virtual com IA que ajuda jogadores de eFootball a:
- ⚡ **Builds de Cartas**: Como distribuir pontos de evolução
- 🎯 **Ajuda de Gameplay**: Corrigir erros táticos e melhorar performance

## 🏗️ Arquitetura

```
┌─────────────┐      ┌──────────────────┐      ┌─────────────────┐
│   React     │◄────►│  FastAPI         │◄────►│   Supabase      │
│  (Frontend) │      │  (Backend)       │      │   (Database)    │
└─────────────┘      └──────────────────┘      └─────────────────┘
                              │
                              ▼
                     ┌──────────────────┐
                     │   Modelo IA      │
                     │  (Gemini/Claude) │
                     │  + Cache         │
                     └──────────────────┘
                              │
                              ▼
                     ┌──────────────────┐
                     │   Base de        │
                     │   Conhecimento   │
                     │   (RAG)          │
                     └──────────────────┘
```

## 🛠️ Stack Tecnológica

### Backend
- **FastAPI** (Python 3.11+)
- **SQLAlchemy** (ORM)
- **Supabase** (PostgreSQL + Auth)
- **LangChain** (RAG + Cache Semântico)
- **Celery** (Scraping assíncrono)

### Frontend
- **React 18** + **TypeScript**
- **Vite** (Build Tool)
- **TailwindCSS** (UI)
- **React Query** (Cache HTTP)

### IA
- **Modelo**: Gemini Flash 1.5 (início) → Claude Haiku (escala)
- **RAG**: ChromaDB (vetores locais)
- **Cache**: Anthropic Prompt Caching ou Redis

## 📁 Estrutura de Pastas

```
projetoefutebol/
├── backend/                    # FastAPI
│   ├── app/
│   │   ├── api/               # Endpoints
│   │   │   ├── builds.py      # Consulta builds de cartas
│   │   │   ├── gameplay.py    # Dicas de gameplay
│   │   │   └── users.py       # Auth + Freemium
│   │   ├── core/              # Config
│   │   │   ├── config.py
│   │   │   └── security.py
│   │   ├── services/
│   │   │   ├── ai_service.py  # Integração IA
│   │   │   ├── cache.py       # Cache Semântico
│   │   │   └── rag.py         # Sistema RAG
│   │   ├── scrapers/          # Python scrapers
│   │   │   └── efootball_hub.py
│   │   └── models/            # SQLAlchemy
│   ├── requirements.txt
│   └── main.py
│
├── frontend/                   # React
│   ├── src/
│   │   ├── components/
│   │   │   ├── BuildConsultant.tsx
│   │   │   └── GameplayAssistant.tsx
│   │   ├── pages/
│   │   ├── services/
│   │   │   └── api.ts
│   │   └── App.tsx
│   ├── package.json
│   └── vite.config.ts
│
├── knowledge_base/             # Base de Conhecimento
│   ├── builds/                # Planilhas do Pro Player
│   │   └── builds_guide.json
│   ├── gameplay/              # FAQs de gameplay
│   │   └── tactics_faq.json
│   └── players_data/          # Dados scraped
│       └── players.json
│
└── docs/
    └── COMPARACAO_IAS.md      # Este arquivo
```

## 🎯 Módulos Principais

### 1️⃣ Consulta de Builds (builds.py)
**Input**: "Melhor build para Neymar CF"
**Processo**:
1. Busca dados do jogador (scraper)
2. Consulta planilha do Pro Player (RAG)
3. IA monta resposta personalizada
4. Salva no cache semântico

### 2️⃣ Ajuda de Gameplay (gameplay.py)
**Input**: "Como defender bola aérea?"
**Processo**:
1. Busca no FAQ do Pro Player (RAG)
2. IA explica em linguagem simples
3. Retorna vídeo/imagem se disponível
4. Cache da resposta

## 💰 Sistema Freemium

| Tipo | Perguntas/Dia | Custo/Mês |
|------|---------------|-----------|
| Free | 5 perguntas | R$ 0 |
| Premium | Ilimitado | R$ 19,90 |

**Controle**: Token count no Supabase + Rate Limiting

## 🚀 Próximos Passos

1. [ ] Setup inicial do projeto
2. [ ] Backend FastAPI + Supabase
3. [ ] Integração Gemini Flash
4. [ ] Sistema RAG básico
5. [ ] Frontend React
6. [ ] Cache semântico
7. [ ] Sistema de pagamento

---

**Versão**: 1.0.0  
**Última atualização**: 04/12/2024
