# 🚀 Guia Rápido - eFootball Coach API

## 📝 Resumo do Projeto

Sistema de consultoria inteligente para jogadores de eFootball que responde perguntas sobre:
- **Builds de Cartas**: Distribuição de pontos de habilidade
- **Gameplay**: Dicas táticas e soluções para problemas

### Fluxo Principal
```
Usuário faz pergunta → Sistema busca no banco → IA processa → Responde ao usuário
```

---

## ✅ Checklist de Configuração

### 1. Banco de Dados (Supabase)
- [ ] Acessar https://supabase.com/dashboard
- [ ] Criar/selecionar projeto
- [ ] Ir em **SQL Editor**
- [ ] Executar arquivo: `database/CREATE_TABLES.sql`
- [ ] Testar conexão: `python test_database_connection.py`

### 2. Variáveis de Ambiente (.env)
- [ ] SUPABASE_URL
- [ ] SUPABASE_KEY  
- [ ] SUPABASE_SERVICE_KEY
- [ ] GOOGLE_API_KEY (Gemini)
- [ ] SECRET_KEY (JWT)

### 3. Dependências Python
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Executar API
```bash
python main.py
# Acessar: http://localhost:8000/api/v1/docs
```

---

## 🗄️ Estrutura do Banco (Resumo)

### Tabelas Principais

#### `users` - Usuários
- Quem usa o sistema
- Roles: admin, premium, free
- Quota de perguntas diárias

#### `cards` - Cartas/Jogadores
- Cadastro de jogadores do eFootball
- Exemplo: Neymar, Messi, Ronaldo
- **Preenchido por profissionais via interface futura**

#### `builds` - Builds Meta
- Distribuição de pontos aprovada
- shooting, passing, dribbling, etc (0-99 pontos cada)
- Campo `meta_content` (JSON) com dicas extras
- **Preenchido por profissionais**

#### `gameplay_tips` - Dicas de Gameplay
- Problemas comuns e soluções
- Categorias: ataque, defesa, passe, etc
- **Preenchido por profissionais**

#### `ai_cache` - Cache de Respostas
- Economiza chamadas à API do Gemini
- Armazena hash da pergunta + resposta
- Auto-gerenciado pelo sistema

---

## 🔄 Como o Sistema Funciona

### Exemplo: Pergunta sobre Build

1. **Usuário**: "Qual a melhor build para Neymar LWF?"

2. **Sistema verifica**:
   - ✅ Usuário autenticado?
   - ✅ Tem quota disponível?
   - ✅ Resposta já está em cache?

3. **RAG busca no banco**:
   ```sql
   SELECT * FROM builds 
   WHERE card_id = (SELECT id FROM cards WHERE name LIKE '%Neymar%')
   AND meta_content->>'position' = 'LWF'
   ```

4. **Contexto encontrado**:
   ```json
   {
     "shooting": 10,
     "dribbling": 10,
     "speed": 8,
     "playstyle": "Prolific Winger",
     "dicas": ["Use Double Touch", "Finalize de fora"]
   }
   ```

5. **IA processa** com contexto rico:
   ```
   Prompt: Você é especialista em eFootball.
   
   Jogador: Neymar Jr
   Posição: LWF
   Build oficial: shooting=10, dribbling=10...
   
   Forneça resposta detalhada...
   ```

6. **Resposta** enviada ao usuário + salva em cache

---

## 📊 Status Atual do Banco

Execute o teste para verificar:
```bash
python test_database_connection.py
```

**Resultado esperado**:
```
✅ users                 | Usuários do sistema
✅ cards                 | Cartas/Jogadores  
✅ builds                | Builds de cartas
✅ gameplay_tips         | Dicas de gameplay
✅ ai_cache              | Cache da IA
```

---

## 🛠️ Preenchimento de Dados (Próximos Passos)

### Interface futura permitirá profissionais cadastrarem:

#### 1. Cartas (cards)
```sql
INSERT INTO cards (konami_id, name, card_type, position)
VALUES (12345, 'Neymar Jr', 'Legendary', 'LWF');
```

#### 2. Builds (builds)
```sql
INSERT INTO builds (
    user_id, card_id, title,
    shooting, passing, dribbling, dexterity,
    is_official_meta, meta_content
) VALUES (
    1, 123, 'Neymar LWF Meta',
    10, 7, 10, 8,
    true,
    '{"playstyle": "Prolific Winger"}'::jsonb
);
```

#### 3. Dicas (gameplay_tips)
```sql
INSERT INTO gameplay_tips (category, title, solution)
VALUES (
    'finalizacao',
    'Como fazer finesse shot',
    '1. Segure L2+R2 ao chutar
     2. Direcione para canto oposto'
);
```

---

## 🔑 Endpoints Principais

### Autenticação
```bash
POST /api/v1/auth/register
POST /api/v1/auth/login
```

### Builds
```bash
POST /api/v1/builds/
Body: {"player_name": "Neymar", "position": "LWF"}
```

### Gameplay
```bash
POST /api/v1/gameplay/ask
Body: {"question": "Como fazer finesse shot?"}
```

### Quota
```bash
GET /api/v1/users/quota
```

---

## 📈 Limites e Quotas

| Tipo    | Perguntas/dia |
|---------|---------------|
| Free    | 5             |
| Premium | 100           |

Reset diário automático às 00:00 UTC.

---

## 🐛 Troubleshooting

### Tabelas não encontradas
➡️ Execute o SQL no Supabase Dashboard

### Erro de autenticação
➡️ Verifique .env (SUPABASE_URL e SUPABASE_KEY)

### IA não responde
➡️ Verifique GOOGLE_API_KEY no .env

### Quota excedida
➡️ Aguarde reset (00:00 UTC) ou faça upgrade para premium

---

## 📚 Documentação Completa

Para detalhes técnicos completos, consulte:
- `DOCUMENTACAO.md` - Documentação técnica completa
- `database/CREATE_TABLES.sql` - Estrutura do banco
- `README.md` - Informações do projeto

---

## 🎯 Comandos Úteis

```bash
# Ativar ambiente virtual
source venv/bin/activate

# Testar banco
python test_database_connection.py

# Executar API
python main.py

# Ver logs
tail -f logs/app.log

# Testar endpoint
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"123456"}'
```

---

**Versão**: 1.0.0  
**Última atualização**: Dezembro 2024
