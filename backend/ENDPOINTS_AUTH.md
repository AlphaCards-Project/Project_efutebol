# 🔐 Endpoints de Autenticação - eFootball Assistant

## Visão Geral

A API possui endpoints completos e funcionais para **registro** e **login** de usuários, integrados com Supabase Auth.

## 🚀 Base URL

```
Local: http://localhost:8000/api/v1
Produção: https://seu-dominio.com/api/v1
```

## 📋 Endpoints Disponíveis

### 1. Registro de Usuário

**POST** `/auth/register`

Cria uma nova conta de usuário no sistema.

#### Request Body

```json
{
  "email": "usuario@exemplo.com",
  "password": "senha123",
  "full_name": "João Silva",       // Opcional
  "nickname": "joaogamer",          // Opcional
  "platform": "console"             // Opcional: console, pc ou mobile
}
```

#### Response (201 Created)

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "usuario@exemplo.com",
    "name": "João Silva",
    "nickname": "joaogamer",
    "platform": "console",
    "role": "free",
    "is_premium": false,
    "daily_questions_used": 0,
    "created_at": "2024-01-01T00:00:00Z"
  }
}
```

#### Erros Possíveis

- **409 Conflict**: Email já cadastrado
- **400 Bad Request**: Dados inválidos (email mal formatado, senha muito curta)
- **500 Internal Server Error**: Erro no servidor

#### Exemplo cURL

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "teste@exemplo.com",
    "password": "senha123",
    "full_name": "Usuário Teste",
    "nickname": "teste123",
    "platform": "console"
  }'
```

#### Exemplo JavaScript (Fetch)

```javascript
const response = await fetch('http://localhost:8000/api/v1/auth/register', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    email: 'usuario@exemplo.com',
    password: 'senha123',
    full_name: 'João Silva',
    nickname: 'joaogamer',
    platform: 'console'
  })
});

const data = await response.json();
console.log('Token:', data.access_token);
console.log('Usuário:', data.user);

// Salvar token no localStorage
localStorage.setItem('token', data.access_token);
```

---

### 2. Login de Usuário

**POST** `/auth/login`

Autentica um usuário existente e retorna um token JWT.

#### Request Body

```json
{
  "email": "usuario@exemplo.com",
  "password": "senha123"
}
```

#### Response (200 OK)

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "usuario@exemplo.com",
    "name": "João Silva",
    "nickname": "joaogamer",
    "platform": "console",
    "role": "free",
    "is_premium": false,
    "daily_questions_used": 5,
    "created_at": "2024-01-01T00:00:00Z"
  }
}
```

#### Erros Possíveis

- **401 Unauthorized**: Email ou senha incorretos
- **400 Bad Request**: Dados inválidos
- **500 Internal Server Error**: Erro no servidor

#### Exemplo cURL

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "teste@exemplo.com",
    "password": "senha123"
  }'
```

#### Exemplo JavaScript (Fetch)

```javascript
const response = await fetch('http://localhost:8000/api/v1/auth/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    email: 'usuario@exemplo.com',
    password: 'senha123'
  })
});

if (response.ok) {
  const data = await response.json();
  localStorage.setItem('token', data.access_token);
  console.log('Login realizado com sucesso!');
} else {
  console.error('Erro no login:', response.status);
}
```

---

### 3. Obter Perfil do Usuário

**GET** `/users/me`

Retorna os dados do usuário autenticado.

#### Headers Obrigatórios

```
Authorization: Bearer <seu_token_jwt>
```

#### Response (200 OK)

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "usuario@exemplo.com",
  "name": "João Silva",
  "nickname": "joaogamer",
  "platform": "console",
  "role": "free",
  "is_premium": false,
  "daily_questions_used": 5,
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### Erros Possíveis

- **401 Unauthorized**: Token inválido ou expirado
- **404 Not Found**: Usuário não encontrado

#### Exemplo cURL

```bash
curl -X GET http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

#### Exemplo JavaScript (Fetch)

```javascript
const token = localStorage.getItem('token');

