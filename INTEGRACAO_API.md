# Integração API - Frontend e Backend

## ✅ Status da Integração

A integração entre frontend e backend foi implementada com sucesso para os endpoints de **Players**, **Cards** e **Builds**.

## 📁 Estrutura de Serviços

### Backend (FastAPI)
```
backend/app/api/
├── players.py    # CRUD de jogadores
├── cards.py      # CRUD de cartas
└── builds.py     # CRUD e recomendações de builds
```

### Frontend (React + TypeScript)
```
frontend/src/services/
├── playersService.ts  # Integração com API de jogadores
├── cardsService.ts    # Integração com API de cartas
└── buildService.ts    # Integração com API de builds
```

## 🔌 Endpoints Implementados

### 1. Players API

#### Backend (`/api/v1/players`)
- `POST /` - Criar jogador (admin apenas)
- `GET /` - Listar jogadores (com filtros)
- `GET /{player_id}` - Buscar jogador por ID
- `PUT /{player_id}` - Atualizar jogador (admin apenas)
- `DELETE /{player_id}` - Deletar jogador (admin apenas)

#### Frontend (`playersService.ts`)
```typescript
import { playersService } from '@/services/playersService'

// Listar jogadores
const players = await playersService.listPlayers({ 
  search: 'Messi',
  nationality: 'Argentina',
  limit: 50 
})

// Criar jogador (admin)
const newPlayer = await playersService.createPlayer({
  name: 'Lionel Messi',
  nationality: 'Argentina'
})

// Buscar jogador específico
const player = await playersService.getPlayer(1)

// Atualizar jogador (admin)
await playersService.updatePlayer(1, { name: 'Leo Messi' })

// Deletar jogador (admin)
await playersService.deletePlayer(1)
```

### 2. Cards API

#### Backend (`/api/v1/cards`)
- `POST /` - Criar carta (admin apenas)
- `GET /` - Listar cartas (com filtros)
- `GET /{card_id}` - Buscar carta por ID
- `PUT /{card_id}` - Atualizar carta (admin apenas)
- `DELETE /{card_id}` - Deletar carta (admin apenas)

#### Frontend (`cardsService.ts`)
```typescript
import { cardsService } from '@/services/cardsService'

// Listar cartas
const cards = await cardsService.listCards({ 
  position: 'CF',
  card_type: 'Legend',
  search: 'Messi',
  limit: 50 
})

// Criar carta (admin)
const newCard = await cardsService.createCard({
  player_id: 1,
  name: 'Messi TOTY 2024',
  version: 'TOTY',
  card_type: 'Legend',
  position: 'RWF',
  overall_rating: 98,
  image_url: 'https://...'
})

// Buscar carta específica
const card = await cardsService.getCard(1)

// Atualizar carta (admin)
await cardsService.updateCard(1, { overall_rating: 99 })

// Deletar carta (admin)
await cardsService.deleteCard(1)
```

### 3. Builds API

#### Backend (`/api/v1/builds`)
- `POST /` - Obter recomendação de build (IA)
- `POST /create` - Criar build personalizada
- `GET /my-builds` - Listar builds do usuário
- `GET /card/{card_id}` - Listar builds de uma carta
- `GET /{build_id}` - Buscar build específica
- `PUT /{build_id}` - Atualizar build (apenas dono)
- `DELETE /{build_id}` - Deletar build (dono ou admin)

#### Frontend (`buildService.ts`)
```typescript
import { buildService } from '@/services/buildService'

// Obter recomendação de build (IA)
const recommendation = await buildService.getBuildRecommendation({
  player_name: 'Messi',
  position: 'RWF'
})

// Criar build
const newBuild = await buildService.createBuild({
  card_id: 1,
  title: 'Messi META CF',
  shooting: 10,
  passing: 8,
  dribbling: 10,
  dexterity: 9,
  lower_body_strength: 7,
  aerial_strength: 6,
  defending: 5,
  gk_1: 0,
  gk_2: 0,
  gk_3: 0,
  is_official_meta: false
})

// Listar minhas builds
const myBuilds = await buildService.getMyBuilds()

// Buscar builds de uma carta
const cardBuilds = await buildService.getBuildsByCard(1)

// Atualizar build
await buildService.updateBuild(1, { title: 'Messi CF Updated' })

// Deletar build
await buildService.deleteBuild(1)
```

