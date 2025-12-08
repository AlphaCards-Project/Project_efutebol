# 🛠️ Scripts de Administração

## Scripts Disponíveis

### 1. 📋 create_admin.py - Criação Interativa
Script interativo completo para criar perfis com todas as opções.

```bash
python create_admin.py
```

**Recursos:**
- Interface interativa amigável
- Criação de Admin, Premium ou Free
- Configuração de nome, nickname, plataforma
- Confirmação de senha
- Resumo antes de confirmar

---

### 2. ⚡ quick_admin.py - Criação Rápida
Script rápido para criar admin via linha de comando.

```bash
python quick_admin.py EMAIL SENHA [NOME] [NICKNAME]
```

**Exemplos:**
```bash
# Admin básico
python quick_admin.py admin@test.com senha123

# Com nome
python quick_admin.py admin@test.com senha123 "João Silva"

# Com nome e nickname
python quick_admin.py admin@test.com senha123 "João Silva" joao_pro
```

---

## 🚀 Uso Rápido

### Criar admin de teste:
```bash
cd backend
python quick_admin.py test@admin.com admin123
```

### Criar admin completo:
```bash
cd backend
python create_admin.py
```

---

## ⚠️ Requisitos

- Python 3.8+
- Arquivo `.env` configurado com credenciais do Supabase
- Virtual environment ativado (ou usar caminho completo do Python)

---

## 💡 Dicas

1. **Para desenvolvimento rápido:**
   Use `quick_admin.py` para criar contas de teste rapidamente

2. **Para produção:**
   Use `create_admin.py` para criar contas com todas as informações

3. **Senha segura:**
   Sempre use senhas fortes em produção (mínimo 12 caracteres)

4. **Verificar criação:**
   Confira no Supabase Dashboard se o usuário foi criado corretamente
