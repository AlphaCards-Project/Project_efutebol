const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

interface LoginResponse {
  access_token: string
  token_type: string
  user: {
    id: string
    email: string
    name?: string
    nickname?: string
    platform?: string
    role: string
    is_premium: boolean
    daily_questions_used: number
    created_at: string
  }
}

interface GameplayResponse {
  question: string
  answer: string
  category?: string
  video_url?: string
  from_cache: boolean
}

interface QuotaResponse {
  daily_limit: number
  questions_used: number
  questions_remaining: number
  is_premium: boolean
  reset_time: string
}

class ApiService {
  private getAuthHeaders(): HeadersInit {
    const token = localStorage.getItem('token')
    return {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` })
    }
  }

  async askGameplay(question: string): Promise<GameplayResponse> {
    const response = await fetch(`${API_BASE_URL}/api/v1/gameplay/ask`, {
      method: 'POST',
      headers: this.getAuthHeaders(),
      body: JSON.stringify({ question })
    })

    if (!response.ok) {
      if (response.status === 429) {
        throw new Error('Limite diário de perguntas atingido. Faça upgrade para Premium!')
      }
      if (response.status === 401) {
        const error = await response.json()
        throw new Error(error.detail || 'Faça login para fazer novas perguntas')
      }
      const error = await response.json()
      throw new Error(error.detail || 'Erro ao processar pergunta')
    }

    return response.json()
  }

  async getQuota(): Promise<QuotaResponse> {
    const response = await fetch(`${API_BASE_URL}/api/v1/users/quota`, {
      headers: this.getAuthHeaders()
    })

    if (!response.ok) {
      throw new Error('Erro ao buscar quota')
    }

    return response.json()
  }

  async getCurrentUser(): Promise<LoginResponse['user']> {
    const response = await fetch(`${API_BASE_URL}/api/v1/users/me`, {
      headers: this.getAuthHeaders()
    })

    if (!response.ok) {
      throw new Error('Erro ao buscar dados do usuário')
    }

    return response.json()
  }

  async updateUserProfile(data: {
    full_name?: string
    nickname?: string
    platform?: string
  }): Promise<LoginResponse['user']> {
    const response = await fetch(`${API_BASE_URL}/api/v1/users/me`, {
      method: 'PUT',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(data)
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Erro ao atualizar perfil')
    }

    return response.json()
  }

  async getUserStats(): Promise<{
    total_questions: number
    builds_consulted: number
    gameplay_questions: number
    favorite_position?: string
    most_searched_player?: string
    last_active: string
  }> {
    const response = await fetch(`${API_BASE_URL}/api/v1/users/stats`, {
      headers: this.getAuthHeaders()
    })

    if (!response.ok) {
      throw new Error('Erro ao buscar estatísticas')
    }

    return response.json()
  }

  isAuthenticated(): boolean {
    return !!localStorage.getItem('token')
  }

  logout(): void {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }
}

export const apiService = new ApiService()
export type { GameplayResponse, QuotaResponse }