## 🎨 Componentes de UI

### 1. Builds Component (`/dashboard/builds`)

**Fluxo completo de criação:**
1. **Seleção de Carta** - Usuário escolhe uma carta existente
2. **Criação de Build** - Distribui pontos nos atributos
3. **Salvamento** - Build é salva no backend via API

**Features:**
- Busca de cartas por nome
- Grid responsivo de cartas
- Formulário de build com validação
- Cálculo automático de overall
- Limite de 100 pontos totais

### 2. Catalog Component (`/dashboard/catalog`)

**Visualização de Builds:**
- Lista todas as builds do usuário
- Mostra estatísticas (total, builds META)
- Cards com barras de progresso para cada atributo
- Ação de deletar build
- Estado vazio com mensagem

### 3. Admin Components (Admin apenas)

#### PlayersManager (`/dashboard/admin/players`)
- Listar jogadores com busca
- Criar novo jogador
- Deletar jogador
- Tabela responsiva

#### CardsManager (`/dashboard/admin/cards`)
- Listar cartas com busca
- Criar nova carta (com seleção de jogador)
- Deletar carta
- Formulário completo de carta

## 🔐 Autenticação

Todos os serviços incluem automaticamente o token JWT nas requisições:

```typescript
private getAuthHeaders(): HeadersInit {
  const token = localStorage.getItem('token')
  return {
    'Content-Type': 'application/json',
    ...(token && { 'Authorization': `Bearer ${token}` })
  }
}
```

## ⚠️ Tratamento de Erros

Todos os serviços tratam erros de forma consistente:

```typescript
try {
  const data = await service.method()
} catch (error: any) {
  // error.message contém a mensagem de erro do backend
  console.error('Erro:', error)
  alert(error.message)
}
```

## 🚀 Como Usar

### 1. Iniciar Backend
```bash
cd backend
source .venv/bin/activate
uvicorn main:app --reload
```

### 2. Iniciar Frontend
```bash
cd frontend
npm install
npm run dev
```

### 3. Configurar Variáveis de Ambiente

**Backend (.env):**
```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
JWT_SECRET_KEY=your_secret_key
```

**Frontend (.env):**
```env
VITE_API_URL=http://localhost:8000
```

## 📝 Tipos TypeScript

Todos os serviços incluem tipos TypeScript completos:

```typescript
interface Player {
  id: number
  name: string
  nationality: string
  created_at: string
  updated_at: string
}

interface Card {
  id: number
  player_id: number
  name: string
  version: string
  card_type: string
  position: string
  overall_rating: number
  image_url?: string
  created_at: string
  updated_at: string
}

interface Build {
  id: number
  user_id: string
  card_id: number
  title: string
  shooting: number
  passing: number
  dribbling: number
  // ... outros atributos
  overall_rating?: number
  is_official_meta: boolean
  created_at: string
  updated_at: string
}
```

## ✨ Próximos Passos

1. ✅ Integração básica completa
2. 🔄 Adicionar paginação nos listagens
3. 🔄 Implementar filtros avançados
4. 🔄 Adicionar upload de imagens para cartas
5. 🔄 Melhorar UI/UX dos componentes
6. 🔄 Adicionar testes automatizados
7. 🔄 Implementar cache no frontend
8. 🔄 Adicionar skeleton loading states

## 🐛 Debug

Para debugar requisições, verifique:

1. **Console do navegador** - Mostra erros de requisição
2. **Network tab** - Inspecionar requests/responses
3. **Backend logs** - Terminal rodando uvicorn
4. **Token JWT** - Verificar localStorage no DevTools

## 📚 Documentação Adicional

- [Endpoints Backend](backend/ENDPOINTS_AUTH.md)
- [Endpoints Cards](backend/ENDPOINTS_CARDS.md)
- [Setup Completo](SETUP_COMPLETO.md)
- [Quick Start](QUICK_START.md)
