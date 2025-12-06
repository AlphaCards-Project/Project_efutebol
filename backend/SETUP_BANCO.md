# 🗄️ Setup do Banco de Dados - Passo a Passo

## ✅ Status Atual

- ✅ Conexão com Supabase funcionando
- ✅ API Groq (Llama 3.3) funcionando
- ⏳ Tabelas precisam ser criadas

---

## 📋 Como Criar as Tabelas no Supabase

### Opção 1: Via Dashboard (Recomendado - Mais Fácil)

1. **Acesse o Supabase Dashboard:**
   ```
   https://supabase.com/dashboard/project/kpwghdyiuktkedwfpkue
   ```

2. **Vá para SQL Editor:**
   - No menu lateral esquerdo, clique em **"SQL Editor"**
   - Clique no botão **"New Query"**

3. **Cole o Script SQL:**
   - Abra o arquivo: `backend/database/CREATE_TABLES.sql`
   - Copie TODO o conteúdo (Ctrl+A, Ctrl+C)
   - Cole no editor SQL do Supabase (Ctrl+V)

4. **Execute:**
   - Clique no botão **"Run"** (ou pressione Ctrl+Enter)
   - Aguarde 1-2 minutos (o script cria 5 tabelas + índices + funções + RLS)

5. **Verifique:**
   ```bash
   cd backend
   source venv/bin/activate
   python teste_supabase.py
   ```
   
   Você deve ver ✅ em todas as tabelas!

---

## 🎯 O que o Script Cria

### Tabelas:
1. **users** - Usuários (free/premium/admin)
2. **builds** - Builds personalizadas dos usuários
3. **builds_meta** - Builds meta do Pro Player
4. **gameplay_tips** - Dicas de gameplay
5. **user_interactions** - Histórico de consultas

### Recursos:
- ✅ Extensão UUID
- ✅ Índices para performance
- ✅ Triggers para updated_at
- ✅ Funções úteis (reset_daily_quota, etc)
- ✅ Row Level Security (RLS)

---

## 🧪 Testes Realizados

### ✅ Teste Groq (IA):
```bash
python teste_groq.py
```
**Resultado:** Funcionando perfeitamente com Llama 3.3 70B

### ⏳ Teste Supabase:
```bash
python teste_supabase.py
```
**Resultado:** Conectado, aguardando criação das tabelas

---

## 🚀 Depois de Criar as Tabelas

### 1. Popular com Dados Iniciais (Opcional):
```bash
# Executar no SQL Editor do Supabase:
# Copiar conteúdo de: database/INSERT_INITIAL_DATA.sql
```

### 2. Iniciar a API:
```bash
cd backend
source venv/bin/activate
python main.py
```

### 3. Acessar Documentação:
```
http://localhost:8000/docs
```

---

## 📊 Estrutura do Sistema

```
┌─────────────────────────────────────────────────────┐
│                   FRONTEND                          │
│            (React/Vue/Next.js)                      │
└─────────────────┬───────────────────────────────────┘
                  │
                  │ HTTP Requests
                  │
┌─────────────────▼───────────────────────────────────┐
│              BACKEND (FastAPI)                      │
│                                                     │
│  ┌──────────────────────────────────────────────┐  │
│  │  RAG Service (Retrieval-Augmented Gen)       │  │
│  │  └─ knowledge_base/ (builds, gameplay)       │  │
│  └──────────────────────────────────────────────┘  │
│                       │                             │
│                       ├─► Groq (Llama 3.3 70B)      │
│                       │                             │
│                       └─► Supabase (PostgreSQL)     │
└─────────────────────────────────────────────────────┘
```

---

## 🔑 Credenciais Configuradas

No arquivo `.env`:
- ✅ SUPABASE_URL
- ✅ SUPABASE_KEY (publishable)
- ✅ SUPABASE_SERVICE_KEY (secret)
- ✅ API_KEY (Groq)
- ✅ JWT SECRET_KEY

---

## 📝 Próximos Passos

1. ⏳ **Criar tabelas no Supabase** (seguir instruções acima)
2. ⏳ Popular dados iniciais (opcional)
3. ⏳ Testar endpoints da API
4. ⏳ Conectar o frontend

---

## 🆘 Problemas Comuns

### Erro: "Could not find the table"
**Solução:** Tabelas não foram criadas. Execute o script SQL no dashboard.

### Erro: "Invalid API key"
**Solução:** Verifique se a API_KEY do Groq está correta no `.env`

### Erro: "Row Level Security"
**Solução:** O script já configura o RLS. Certifique-se de executar TODO o script.

---

## 📞 Suporte

Se precisar de ajuda:
1. Verifique os logs de erro
2. Execute `python teste_supabase.py` para diagnóstico
3. Consulte a documentação do Supabase

---

**Última atualização:** 2024-12-05
