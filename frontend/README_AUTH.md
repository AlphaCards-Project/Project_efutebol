# 🎮 eFootball Assistant - Frontend

## 🚀 Telas de Autenticação

Este projeto agora possui telas completas de **Login** e **Registro** integradas ao backend FastAPI.

### ✨ Funcionalidades Implementadas

- ✅ Tela de Login elegante (dourado e preto)
- ✅ Tela de Registro com validação
- ✅ Integração completa com backend via API REST
- ✅ Gerenciamento de estado com Context API
- ✅ Armazenamento de token JWT no localStorage
- ✅ Dashboard protegido para usuários autenticados
- ✅ Design responsivo
- ✅ Animações suaves
- ✅ Tratamento de erros

### 🎨 Design

**Cores principais:**
- **Dourado**: `#D4AF37` (Gold) - Elementos principais, bordas, botões
- **Preto**: `#000000` - Background principal
- **Cinza escuro**: `#1a1a1a` - Cards e elementos secundários

**Estilo:**
- Elegante e luxuoso
- Gradientes sutis
- Sombras com glow dourado
- Animações suaves
- Foco em funcionalidade

### 📁 Estrutura de Arquivos

```
src/
├── components/
│   ├── Auth/
│   │   ├── Login.tsx          # Tela de login
│   │   ├── Register.tsx       # Tela de registro
│   │   └── Auth.css           # Estilos das telas de auth
│   └── Dashboard.tsx          # Tela após login
├── contexts/
│   └── AuthContext.tsx        # Context API para autenticação
├── services/
│   └── api.ts                 # Serviço de API (fetch)
├── App.tsx                    # Componente principal
├── index.css                  # Estilos globais
└── main.tsx                   # Entry point
```

### 🔧 Como Rodar

#### 1. Instalar Dependências

```bash
cd frontend
npm install
```

#### 2. Configurar Backend

Certifique-se de que o backend está rodando:

```bash
cd ../backend
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

python main.py
```

O backend deve estar rodando em: `http://localhost:8000`

#### 3. Iniciar Frontend

```bash
cd frontend
npm run dev
```

O frontend estará disponível em: `http://localhost:5173`

### 🔐 Fluxo de Autenticação

1. **Usuário acessa o site** → Vê tela de Login
2. **Clica em "Registre-se"** → Vai para tela de Registro
3. **Preenche formulário** → Envia dados para `/auth/register`
4. **Backend cria usuário** → Retorna JWT token
5. **Frontend salva token** → Armazena no localStorage
6. **Usuário autenticado** → Redirecionado para Dashboard
7. **Ao recarregar página** → Token é lido do localStorage
8. **Clica em "Sair"** → Remove token e volta para Login

### 📝 Campos do Formulário

#### Login
- **Email** (obrigatório)
- **Senha** (obrigatório, mínimo 6 caracteres)

#### Registro
- **Email** (obrigatório)
- **Nome Completo** (opcional)
- **Nickname/Gamertag** (opcional)
- **Plataforma** (opcional: Console, PC ou Mobile)
- **Senha** (obrigatório, mínimo 6 caracteres)
- **Confirmar Senha** (obrigatório)

### 🔑 Integração com API

O serviço de API (`src/services/api.ts`) faz requisições para:

```typescript
// Registro
POST /api/v1/auth/register
Body: { email, password, full_name?, nickname?, platform? }
Response: { access_token, user }

// Login
POST /api/v1/auth/login
Body: { email, password }
Response: { access_token, user }

// Perfil do usuário
GET /api/v1/users/me
Headers: { Authorization: Bearer <token> }
Response: { id, email, name, nickname, platform, role, is_premium, ... }
```

### 🛡️ Segurança

- ✅ Senha nunca exposta no frontend
- ✅ Token JWT armazenado no localStorage
- ✅ Headers de autorização em requisições protegidas
- ✅ Validação de formulários no frontend
- ✅ Validação adicional no backend
- ✅ Mensagens de erro genéricas (não expõe detalhes)

### 🎯 Context API

O `AuthContext` gerencia o estado global da autenticação:

```typescript
const { user, token, loading, login, register, logout } = useAuth();

// Usar em qualquer componente:
if (loading) return <div>Carregando...</div>;
if (!user) return <Login />;
return <Dashboard />;
```

### 📱 Responsividade

O design é totalmente responsivo e funciona em:
- 📱 Mobile (320px+)
- 📱 Tablet (768px+)
- 💻 Desktop (1024px+)
- 🖥️ Large Desktop (1440px+)

### 🎨 Customização

Para alterar as cores, edite o arquivo `Auth.css`:

```css
/* Mudar cor do dourado */
#D4AF37 → sua nova cor

/* Mudar cor do background */
#000000 → sua nova cor

/* Mudar cor dos textos */
#ffffff → sua nova cor
```

### 🐛 Troubleshooting

#### Erro: "Failed to fetch"
- Verifique se o backend está rodando
- Confirme a URL da API no `.env`
- Verifique CORS no backend

#### Erro: "401 Unauthorized"
- Token expirado ou inválido
- Faça logout e login novamente

#### Erro: "409 Conflict"
- Email já cadastrado
- Use outro email ou faça login

#### Página em branco
- Abra o console do navegador (F12)
- Verifique erros no console
- Certifique-se de que o Vite está rodando

### 🚀 Próximos Passos

Após login bem-sucedido, você pode:

1. Adicionar mais páginas (rotas)
2. Implementar React Router
3. Criar página de perfil do usuário
4. Adicionar funcionalidades do eFootball
5. Implementar sistema de perguntas à IA
6. Criar página de builds

### 📚 Tecnologias Utilizadas

- **React 19** - UI Library
- **TypeScript** - Type Safety
- **Vite** - Build Tool
- **Context API** - State Management
- **Fetch API** - HTTP Requests
- **CSS3** - Styling com animações

### 💡 Dicas

1. Use `Ctrl/Cmd + Shift + I` para abrir DevTools
2. Aba "Network" mostra requisições HTTP
3. Aba "Application" > "Local Storage" mostra token salvo
4. Use React DevTools para debug

---

**Desenvolvido com ❤️ para a comunidade eFootball**
