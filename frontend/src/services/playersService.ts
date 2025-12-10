const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export interface Player {
  id: number
  name: string
  nationality: string
  created_at: string
  updated_at: string
}

export interface PlayerCreate {
  name: string
  nationality: string
}

export interface PlayerUpdate {
  name?: string
  nationality?: string
}

class PlayersService {
  private getAuthHeaders(): HeadersInit {
    const token = localStorage.getItem('token')
    return {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` })
    }
  }

  async listPlayers(params?: {
    search?: string
    nationality?: string
    limit?: number
    offset?: number
  }): Promise<Player[]> {
    const queryParams = new URLSearchParams()
    if (params?.search) queryParams.append('search', params.search)
    if (params?.nationality) queryParams.append('nationality', params.nationality)
    if (params?.limit) queryParams.append('limit', params.limit.toString())
    if (params?.offset) queryParams.append('offset', params.offset.toString())

    const response = await fetch(
      `${API_BASE_URL}/api/v1/players?${queryParams}`,
      { headers: this.getAuthHeaders() }
    )

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Erro ao buscar jogadores')
    }

    return response.json()
  }

  async getPlayer(playerId: number): Promise<Player> {
    const response = await fetch(
      `${API_BASE_URL}/api/v1/players/${playerId}`,
      { headers: this.getAuthHeaders() }
    )

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Erro ao buscar jogador')
    }

    return response.json()
  }

  async createPlayer(playerData: PlayerCreate): Promise<Player> {
    const response = await fetch(`${API_BASE_URL}/api/v1/players`, {
      method: 'POST',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(playerData)
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Erro ao criar jogador')
    }

    return response.json()
  }

  async updatePlayer(playerId: number, playerData: PlayerUpdate): Promise<Player> {
    const response = await fetch(`${API_BASE_URL}/api/v1/players/${playerId}`, {
      method: 'PUT',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(playerData)
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Erro ao atualizar jogador')
    }

    return response.json()
  }

  async deletePlayer(playerId: number): Promise<{ message: string; detail: string }> {
    const response = await fetch(`${API_BASE_URL}/api/v1/players/${playerId}`, {
      method: 'DELETE',
      headers: this.getAuthHeaders()
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Erro ao deletar jogador')
    }

    return response.json()
  }
}

export const playersService = new PlayersService()
