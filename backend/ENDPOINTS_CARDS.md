# 🃏 Endpoints de Cards e Players

## 📋 Visão Geral

Novos endpoints criados para gerenciar **Jogadores** e **Cartas** no sistema.

### Fluxo do Usuário Premium:
1. **Criar Jogador** (se não existir) → `POST /api/v1/cards/players`
2. **Criar Carta** do jogador → `POST /api/v1/cards/`
3. **Criar Build** para aquela carta → `POST /api/v1/builds/create`

---

## 🏃 PLAYERS - Gerenciamento de Jogadores

### 1. Criar Jogador
**`POST /api/v1/cards/players`**

**Permissão:** Premium ou Admin

```json
{
  "name": "Lionel Messi",
  "nationality": "Argentina"
}
```

**Resposta:**
```json
{
  "id": 1,
  "name": "Lionel Messi",
  "nationality": "Argentina",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

---

### 2. Listar Jogadores
**`GET /api/v1/cards/players`**

**Query Params:**
- `search` - Busca por nome (opcional)
- `nationality` - Filtrar por nacionalidade (opcional)
- `limit` - Quantidade de resultados (padrão: 50)
- `offset` - Paginação (padrão: 0)

**Exemplo:**
```
GET /api/v1/cards/players?search=Messi&limit=10
```

---

### 3. Buscar Jogador por ID
**`GET /api/v1/cards/players/{player_id}`**

**Exemplo:**
```
GET /api/v1/cards/players/1
```

---

### 4. Atualizar Jogador
**`PUT /api/v1/cards/players/{player_id}`**

**Permissão:** Apenas Admin

```json
{
  "name": "Lionel Andrés Messi",
  "nationality": "Argentina"
}
```

---

### 5. Deletar Jogador
**`DELETE /api/v1/cards/players/{player_id}`**

**Permissão:** Apenas Admin

⚠️ **Nota:** Não é possível deletar jogadores com cartas associadas.

---

## 🃏 CARDS - Gerenciamento de Cartas

### 1. Criar Carta
**`POST /api/v1/cards/`**

**Permissão:** Premium ou Admin

```json
{
  "player_id": 1,
  "name": "Messi TOTY 2024",
  "version": "TOTY",
  "card_type": "Featured",
  "position": "RWF",
  "overall_rating": 98,
  "image_url": "https://example.com/messi-toty.png"
}
```

**Resposta:**
```json
{
  "id": 1,
  "player_id": 1,
  "name": "Messi TOTY 2024",
  "version": "TOTY",
  "card_type": "Featured",
  "position": "RWF",
  "overall_rating": 98,
  "image_url": "https://example.com/messi-toty.png",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

---

### 2. Listar Cartas
**`GET /api/v1/cards/`**

**Query Params:**
- `player_id` - Filtrar por jogador (opcional)
- `position` - Filtrar por posição (opcional)
- `card_type` - Filtrar por tipo (opcional)
- `search` - Busca por nome da carta (opcional)
- `limit` - Quantidade de resultados (padrão: 50)
- `offset` - Paginação (padrão: 0)

**Exemplo:**
```
GET /api/v1/cards/?position=RWF&card_type=Featured&limit=20
```

---

### 3. Buscar Carta por ID
**`GET /api/v1/cards/{card_id}`**

**Exemplo:**
```
GET /api/v1/cards/1
```

---

### 4. Atualizar Carta
**`PUT /api/v1/cards/{card_id}`**

**Permissão:** Apenas Admin

```json
{
  "overall_rating": 99,
  "image_url": "https://example.com/updated-image.png"
}
```

---

### 5. Deletar Carta
**`DELETE /api/v1/cards/{card_id}`**

**Permissão:** Apenas Admin

⚠️ **Nota:** Não é possível deletar cartas com builds associadas.

---

## 🔗 Integração com Builds

Após criar uma carta, o usuário pode criar builds para ela:

```json
POST /api/v1/builds/create
{
  "card_id": 1,
  "title": "Meta CF - Goal Poacher",
  "shooting": 15,
  "passing": 5,
  "dribbling": 10,
  ...
}
```

E buscar builds de uma carta específica:

```
GET /api/v1/builds/card/1
```

---

## 🔒 Permissões

| Ação | Free | Premium | Admin |
|------|------|---------|-------|
| Listar Players/Cards | ✅ | ✅ | ✅ |
| Criar Player | ❌ | ✅ | ✅ |
| Criar Card | ❌ | ✅ | ✅ |
| Editar Player/Card | ❌ | ❌ | ✅ |
| Deletar Player/Card | ❌ | ❌ | ✅ |

---

## 📊 Exemplo de Fluxo Completo

```bash
# 1. Criar jogador
curl -X POST "http://localhost:8000/api/v1/cards/players" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Cristiano Ronaldo",
    "nationality": "Portugal"
  }'
# Resposta: { "id": 2, ... }

# 2. Criar carta do jogador
curl -X POST "http://localhost:8000/api/v1/cards/" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "player_id": 2,
    "name": "CR7 Icon 99",
    "version": "Icon",
    "card_type": "Legend",
    "position": "CF",
    "overall_rating": 99
  }'
# Resposta: { "id": 5, ... }

# 3. Criar build para a carta
curl -X POST "http://localhost:8000/api/v1/builds/create" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "card_id": 5,
    "title": "Meta CF Finalizador",
    "shooting": 20,
    "passing": 3,
    "dribbling": 12,
    "dexterity": 10,
    "lower_body_strength": 15,
    "aerial_strength": 18,
    "defending": 0,
    "gk_1": 0,
    "gk_2": 0,
    "gk_3": 0,
    "overall_rating": 99,
    "is_official_meta": true
  }'

# 4. Buscar todas as builds da carta
curl -X GET "http://localhost:8000/api/v1/builds/card/5" \
  -H "Authorization: Bearer <token>"
```

---

## ✅ Status da Implementação

### ✅ Completo:
- [x] Endpoints de Players (CRUD completo)
- [x] Endpoints de Cards (CRUD completo)
- [x] Schemas de validação (Pydantic)
- [x] Integração com Builds existentes
- [x] Sistema de permissões (Free/Premium/Admin)
- [x] Validações e tratamento de erros
- [x] Relacionamentos entre tabelas

### 🎯 Próximos Passos (Opcional):
- [ ] Upload de imagens de cartas (integração com storage)
- [ ] Scraper automático para popular cartas do eFootball
- [ ] Sistema de likes/favoritos em cartas
- [ ] Estatísticas de uso das cartas (mais consultadas)
- [ ] Busca avançada com filtros combinados