const response = await fetch('http://localhost:8000/api/v1/users/me', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${token}`,
  }
});

const user = await response.json();
console.log('Dados do usuário:', user);
```

---

### 4. Verificar Quota de Perguntas

**GET** `/users/quota`

Retorna informações sobre a quota de perguntas do usuário.

#### Headers Obrigatórios

```
Authorization: Bearer <seu_token_jwt>
```

#### Response (200 OK)

```json
{
  "daily_limit": 10,
  "questions_used": 5,
  "questions_remaining": 5,
  "is_premium": false,
  "reset_time": "2024-01-02T00:00:00Z"
}
```

#### Exemplo cURL

```bash
curl -X GET http://localhost:8000/api/v1/users/quota \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

---

## 🔑 Autenticação JWT

### Como Funciona

1. Usuário faz **registro** ou **login**
2. Backend retorna um **token JWT** válido
3. Cliente armazena o token (localStorage, cookies, etc)
4. Cliente envia o token em **todas as requisições protegidas**
5. Backend valida o token e identifica o usuário

### Validade do Token

- **Duração**: 7 dias (configurável em `settings.ACCESS_TOKEN_EXPIRE_MINUTES`)
- **Renovação**: Fazer novo login quando expirar

### Formato do Header

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1NTBlODQwMC1lMjliLTQxZDQtYTcxNi00NDY2NTU0NDAwMDAiLCJlbWFpbCI6InVzdWFyaW9AZXhlbXBsby5jb20iLCJpc19wcmVtaXVtIjpmYWxzZSwiZXhwIjoxNzM0MjA4MzAwfQ.signature
```

---

## 🛡️ Segurança

### Proteção Implementada

✅ **Senhas hasheadas** com bcrypt (não armazenadas em texto plano)  
✅ **JWT assinado** com SECRET_KEY forte  
✅ **CORS configurado** para domínios permitidos  
✅ **Row Level Security (RLS)** no Supabase  
✅ **Validação de email** com Pydantic  
✅ **Senha mínima** de 6 caracteres  

### Boas Práticas

- ⚠️ Nunca exponha o token em URLs
- ⚠️ Armazene o token de forma segura (httpOnly cookies quando possível)
- ⚠️ Use HTTPS em produção
- ⚠️ Implemente refresh tokens para longa duração
- ⚠️ Valide sempre a expiração do token no frontend

---

## 📱 Integração Frontend

### React Example

```jsx
import { useState } from 'react';

function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    
    const response = await fetch('http://localhost:8000/api/v1/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });

    if (response.ok) {
      const data = await response.json();
      localStorage.setItem('token', data.access_token);
      localStorage.setItem('user', JSON.stringify(data.user));
      // Redirecionar para dashboard
    }
  };

  return (
    <form onSubmit={handleLogin}>
      <input 
        type="email" 
        value={email} 
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
        required 
      />
      <input 
        type="password" 
        value={password} 
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Senha"
        required 
      />
      <button type="submit">Entrar</button>
    </form>
  );
}
```

### Vue.js Example

```vue
<template>
  <form @submit.prevent="handleLogin">
    <input v-model="email" type="email" placeholder="Email" required />
    <input v-model="password" type="password" placeholder="Senha" required />
    <button type="submit">Entrar</button>
  </form>
</template>

<script>
export default {
  data() {
    return {
      email: '',
      password: ''
    }
  },
  methods: {
    async handleLogin() {
      const response = await fetch('http://localhost:8000/api/v1/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: this.email,
          password: this.password
        })
      });

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('token', data.access_token);
        this.$router.push('/dashboard');
      }
    }
  }
}
</script>
```

---

## 🧪 Testando os Endpoints

### 1. Usando Swagger UI (Recomendado)

Acesse: http://localhost:8000/api/v1/docs

- Interface visual interativa
- Teste todos os endpoints
- Veja exemplos e schemas
- Autorização integrada

### 2. Usando Postman

1. Crie uma nova Collection "eFootball Auth"
2. Adicione os endpoints POST /register e POST /login
3. Salve o token retornado em uma variável de ambiente
4. Use `{{token}}` nos headers de requisições protegidas

### 3. Usando Thunder Client (VS Code)

1. Instale a extensão Thunder Client
2. Crie requisição POST para /register
3. Salve o token retornado
4. Use Environment Variables para reutilizar o token

---

## ❓ FAQ

### Como resetar minha senha?

Por enquanto, não há endpoint de reset de senha. Implementação futura com envio de email.

### Posso ter múltiplas sessões ativas?

Sim, o JWT permite múltiplas sessões. Cada login gera um novo token válido.

### O que acontece quando o token expira?

O backend retorna **401 Unauthorized**. O frontend deve redirecionar para login.

### Posso testar sem criar conta?

Use a rota `/health` para verificar se a API está rodando. Para testar autenticação, crie uma conta de teste.

---

## 🔄 Status dos Endpoints

| Endpoint | Status | Observações |
|----------|--------|-------------|
| POST /auth/register | ✅ Pronto | Totalmente funcional |
| POST /auth/login | ✅ Pronto | Totalmente funcional |
| GET /users/me | ✅ Pronto | Requer autenticação |
| GET /users/quota | ✅ Pronto | Requer autenticação |
| POST /auth/logout | ⏳ Futuro | Invalidar token |
| POST /auth/reset-password | ⏳ Futuro | Reset de senha |
| POST /auth/refresh | ⏳ Futuro | Renovar token |

---

**Última atualização**: 2025-12-06  
**Versão da API**: 1.0.0
