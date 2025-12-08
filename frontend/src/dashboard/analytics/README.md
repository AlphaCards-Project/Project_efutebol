# Analytics - Componentes de Estatísticas

## UserStats Component

Componente para exibir estatísticas do usuário com integração à API.

### Uso

```tsx
import { UserStats } from './dashboard/analytics'

function Dashboard() {
  return (
    <div>
      <h1>Meu Dashboard</h1>
      <UserStats />
    </div>
  )
}
```

### Features

- ✅ Carregamento automático das estatísticas via API
- ✅ Estados de loading e erro
- ✅ Design responsivo
- ✅ Cards com ícones visuais
- ✅ Formatação de data em português

### Estatísticas Exibidas

1. **Total de Perguntas** - Todas as perguntas feitas pelo usuário
2. **Builds Consultadas** - Número de builds visualizadas
3. **Dicas de Gameplay** - Perguntas sobre gameplay
4. **Posição Favorita** - Posição mais consultada (opcional)
5. **Jogador Mais Buscado** - Jogador mais pesquisado (opcional)
6. **Última Atividade** - Data/hora da última interação

### Requisitos

- Usuário autenticado (token JWT no localStorage)
- Backend rodando em `http://localhost:8000`
- Endpoint `/api/v1/users/stats` disponível

### Personalização

Para personalizar as cores, edite `UserStats.css`:

```css
.user-stats {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  /* Altere para suas cores preferidas */
}
```

### API Response

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
