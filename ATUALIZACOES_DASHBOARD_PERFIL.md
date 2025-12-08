# Atualizações - Dashboard e Edição de Perfil

## 📋 Resumo das Alterações

Este documento descreve as atualizações realizadas no projeto para adicionar funcionalidades de dashboard com estatísticas de usuários e integração completa da edição de perfil.

## 🗄️ Backend - Novos Modelos

### 1. Tabela `user_activities`
Registra todas as atividades dos usuários na plataforma.

**Campos:**
- `id`: ID único da atividade
- `user_id`: ID do usuário (FK para users)
- `activity_type`: Tipo da atividade (ex: "build_consulted", "gameplay_question", etc)
- `activity_data`: Dados adicionais em JSON (player, position, etc)
- `created_at`: Data/hora da atividade

### 2. Tabela `user_stats`
Armazena estatísticas agregadas dos usuários.

**Campos:**
- `id`: ID único
- `user_id`: ID do usuário (FK para users) - ÚNICO
- `total_questions`: Total de perguntas feitas
- `builds_consulted`: Total de builds consultadas
- `gameplay_questions`: Total de perguntas sobre gameplay
- `favorite_position`: Posição favorita (mais consultada)
- `most_searched_player`: Jogador mais buscado
- `last_active`: Última atividade do usuário
- `updated_at`: Última atualização das estatísticas

## 🔌 Backend - Novos Endpoints

### Edição de Perfil

**PUT `/api/v1/users/me`**
Atualiza o perfil do usuário autenticado.

**Body:**
```json
{
  "full_name": "Nome do Usuário",
  "nickname": "nickname_gamer",
  "platform": "console" // ou "pc" ou "mobile"
}
```

**Response:**
```json
{
  "id": "uuid",
  "email": "user@email.com",
  "name": "Nome do Usuário",
  "nickname": "nickname_gamer",
  "platform": "console",
  "role": "free",
  "is_premium": false,
  "daily_questions_used": 5,
  "created_at": "2024-01-01T00:00:00"
}
```

### Estatísticas do Usuário

**GET `/api/v1/users/stats`**
Retorna estatísticas de uso do usuário autenticado.

**Response:**
```json
{
  "total_questions": 45,
  "builds_consulted": 23,
  "gameplay_questions": 22,
  "favorite_position": "CF",
  "most_searched_player": "Messi",
  "last_active": "2024-01-01T00:00:00"
}
```

## 🎨 Frontend - Componentes Atualizados

### 1. Profile.tsx
**Localização:** `frontend/src/profile/Profile.tsx`

**Funcionalidades implementadas:**
- ✅ Carregamento de dados do perfil via API (`GET /api/v1/users/me`)
- ✅ Atualização de perfil via API (`PUT /api/v1/users/me`)
- ✅ Validação de token e redirecionamento para login se não autenticado
- ✅ Validação de nickname duplicado
- ✅ Mensagens de sucesso e erro
- ✅ Loading state durante salvamento

**Campos editáveis:**
- Nome completo (full_name)
- Nickname
- E-mail (visualização apenas, não editável via este endpoint)
- Plataforma (PC, PlayStation, Xbox, Mobile)

### 2. UserStats.tsx (NOVO)
**Localização:** `frontend/src/dashboard/analytics/UserStats.tsx`

**Funcionalidades:**
- ✅ Exibição de estatísticas do usuário
- ✅ Cards visuais com ícones
- ✅ Responsivo para mobile
- ✅ Loading e error states
- ✅ Integração com API

**Estatísticas exibidas:**
- 📊 Total de perguntas
- ⚽ Builds consultadas
- 🎮 Dicas de gameplay
- 🎯 Posição favorita
- ⭐ Jogador mais buscado
- 🕒 Última atividade

## 📦 Schemas Atualizados

### UserUpdate (NOVO)
Para atualização de perfil:
```python
class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, max_length=100)
    nickname: Optional[str] = Field(None, max_length=50)
    platform: Optional[str] = Field(None)
```

### UserStatsResponse (NOVO)
Para resposta de estatísticas:
```python
class UserStatsResponse(BaseModel):
    total_questions: int
    builds_consulted: int
    gameplay_questions: int
    favorite_position: Optional[str]
    most_searched_player: Optional[str]
    last_active: datetime
```

## 🔄 Migrações

Uma nova migração Alembic foi criada automaticamente:
- **Arquivo:** `alembic/versions/a77dd3526054_add_user_stats_and_activities.py`
- **Descrição:** Adiciona tabelas `user_activities` e `user_stats`

Para aplicar as migrações:
```bash
cd backend
source venv/bin/activate
alembic upgrade head
```

## 🔐 Autenticação

Todos os novos endpoints requerem autenticação via Bearer Token:
```
Authorization: Bearer <seu_token_jwt>
```

O token é obtido via login em `/api/v1/auth/login`.

## 🎯 Próximos Passos Sugeridos

### Backend:
1. Implementar sistema de tracking automático de atividades
2. Criar job/cronjob para atualizar estatísticas agregadas periodicamente
3. Adicionar endpoints para histórico de atividades
4. Implementar cache para estatísticas

### Frontend:
1. Adicionar gráficos de evolução temporal (Chart.js ou Recharts)
2. Criar página dedicada de dashboard com mais visualizações
3. Implementar filtros por período nas estatísticas
4. Adicionar comparação com outros usuários (leaderboard)
5. Notificações quando atingir marcos (10 perguntas, 50 builds, etc)

### Features Adicionais:
1. Sistema de conquistas/badges
2. Exportar relatório de estatísticas em PDF
3. Compartilhar estatísticas nas redes sociais
4. Histórico detalhado de perguntas e respostas
5. Favoritar builds e jogadores

## 🧪 Como Testar

### Backend:
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload

# Em outro terminal, testar endpoints:
curl -X GET "http://localhost:8000/api/v1/users/me" \
  -H "Authorization: Bearer SEU_TOKEN"

curl -X PUT "http://localhost:8000/api/v1/users/me" \
  -H "Authorization: Bearer SEU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"full_name":"Novo Nome","nickname":"novo_nick","platform":"pc"}'

curl -X GET "http://localhost:8000/api/v1/users/stats" \
  -H "Authorization: Bearer SEU_TOKEN"
```

### Frontend:
```bash
cd frontend
npm run dev

# Acesse:
# - http://localhost:5173/profile - Editar perfil
# - Componente UserStats pode ser adicionado em qualquer dashboard
```

## 📝 Notas Importantes

1. **O Alembic não foi modificado** - A configuração existente foi mantida
2. **Nickname deve ser único** - Validação implementada no backend
3. **Estatísticas são criadas automaticamente** - Quando não existem, são iniciadas com zeros
4. **Platform é opcional** - Usuário pode não ter plataforma definida
5. **Email não pode ser alterado** - Por questões de segurança e autenticação

## 🐛 Troubleshooting

### Erro: "Nickname já está em uso"
- O nickname escolhido já pertence a outro usuário
- Escolha um nickname diferente

### Erro: "Você precisa estar autenticado"
- Faça login novamente
- Verifique se o token está sendo enviado corretamente

### Estatísticas aparecem zeradas
- Normal para usuários novos
- As estatísticas são incrementadas conforme o uso da plataforma
- Implemente tracking de atividades para popular os dados

### Migração não aplicada
```bash
cd backend
source venv/bin/activate
alembic upgrade head
```

## 📧 Suporte

Em caso de dúvidas ou problemas, consulte a documentação completa em:
- `DOCUMENTACAO.md`
- `QUICK_START.md`
- `SETUP_COMPLETO.md`
