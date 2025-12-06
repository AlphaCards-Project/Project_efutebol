# ⚡ Quick Start - eFootball Assistant

## 🚀 Começar em 5 minutos

### 1. Setup do Banco (2 min)

```bash
# Vá para https://app.supabase.com
# SQL Editor → Cole backend/database/SETUP_DEFINITIVO.sql → Execute
```

### 2. Backend (1 min)

```bash
cd backend

# Configure .env com suas credenciais Supabase
nano .env  # ou use seu editor

# Inicie
source venv/bin/activate
python main.py
```

✅ Backend: http://localhost:8000  
✅ Docs: http://localhost:8000/api/v1/docs

### 3. Frontend (1 min)

```bash
cd frontend
npm install
npm run dev
```

✅ Frontend: http://localhost:5173

### 4. Teste (1 min)

1. Abra http://localhost:5173
2. Clique em "Registre-se"
3. Preencha email e senha
4. ✅ Veja o Dashboard!

---

## 📁 Arquivos Importantes

### Backend
- `database/SETUP_DEFINITIVO.sql` - Script SQL completo
- `ENDPOINTS_AUTH.md` - Documentação da API
- `test_auth_endpoints.py` - Testes automatizados

### Frontend
- `src/components/Auth/Login.tsx` - Tela de login
- `src/components/Auth/Register.tsx` - Tela de registro
- `src/contexts/AuthContext.tsx` - Gerenciamento de estado
- `README_AUTH.md` - Documentação do frontend

### Raiz
- `SETUP_COMPLETO.md` - Guia completo
- `QUICK_START.md` - Este arquivo

---

## 🧪 Testar Backend

```bash
cd backend
python test_auth_endpoints.py
```

---

## 🎨 Cores do Design

- **Dourado**: `#D4AF37`
- **Preto**: `#000000`
- **Cinza**: `#1a1a1a`

---

## ✅ Checklist Rápido

- [ ] Banco criado no Supabase
- [ ] Backend rodando (porta 8000)
- [ ] Frontend rodando (porta 5173)
- [ ] Consegui registrar um usuário
- [ ] Consegui fazer login
- [ ] Vi o Dashboard

Se todos marcados: **🎉 SUCESSO!**

---

## 🐛 Problemas?

### Backend não inicia
```bash
pip install -r requirements.txt
```

### Frontend não compila
```bash
npm install
```

### Erro CORS
Adicione em `backend/.env`:
```
ALLOWED_ORIGINS=http://localhost:5173
```

---

## 📞 Ajuda

Consulte: `SETUP_COMPLETO.md` para guia detalhado

**Status atual**: ✅ **Tudo funcionando!**
